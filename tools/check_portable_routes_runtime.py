"""Optional real helper acceptance. Downloads pinned binaries; never registers with Cloudflare.

WireGuard packets go only to a UDP socket owned by this test on loopback.
"""
import asyncio
import base64
import socket
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tgwitness.network import NetworkConfig
from tgwitness.portable_routes import PortableRoutes, install_helper, run_helper, runtime_config, wireguard_profile
from tgwitness.security import Vault


async def main():
    root = Path('test-results/portable-route-binaries').resolve()
    for tool in ('wgcf', 'wireproxy'):
        binary = await install_helper(root, tool, allow_download=True)
        await run_helper(binary, ['--help' if tool == 'wgcf' else '-v'], root)
        print(tool + ': pinned hash and executable checked', flush=True)
    binary = await install_helper(root, 'wireproxy')
    with tempfile.TemporaryDirectory() as folder, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer:
        peer.bind(('127.0.0.1', 0))
        key = base64.b64encode(bytes(range(32))).decode()
        text = (f'[Interface]\nPrivateKey = {key}\nAddress = 10.0.0.2/32, fd00::2/128\nDNS = 1.1.1.1\n'
                f'[Peer]\nPublicKey = {key}\nEndpoint = local.test:{peer.getsockname()[1]}\n'
                'AllowedIPs = 0.0.0.0/0, ::/0\n')
        c = SimpleNamespace(vault=Vault(Path(folder)), network_config=lambda: NetworkConfig())
        manager = PortableRoutes(c)
        async def local_config(profile, route):
            with patch('tgwitness.netclient.resolve', AsyncMock(return_value=['1.1.1.1'])):
                config = await runtime_config(wireguard_profile(text), route)
            return config.replace('Endpoint = 1.1.1.1:', 'Endpoint = 127.0.0.1:')
        with patch('tgwitness.portable_routes.install_helper', AsyncMock(return_value=binary)), \
                patch('tgwitness.portable_routes.runtime_config', local_config):
            saved = await manager.prepare('vpn', text, False, lambda _: None)
            process = manager.processes[saved['id']]
            assert process.returncode is None
            port = saved['network']['port']
            print('Authenticated loopback listener started; profile accepted by wireproxy', flush=True)
            # Simulate disappearance of the panel. The worker must reap wireproxy.
            process.stdin.close()
            await asyncio.wait_for(process.wait(), 10)
            try:
                _, writer = await asyncio.open_connection('127.0.0.1', port)
            except OSError:
                pass
            else:
                writer.close()
                raise AssertionError('wireproxy outlived its owning panel pipe')
            await manager.close()
            assert not (manager.root / (saved['id'] + '.conf')).exists()
            print('Parent-pipe closure stopped the tunnel; runtime secrets removed', flush=True)


if __name__ == '__main__':
    asyncio.run(main())
