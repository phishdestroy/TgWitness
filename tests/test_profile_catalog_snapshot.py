import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextvars import Context, copy_context
import json
from types import SimpleNamespace

import pytest

from tgwitness.collector import Collector
from tgwitness.network import NetworkConfig, RoutePolicy
from tgwitness.profiles import Profiles
from tgwitness.proxy_catalog import ProxyPool, PublicCatalog
from tgwitness.security import Vault
from tgwitness.store import Store


SECRET = "ab" * 16


def proxy(alias):
    return {"id": alias, "label": alias,
            "route": NetworkConfig(kind="mtproxy", host=alias + ".example.org", port=443, secret=SECRET)}


class Catalog:
    def __init__(self, *aliases):
        self.rows = [proxy(alias) for alias in aliases]
        self.calls = 0
        self.failure = False

    def catalog(self):
        self.calls += 1
        if self.failure:
            raise ValueError("Invalid operator catalog")
        return {"mode": "bundled", "proxies": self.rows}


@pytest.fixture
def registry(tmp_path):
    stores = []

    def workspace(number, pool):
        root = tmp_path / str(number)
        root.mkdir()
        vault = Vault(root)
        store = Store(root)
        stores.append(store)
        store.bind(vault)
        collector = Collector(store, vault)
        collector.proxy_pool = pool
        return SimpleNamespace(state=SimpleNamespace(store=store, vault=vault, collector=collector))

    main = workspace(0, ProxyPool(Catalog("main")))
    profiles = Profiles(main, tmp_path, None)

    def add(pool):
        number = len(profiles.entries)
        app = workspace(number, pool)
        pid = f"{number:032x}"
        profiles.entries[pid] = {"id": pid, "label": str(number), "app": app, "cm": None}
        return app

    yield profiles, main, add
    for store in stores:
        store.close()


def test_summary_reads_shared_catalog_once_and_refreshes_next_time(registry):
    profiles, main, add = registry
    pool = main.state.collector.proxy_pool
    add(pool)
    first = profiles.summary()
    assert pool.catalog.calls == 1
    assert [row["collector"]["network"]["pool"]["listed"] for row in first] == [1, 1]
    pool.catalog.rows.append(proxy("new"))
    second = profiles.summary()
    assert pool.catalog.calls == 2
    assert [row["collector"]["network"]["pool"]["listed"] for row in second] == [2, 2]


def test_summary_keeps_pools_separate_and_skips_unavailable_apps(registry):
    profiles, main, add = registry
    first = main.state.collector.proxy_pool
    second = ProxyPool(Catalog("other", "another"))
    add(second)
    add(first)
    profiles.entries["unavailable"] = {"id": "unavailable", "label": "Unavailable", "app": None,
                                       "error_type": "SyntheticFailure"}
    rows = profiles.summary()
    assert first.catalog.calls == second.catalog.calls == 1
    assert [row["collector"]["network"]["pool"]["listed"] for row in rows[:3]] == [1, 2, 1]
    assert rows[3]["collector"] is None and rows[3]["error_type"] == "SyntheticFailure"


def test_summary_does_not_read_catalog_for_fixed_routes(registry):
    profiles, main, add = registry
    pool = main.state.collector.proxy_pool
    other = add(pool)
    main.state.vault.save("network", {"kind": "direct"})
    other.state.vault.save("network", proxy("fixed")["route"].model_dump())
    rows = profiles.summary()
    assert [row["collector"]["network"]["kind"] for row in rows] == ["direct", "mtproxy"]
    assert pool.catalog.calls == 0


def test_summary_leaves_signed_journals_unchanged(registry):
    profiles, main, add = registry
    other = add(main.state.collector.proxy_pool)
    apps = (main, other)
    for index, app in enumerate(apps):
        app.state.store.append("message.new", {"text": "Synthetic record"}, 100 + index, 1)
    before = [app.state.store.stats() for app in apps]
    profiles.summary()
    profiles.summary()
    assert [app.state.store.stats() for app in apps] == before
    for app in apps:
        app.state.store.verify(app.state.vault.public_key)


