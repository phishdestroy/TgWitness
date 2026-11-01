"""The panel's guided 24/7 server: python -m tgwitness.cloud deploy and destroy, started from the local panel.

Hetzner hosts the server. Its address is a quick tunnel on trycloudflare.com, or a name under the user's own
domain when a Cloudflare token comes along. The tokens come with each request
from the browser on this computer and live only for that request or task: nothing writes them down. The
deployment record, the redacted installer and the panel token are kept under the data directory, as the
command line keeps them under deployments/.
"""
import json
import re
import secrets
import threading
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

import requests
from pydantic import BaseModel, field_validator

from . import __version__, cloud
from .providers import get
from .providers.base import DeployError
from .store import utcnow

# Region → preferred location, then any location in these network zones.
REGIONS = {"eu": ("nbg1", ("eu-central",)), "us": ("ash", ("us-east", "us-west"))}
PREFERRED_TYPE = "cpx22"  # the type the deployment guide starts with; otherwise the cheapest that fits
MIN_MEMORY = 2
GITHUB = "https://api.github.com/repos/phishdestroy/TgWitness/commits/"
FILES = {"deployment.json": "application/json", "panel-token.txt": "text/plain; charset=utf-8",
         "cloud-init.redacted.yaml": "text/plain; charset=utf-8"}
HETZNER_TOKEN = re.compile(r"[A-Za-z0-9]{32,128}")
CLOUDFLARE_TOKEN = re.compile(r"[A-Za-z0-9_-]{20,400}")


class WizardError(ValueError):
    """A problem the user can solve; technical holds the service's own answer."""

    def __init__(self, message, technical=""):
        super().__init__(message)
        self.technical = technical


def plain(value):
    return (value or "").strip()


class Tokens(BaseModel):
    hetzner_token: str
    cloudflare_token: str = ""

    @field_validator("hetzner_token")
    @classmethod
    def hetzner(cls, value):
        if not HETZNER_TOKEN.fullmatch(plain(value)):
            raise ValueError("Paste the Hetzner API token: letters and digits, shown once when it is created.")
        return plain(value)

    @field_validator("cloudflare_token")
    @classmethod
    def cloudflare(cls, value):
        if plain(value).startswith("cfk_"):
            raise ValueError("This is the Cloudflare Global API Key. Leave the field empty, or create an API token "
                             "with the prepared link.")
        if plain(value) and not CLOUDFLARE_TOKEN.fullmatch(plain(value)):
            raise ValueError("Paste the Cloudflare API token, shown once when it is created.")
        return plain(value)


class Check(Tokens):
    region: Literal["eu", "us"] = "eu"
    gateway: bool = False


class Deploy(Check):
    zone: str = ""
    account: str = ""
    gateway_account: str = ""
    location: str
    server_type: str
    name: str | None = None
    ref: str | None = None

    @field_validator("name", "ref")
    @classmethod
    def optional(cls, value):
        return plain(value) or None


class Destroy(Tokens):
    name: str
    confirm: str


class Address(BaseModel):
    name: str


def explain(exc):
    """A message that says what to do; the service's own words stay in technical. API errors start with the
    service's name (providers.base.Api.call)."""
    text = str(exc)
    head = text.split(":", 1)[0]
    if "did not answer in time" in text:
        return WizardError("The server was created but TgWitness on it did not answer in time. It may still be "
                           "installing: check the address later, or delete the server and start again.", text)
    if "no further DNS location" in text:
        return WizardError("Your Cloudflare account allows no more DNS locations and has several already. Remove "
                           "one in Cloudflare Zero Trust, or choose one with the command line option "
                           "--gateway-location.", text)
    if "does not accept DNS over TLS" in text:
        return WizardError("Your Gateway DNS location does not accept DNS over TLS. Turn it on for the location in "
                           "Cloudflare Zero Trust, then try again.", text)
    if "already has DNS records" in text:
        return WizardError("This address is already used in your domain. Choose another server name under "
                           "Advanced.", text)
    if head.startswith("Hetzner"):
        if "HTTP 401" in text:
            return WizardError("Hetzner did not accept the token. Copy it again from Security → API tokens in "
                               "your Hetzner project.", text)
        if "forbidden" in text or "HTTP 403" in text:
            return WizardError("The Hetzner token is read-only. Create a new token with Read & Write permission.",
                               text)
        if "resource_limit_exceeded" in text:
            return WizardError("Hetzner refused: the project's server limit is reached. Remove an unused server "
                               "or ask Hetzner to raise the limit.", text)
        if "resource_unavailable" in text or "placement_error" in text:
            return WizardError("Hetzner has no free server of this type in this location right now. Choose the "
                               "other region or try again later.", text)
        if "uniqueness_error" in text:
            return WizardError("A server with this name already exists in the Hetzner project. Choose another "
                               "name under Advanced.", text)
        return WizardError("Hetzner refused the request.", text)
    if head.startswith("Cloudflare"):
        if "HTTP 401" in text or "HTTP 403" in text or "10000" in text or "9109" in text:
            return WizardError("Cloudflare did not accept the token or it lacks a permission. Create the token "
                               "with the prepared link: Zone Read, DNS Edit and Cloudflare Tunnel Edit.", text)
        return WizardError("Cloudflare refused the request.", text)
    return WizardError("The task stopped.", text)


