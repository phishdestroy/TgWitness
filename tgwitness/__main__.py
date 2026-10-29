import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="TgWitness observation journal")
    parser.add_argument("--host", default=os.environ.get("TGWITNESS_HOST", "127.0.0.1"),
                        help="Listen address (default 127.0.0.1, env TGWITNESS_HOST). Expose remotely only behind HTTPS")
    parser.add_argument("--port", type=int, default=os.environ.get("TGWITNESS_PORT", "8787"),
                        help="Listen port (default 8787, env TGWITNESS_PORT)")
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="Data directory (default data/live, or data/demo with --demo; env TGWITNESS_DATA)")
    parser.add_argument("--demo", action="store_true", help="Use a separate synthetic journal; Telegram login disabled")
    parser.add_argument("--check", action="store_true", help="Check local installation, storage, keys and port; do not start")
    parser.add_argument("--json", action="store_true", help="JSON output for --check")
    args = parser.parse_args()
    root = (args.data_dir or Path(os.environ.get("TGWITNESS_DATA", "data/demo" if args.demo else "data/live"))).resolve()
    if args.check:
        from .doctor import inspect_environment, print_report
        report = inspect_environment(root, args.host, args.port)
        print_report(report, args.json)
        raise SystemExit(0 if report["ready"] else 1)
    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535")
    import uvicorn
    from .app import create_app
    from .logging_config import server_logging
    print("TgWitness")
    host = "127.0.0.1" if args.host == "0.0.0.0" else "[" + args.host + "]" if ":" in args.host else args.host
    print("Panel: http://" + host + ":" + str(args.port))
    print("Data directory:", root)
    if args.demo:
        print("Local demo opens without copying a token. Real account authorization is disabled.")
        print("For remote demo access, read", root / "panel-token.txt", "after startup.")
    else:
        print("Panel token: read", root / "panel-token.txt", "after startup (or use TGWITNESS_TOKEN).")
    print("For remote access, place the panel behind HTTPS or use an SSH tunnel.")
    uvicorn.run(create_app(root, demo=args.demo), host=args.host, port=args.port, workers=1,
                access_log=False, log_level="info", log_config=server_logging(root))


if __name__ == "__main__":
    main()
