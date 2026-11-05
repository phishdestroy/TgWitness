"""Linux container bootstrap: network policy first, then permanently drop privileges."""
import ipaddress
import json
import os
import subprocess
from pathlib import Path

from tgwitness_capture.trusted_runtime import connector_config


def firewall(host, port):
    address = ipaddress.IPv4Address(host)
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("Invalid proxy port")
    return f"""table inet trusted_live {{
 chain output {{
  type filter hook output priority 0; policy drop;
  oifname "lo" accept
  ct state established,related accept
  ip daddr {address} tcp dport {port} accept
 }}
}}
"""


def main():
    config = json.loads(Path("/config.json").read_text())
    options = config["trusted"]
    connectors = connector_config(options["connectors"])
    chosen = os.environ.get("TRUSTED_CONNECTOR", "")
    if chosen not in connectors:
        raise ValueError("Set TRUSTED_CONNECTOR to an explicitly selected configured connector")
    connector = connectors[chosen]
    # A fresh container namespace has no client connections at this point.
    subprocess.run(["nft", "-f", "-"], input=firewall(connector["host"], connector["port"]).encode(), check=True)
    receipt = {"policy": "trusted-live-deny-direct-v1", "host": connector["host"], "port": connector["port"],
               "connector": chosen, "netns": os.readlink("/proc/self/ns/net")}
    Path("/run/trusted-route.json").write_text(json.dumps(receipt))
    os.chmod("/run/trusted-route.json", 0o444)
    for directory in ("/data", "/session", "/exports", "/home/recorder"):
        os.chown(directory, 10001, 10001)
    os.execvp("setpriv", ["setpriv", "--reuid=10001", "--regid=10001", "--init-groups",
                           "--bounding-set=-all", "--inh-caps=-all", "--ambient-caps=-all",
                           "python", "/app/trusted-display.py"])


if __name__ == "__main__":
    main()