def location(region, locations):
    preferred, zones = REGIONS[region]
    for item in locations:
        if item["name"] == preferred:
            return item
    for zone in zones:
        for item in locations:
            if item.get("network_zone") == zone:
                return item
    raise WizardError("Hetzner offers no server location in this region right now. Choose the other region.")


def server_type(types, place):
    """The guide's type where Hetzner offers it here, else the cheapest x86 type with enough memory."""
    offers = []
    for kind in types:
        if kind.get("deprecated") or kind.get("deprecation") or kind.get("architecture", "x86") != "x86" \
                or float(kind.get("memory") or 0) < MIN_MEMORY:
            continue
        here = [item for item in kind.get("locations") or [] if item.get("name") == place]
        if kind.get("locations") is not None and not (here and here[0].get("available", True)
                                                       and not here[0].get("deprecation")):
            continue
        price = next((p for p in kind.get("prices") or [] if p.get("location") == place), None)
        if price:
            offers.append((float(price["price_monthly"]["gross"]), kind))
    if not offers:
        raise WizardError("Hetzner has no suitable server in this location right now. Choose the other region.")
    monthly, kind = next((o for o in offers if o[1]["name"] == PREFERRED_TYPE), None) or min(offers, key=lambda o: o[0])
    return {"name": kind["name"], "cores": kind.get("cores"), "memory": kind.get("memory"), "disk": kind.get("disk"),
            "monthly": "%.2f" % monthly}


