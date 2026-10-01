# Containerized external-candidate execution

The repository provides a Docker execution path with a stronger isolation boundary than running external candidate code directly on the host.

## Build the benchmark image

    docker build -f containers/Dockerfile \
      -t ai-coding-business-logic-benchmark:local .

## Run an external candidate

    scripts/run_candidate_container.sh \
      ./my-agent-output \
      my-agent

Additional safe runner arguments such as repeated --task or --task-timeout-seconds are forwarded.

The wrapper owns candidate/report paths and does not allow callers to override candidate-dir, candidate-name, report-dir, json-report, or inherit-env.

## Runtime restrictions

The wrapper enables:

- no container network;
- read-only container root filesystem;
- all Linux capabilities dropped;
- no-new-privileges;
- PID limit;
- memory limit;
- CPU limit;
- file-descriptor limit;
- bounded tmpfs;
- candidate directory mounted read-only;
- report directory as the only explicit writable host mount;
- execution as the invoking host UID/GID rather than root.

## Security boundary

This is stronger isolation, but it is not a proof of perfect sandboxing.

On Linux, containers still share the host kernel. Docker/daemon/runtime vulnerabilities, kernel vulnerabilities, resource side channels, and implementation mistakes remain possible.

For higher-risk code, prefer a disposable VM or dedicated sandbox in addition to these container restrictions.
