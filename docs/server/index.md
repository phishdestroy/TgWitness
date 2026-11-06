# Host TgWitness: Telegram Collection Server

Canonical page: https://phishdestroy.github.io/TgWitness/docs/server/

Keep the collector up and the data safe through restarts.

## Choose a launch method

Native: the [launcher](https://phishdestroy.github.io/TgWitness/docs/start/) plus service templates in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, from the project folder:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

The panel listens on localhost:8787. Open it locally or through an SSH tunnel, with the token from the second command.

## Keep the whole data directory

Native: `data/live`. Docker: the `tgwitness-data` volume. Journals, sessions and keys belong together. A signed export is evidence, not a backup.

1. Stop collecting first.
2. Copy the whole data directory somewhere safe, off the host.
3. Try restoring it on a separate install before you trust it.

## Check after a restart

Check the workspace and key, the connection, sources and that new messages come in. TgWitness catches up what Telegram still has, not everything that happened while it was down.

"Healthy" container means the web server answers. Whether collection works, a test message and the witness will tell.

## Publish only what you intend

HTTPS, volumes, updates and restore are in the deployment reference. What's actually been tested: [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).