def test_invalid_operator_does_not_fall_back_and_valid_empty_stays_operator(tmp_path, monkeypatch):
    path = tmp_path / "operator.json"
    path.write_text("invalid", encoding="utf-8")
    monkeypatch.setenv("TGWITNESS_PROXY_CATALOG", str(path))
    catalog = PublicCatalog(tmp_path)
    monkeypatch.setattr(catalog, "snapshot", lambda: pytest.fail("Operator must not fall back to public lists"))
    pool = ProxyPool(catalog)
    with pool.read_snapshot():
        assert pool.describe("owner")["pool"]["listed"] == 0
        with pytest.raises(ValueError, match="catalog is unavailable"):
            pool.entries()
        path.write_text(json.dumps({"format": "tgwitness-proxy-catalog-v1", "proxies": []}), encoding="utf-8")
        operator, entries = pool.entries()
        assert operator is True and not entries
        with pytest.raises(TypeError):
            entries["bad"] = proxy("bad")
    path.write_text("invalid again", encoding="utf-8")
    with pytest.raises(ValueError, match="catalog is unavailable"):
        pool.entries()


def test_failed_read_is_not_cached_and_runtime_health_stays_live():
    catalog = Catalog("one", "two")
    pool = ProxyPool(catalog)
    catalog.failure = True
    with pool.read_snapshot():
        assert pool.describe("a")["pool"]["listed"] == 0
        catalog.failure = False
        pool.assigned.update(a="one", b="two")
        assert pool.describe("a")["current"]["host"] == "one.example.org"
        pool.succeeded("one", latency_ms=12)
        assert pool.describe("a")["pool"]["healthy"] == 1
        pool.assigned["a"] = "two"
        pool.degrade("one", "SyntheticFailure")
        changed = pool.describe("a")
        assert changed["current"]["host"] == "two.example.org"
        assert changed["pool"]["healthy"] == 0 and changed["pool"]["resting"] == 1
        assert pool.describe("b")["current"]["host"] == "two.example.org"
        assert SECRET not in json.dumps(changed)
        assert catalog.calls == 2


def test_workspace_exposure_is_not_part_of_shared_snapshot(registry):
    _, main, add = registry
    pool = main.state.collector.proxy_pool
    other = add(pool)
    with pool.read_snapshot():
        assert main.state.collector.status()["network"]["exposure"] == "hide"
        main.state.store.set_setting("route_policy", RoutePolicy(exposure="tunnel").model_dump())
        assert main.state.collector.status()["network"]["exposure"] == "tunnel"
        assert other.state.collector.status()["network"]["exposure"] == "hide"
    assert pool.catalog.calls == 1


def test_snapshot_restores_outer_scope_and_clears_on_exception():
    catalog = Catalog("one")
    pool = ProxyPool(catalog)
    with pool.read_snapshot():
        assert set(pool.entries()[1]) == {"one"}
        catalog.rows.append(proxy("two"))
        with pytest.raises(RuntimeError, match="stop"):
            with pool.read_snapshot():
                assert set(pool.entries()[1]) == {"one", "two"}
                raise RuntimeError("stop")
        assert set(pool.entries()[1]) == {"one"}
    assert set(pool.entries()[1]) == {"one", "two"}
    assert catalog.calls == 3


def test_summary_exception_resets_every_entered_pool(registry, monkeypatch):
    profiles, main, add = registry
    first = main.state.collector.proxy_pool
    second = ProxyPool(Catalog("second"))
    other = add(second)

    def fail():
        second.describe("other")
        raise RuntimeError("Synthetic collector failure")

    monkeypatch.setattr(other.state.collector, "status", fail)
    with pytest.raises(RuntimeError, match="Synthetic collector"):
        profiles.summary()
    assert first.catalog.calls == second.catalog.calls == 1
    first.entries()
    second.entries()
    assert first.catalog.calls == second.catalog.calls == 2


def test_foreign_context_and_copied_thread_do_not_reuse_snapshot():
    catalog = Catalog("one")
    pool = ProxyPool(catalog)
    with pool.read_snapshot():
        pool.entries()
        catalog.rows.append(proxy("two"))
        assert set(Context().run(pool.entries)[1]) == {"one", "two"}
        with ThreadPoolExecutor(max_workers=1) as executor:
            inherited = copy_context()
            assert set(executor.submit(inherited.run, pool.entries).result()[1]) == {"one", "two"}
        assert set(pool.entries()[1]) == {"one"}
        escaped = copy_context()
    assert set(escaped.run(pool.entries)[1]) == {"one", "two"}
    assert catalog.calls == 4


def test_child_task_does_not_inherit_parent_view_snapshot():
    pool = ProxyPool(Catalog("one"))

    async def run():
        async def read():
            return pool.entries()

        with pool.read_snapshot():
            pool.entries()
            pool.catalog.rows.append(proxy("two"))
            assert set((await asyncio.create_task(read()))[1]) == {"one", "two"}
            assert set(pool.entries()[1]) == {"one"}
        assert set(pool.entries()[1]) == {"one", "two"}

    asyncio.run(run())
    assert pool.catalog.calls == 3