def version(ref=None, session=None):
    """The commit the server installs: a 40-character commit as given, otherwise a tag or branch on GitHub."""
    ref = ref or "v" + __version__
    if cloud.COMMIT.fullmatch(ref):
        return {"ref": ref, "commit": ref}
    if not cloud.TAG.fullmatch(ref) or ".." in ref:
        raise WizardError("Enter a release tag such as v1.0.0 or a 40-character commit.")
    try:
        response = (session or requests).request("GET", GITHUB + ref, timeout=30, headers={
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    except requests.RequestException as exc:
        raise WizardError("GitHub could not be reached to look up the version. Try again.", str(exc)) from None
    if response.status_code in (404, 422):
        raise WizardError("This version is not published on GitHub. Enter a release tag or a commit under "
                          "Advanced.", ref)
    if response.status_code != 200:
        raise WizardError("GitHub did not answer the version lookup. Try again later, or enter the 40-character "
                          "commit under Advanced.", "HTTP " + str(response.status_code))
    commit = response.json().get("sha", "")
    if not cloud.COMMIT.fullmatch(commit):
        raise WizardError("GitHub returned an unexpected answer for this version.", ref)
    return {"ref": ref, "commit": commit}


def services(tokens, session=None):
    cf = cloud.Cloudflare(tokens.cloudflare_token, session) if tokens.cloudflare_token else None
    return get("hetzner")(tokens.hetzner_token, session=session), cf


def check(request, session=None):
    """What would be created, at what monthly price, and under which of the user's domains when a Cloudflare
    token is given; creates nothing."""
    hetzner, cf = services(request, session)
    try:
        place = location(request.region, hetzner.call("GET", "/locations")["locations"])
        offer = server_type(hetzner.pages("/server_types", "server_types"), place["name"])
        currency = hetzner.call("GET", "/pricing")["pricing"]["currency"]
    except DeployError as exc:
        raise explain(exc) from None
    found = {"location": {"name": place["name"], "city": place.get("city"), "country": place.get("country")},
             "server": offer, "currency": currency, "domains": [], "gateway_accounts": [],
             "version": version(session=session)}
    if cf is None:
        if request.gateway:
            raise WizardError("Gateway DNS needs a Cloudflare API token. Paste one, or turn Gateway DNS off.")
        return found
    try:
        accounts = cf.result("GET", "/accounts", params={"per_page": 50}) or []
        zones = cf.result("GET", "/zones", params={"per_page": 50, "status": "active"}) or []
    except DeployError as exc:
        raise explain(exc) from None
    if request.gateway:
        found["gateway_accounts"] = gateway_accounts(cf, accounts)
        if not found["gateway_accounts"]:
            raise WizardError("The Cloudflare token cannot manage Gateway. Add the permission Account · Zero Trust · "
                              "Edit for your account.")
    tunnels = set()
    for account in accounts:
        try:
            cf.result("GET", "/accounts/" + account["id"] + "/cfd_tunnel", params={"per_page": 1})
            tunnels.add(account["id"])
        except DeployError:
            pass
    if request.gateway and not (zones and tunnels):
        return found  # Gateway DNS needs no domain: the quick tunnel stays
    if not zones:
        raise WizardError("The Cloudflare token sees no active domain. Add your domain to Cloudflare, or allow "
                          "the token for it.")
    if not tunnels:
        raise WizardError("The Cloudflare token cannot manage tunnels. Add the permission Account · Cloudflare "
                          "Tunnel · Edit.")
    domains = [{"name": z["name"], "account": z["account"]["id"]} for z in zones
               if (z.get("account") or {}).get("id") in tunnels]
    if not domains:
        raise WizardError("The token can manage tunnels, but not in the account that holds your domain.")
    return {**found, "domains": domains}


def gateway_accounts(cf, accounts):
    """The accounts in which the token may run Gateway; one that has never used Gateway counts, deploy switches
    it on there."""
    usable = []
    for account in accounts:
        try:
            locations = cf.result("GET", "/accounts/" + account["id"] + "/gateway/locations") or []
        except DeployError as exc:
            if "1001" not in str(exc):
                continue
            locations = []
        usable.append({"id": account["id"], "name": account.get("name"), "locations": len(locations)})
    return usable


class Jobs:
    """One server task at a time, in a thread: deploying waits up to half an hour for the new server."""

    def __init__(self, root, session=None, fetch=None, beacon=None):
        self.directory = Path(root) / "deployments"
        self.session, self.fetch = session, fetch or cloud.collector_statement
        self.beacon = beacon or (lambda topic, key=None: cloud.read_beacon(topic, key, self.session))
        self.guard, self.job = threading.Lock(), None

    def check(self, request):
        return check(request, self.session)

    def status(self):
        with self.guard:
            job = None if self.job is None else {**self.job, "lines": list(self.job["lines"])}
        return {"job": job, "deployments": self.deployments()}

    def deployments(self):
        found = []
        for path in sorted(self.directory.glob("*/deployment.json")) if self.directory.is_dir() else ():
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            server = record.get("server") or {}
            found.append({"name": record.get("name"), "provider": record.get("provider"), "state": record.get("state"),
                          "created_at": record.get("created_at"), "panel_host": record.get("panel_host"),
                          "server_type": record.get("server_type"), "location": record.get("location"),
                          "ipv4": server.get("ipv4"), "commit": record.get("commit"),
                          "fingerprint": (record.get("collector") or {}).get("fingerprint"),
                          "quick": bool(record.get("beacon")), "address": (record.get("address") or {}).get("host"),
                          "gateway": bool(record.get("gateway"))})
        return found

    def address(self, name):
        """The quick tunnel's current address, as the server last posted it signed with this deployment's key."""
        folder = self.directory / name
        if not cloud.NAME.fullmatch(name) or not (folder / "deployment.json").is_file():
            raise WizardError("This deployment does not exist.")
        record = json.loads((folder / "deployment.json").read_text(encoding="utf-8"))
        if not record.get("beacon") or not (folder / "address-key.txt").is_file():
            raise WizardError("This server has a fixed address under your domain.")
        try:
            found = self.beacon(record["beacon"], (folder / "address-key.txt").read_text(encoding="utf-8").strip())
        except DeployError as exc:
            raise WizardError("The server has not posted an address in the last 12 hours. It may be stopped: check "
                              "it in the Hetzner console.", str(exc)) from None
        except requests.RequestException as exc:
            raise WizardError("ntfy.sh, where the server posts its address, could not be reached. Try again.",
                              str(exc)) from None
        with self.guard:
            record["address"] = {"host": found["host"], "posted": found["posted"], "seen_at": utcnow()}
            cloud.write_record(folder / "deployment.json", record)
        return {"name": name, "address": found["host"], "posted": found["posted"]}

    def file(self, name, filename):
        path = self.directory / name / filename
        if not cloud.NAME.fullmatch(name) or filename not in FILES or not path.is_file():
            raise WizardError("This deployment file does not exist.")
        return path, FILES[filename]

    def start(self, kind, name, work):
        with self.guard:
            if self.job and self.job["state"] == "running":
                raise WizardError("Another server task is still running. Wait until it ends.")
            job = self.job = {"id": secrets.token_hex(8), "kind": kind, "name": name, "state": "running",
                              "stage": "start", "started_at": utcnow(), "finished_at": None, "lines": [],
                              "error": None, "result": None}

        def progress(stage, text):
            with self.guard:
                job["stage"] = stage
                job["lines"].append({"at": utcnow(), "text": text})

        def run():
            try:
                result, error = work(progress), None
            except WizardError as exc:
                result, error = None, {"message": str(exc), "technical": exc.technical}
            except DeployError as exc:
                problem = explain(exc)
                result, error = None, {"message": str(problem), "technical": problem.technical}
            except Exception as exc:  # the panel must outlive any failure of this task
                result, error = None, {"message": "The task stopped.", "technical": type(exc).__name__ + ": " + str(exc)}
            with self.guard:
                job.update(state="failed" if error else "done", error=error, result=result, finished_at=utcnow())

        threading.Thread(target=run, name="tgwitness-cloud-" + kind, daemon=True).start()
        return self.status()

    def deploy(self, request):
        name = request.name or "tgw-" + secrets.token_hex(3)
        if not cloud.NAME.fullmatch(name):
            raise WizardError("Server name: lowercase letters, digits and hyphens, up to 50 characters.")
        if (self.directory / name).exists():
            raise WizardError("A deployment with this name already exists. Choose another server name.")
        quick = not (request.zone or request.account)
        if not quick and (not request.cloudflare_token or not cloud.ACCOUNT.fullmatch(request.account)
                          or not cloud.HOST.fullmatch(request.zone)):
            raise WizardError("Check the tokens again and choose one of the listed domains.")
        gateway_account = request.account or request.gateway_account
        if request.gateway and not (request.cloudflare_token and cloud.ACCOUNT.fullmatch(gateway_account)):
            raise WizardError("Check the Cloudflare token again and choose the account for Gateway DNS.")

        def work(progress):
            progress("version", "Looking up the TgWitness version on GitHub")
            chosen = version(request.ref, self.session)
            hetzner, cf = services(request, self.session)
            args = SimpleNamespace(provider="hetzner", name=name, server_type=request.server_type,
                                   location=request.location, image=None, ref=chosen["ref"],
                                   repository=cloud.DEFAULT_REPOSITORY, zone=request.zone or None,
                                   cloudflare_account=(gateway_account if request.gateway else request.account) or None,
                                   gateway_dns=request.gateway, gateway_location=None,
                                   panel_host=None if quick else name + "." + request.zone, quick_tunnel=quick,
                                   witness_host=None, debug_ssh_key=None, debug_ssh_from=None,
                                   out=self.directory / name, wait=30)
            if not quick:
                progress("tunnel", "Cloudflare: creating the tunnel and the address " + args.panel_host)
            record, out = cloud.deploy(args, hetzner, cf, self.fetch, resolve=lambda repository, ref: chosen["commit"],
                                       progress=progress, beacon=self.beacon)
            progress("done", "TgWitness answered with its signing key " + record["collector"]["fingerprint"])
            host = record["address"]["host"] if quick else record["panel_host"]
            return {"name": name, "panel": "https://" + host, "quick": quick, "fingerprint":
                    record["collector"]["fingerprint"], "server": record["server"].get("ipv4"),
                    "commit": record["commit"], "ref": record.get("requested_ref"),
                    "gateway": record.get("gateway"), "gateway_shared": record.get("gateway_shared")}

        self.directory.mkdir(parents=True, exist_ok=True)
        return self.start("deploy", name, work)

    def destroy(self, request):
        path = self.directory / request.name / "deployment.json"
        if not cloud.NAME.fullmatch(request.name) or not path.is_file():
            raise WizardError("This deployment does not exist.")
        if request.confirm.strip() != request.name:
            raise WizardError("Type the server name to confirm the deletion.")
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("provider") not in ("hetzner", "generic"):
            raise WizardError("Only Hetzner servers can be deleted here. Use python -m tgwitness.cloud destroy.")
        if not record.get("beacon") and not request.cloudflare_token:
            raise WizardError("This server's address is under your domain: paste the Cloudflare token as well, so "
                              "its tunnel and DNS record are deleted too.")
        if record.get("gateway") and not request.cloudflare_token:
            raise WizardError("This server resolves through Cloudflare Gateway: paste the Cloudflare token as well, "
                              "so its DNS location is removed too.")

        def work(progress):
            hetzner, cf = services(request, self.session)
            args = SimpleNamespace(record=path, confirm=request.name, provider_token_file=None,
                                   cloudflare_token_file=None)
            record, removed = cloud.destroy(args, hetzner, cf, progress)
            progress("done", "Deleted: " + ", ".join(item["resource"] + " " + str(item["id"]) for item in removed))
            return {"name": request.name, "removed": removed}

        return self.start("destroy", request.name, work)
