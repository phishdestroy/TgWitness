# Keep it running

Canonical page: https://phishdestroy.github.io/TgWitness/docs/server/

Keep the collector available and its data intact across restarts.

## Choose a launch method

For a native installation, use the [launcher](https://phishdestroy.github.io/TgWitness/docs/start/) and the service examples in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). For Docker, install Docker with Compose and run from the project directory:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

The default panel listens on the host’s loopback address, port 8787. Open it locally or through an SSH tunnel. Use the token from the second command to unlock the panel.

## Keep the whole data directory

Native installations use `data/live`. Docker uses the persistent `tgwitness-data` volume. Keep journals, account sessions, keys and operational state together. A signed export is useful evidence, but it is not a full installation backup.

1. Stop collection before taking a consistent backup.
2. Copy the full private data directory to protected storage outside the host.
3. Test restoration into an isolated installation before relying on the backup.

## Check after a restart

Confirm the expected workspace and key, Telegram connection, selected sources and new message capture. Saved MTProto state and catch-up help recover updates that Telegram still retains. They cannot reconstruct every expired update or an edit deleted before capture.

Container health means the web server responds. Use a controlled message and a witness check to assess collection and external publication.

## Publish only what you intend

The deployment reference includes HTTPS examples, persistent-volume commands, updates and restore steps. Docker commands are provided for deployment; the current [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) identifies the environments actually tested.
