# Bounded CI parallelism

The original `tgwitness-ci` runner executes one job at a time. In the measured
[Checks run](https://github.com/phishdestroy/TgWitness/actions/runs/41331263417),
five jobs took 9m45s end to end. The Docker job ran for 1m36s after waiting 8m07s.
The [Wiki job](https://github.com/phishdestroy/TgWitness/actions/runs/41329432245)
ran for 13s after waiting 12m40s behind the website and application checks.

## Routing

| Runner | Custom labels | Account and access |
| --- | --- | --- |
| Primary | `tgwitness-ci`, `tgwitness-general` | Existing `gha` account and Docker access |
| General | `tgwitness-general` only | Separate `tgwitness-ci-general` account, no Docker or sudo |

The `TGWITNESS_GENERAL_RUNNER` repository variable selects the label for source,
Python, browser and Wiki jobs. Until it is set, these jobs continue to use
`tgwitness-ci`. Set it to `tgwitness-general` only after both runners are healthy.
Docker checks, release publishing jobs and the existing website workflow retain
their original routing. Release validation calls `checks.yml`, so its Linux
source, Python and browser jobs use the selected pool; Windows and macOS jobs
remain GitHub-hosted. Sealed collection, provenance, Scorecard and PR checks
retain their GitHub-hosted runners.

Never give the general runner the `tgwitness-ci` label. Docker jobs currently
use shared image names; keeping them on the single primary runner prevents a
second Docker job from overwriting images during another job's checks. Separate
accounts and work directories prevent accidental sharing of caches, runner
credentials and output. They are not isolation from a compromised primary
account, which already has root-equivalent Docker access. Dispatch workflows
only on reviewed refs. Neither persistent runner may execute untrusted pull
requests.

## Prepare and activate

1. Inspect CPU, RAM, current load and disk space on the actual host. Four CPUs,
   8 GB RAM and sufficient disk headroom are the minimum starting point for two
   concurrent jobs. Do not add multiple copies without measuring contention.
2. Run `scripts/install-ci-general-runner.sh` as root on the existing CI host.
   It verifies the runner download and creates separate user, work and tool-cache
   directories. Existing primary registration and Docker configuration remain intact.
3. Create a short-lived registration token from GitHub's runner registration
   API on the administrator's machine. Pass it privately to `config.sh` as the
   general account, with `--unattended`, the repository URL, a unique runner name,
   `--labels tgwitness-general` and `--work _work`. Do not store a personal GitHub
   token on the server or in repository secrets. Never use shell tracing.
4. Install the new service as `tgwitness-ci-general`. Before starting it, add a
   systemd service drop-in with `UMask=0077`, `NoNewPrivileges=yes`,
   `CPUQuota=200%`, `MemoryHigh=3G`, `MemoryMax=4G`, `MemorySwapMax=0`,
   `TasksMax=1024` and `OOMPolicy=stop`. Adjust limits only after inspecting the
   host's actual capacity. The primary runner must retain RAM and CPU headroom.
5. Confirm that the new account cannot read the primary runner's credentials or
   write its work tree, tool cache or Docker socket. Check that it has no sudo
   privileges. Start the service, confirm its labels and online state in GitHub,
   and add `tgwitness-general` to the primary runner's labels.
6. Set `TGWITNESS_GENERAL_RUNNER=tgwitness-general`. Dispatch normal Linux Checks
   and a Wiki build. Confirm overlapping jobs with different `runner_id` values,
   successful browser/installation checks, and Docker running only on the primary.
   Compare elapsed time and queue time with the recorded baseline; inspect CPU,
   memory pressure and service logs for OOM events before accepting the change.

## Rollback

Delete the `TGWITNESS_GENERAL_RUNNER` repository variable to restore the original
routing for new workflow runs. Let any active general-runner job finish, then
stop its service. Do not unregister or remove its directories during a job.
No sealed or release workflow change is required.
