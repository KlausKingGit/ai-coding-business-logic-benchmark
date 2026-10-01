#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 CANDIDATE_DIR CANDIDATE_NAME [runner args...]" >&2
  echo "example: $0 ./candidate my-agent --task task_08_optimistic_concurrency" >&2
}

if [[ $# -lt 2 ]]; then
  usage
  exit 2
fi

candidate_input=$1
candidate_name=$2
shift 2

for arg in "$@"; do
  case "$arg" in
    --candidate-dir|--candidate-dir=*|--candidate-name|--candidate-name=*|--report-dir|--report-dir=*|--json-report|--json-report=*|--inherit-env|--inherit-env=*)
      echo "error: $arg is managed by the container wrapper" >&2
      exit 2
      ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker is required" >&2
  exit 2
fi

if [[ ! -d "$candidate_input" ]]; then
  echo "error: candidate directory not found: $candidate_input" >&2
  exit 2
fi

candidate_abs=$(cd "$candidate_input" && pwd -P)
repo_root=$(cd "$(dirname "$0")/.." && pwd -P)
safe_name=$(printf '%s' "$candidate_name" | tr -c 'A-Za-z0-9._-' '-')
safe_name=${safe_name#-}
safe_name=${safe_name%-}
if [[ -z "$safe_name" ]]; then
  safe_name=external
fi

report_input=${REPORT_DIR:-"$repo_root/reports/container-$safe_name"}
mkdir -p "$report_input"
report_abs=$(cd "$report_input" && pwd -P)

image=${BENCHMARK_IMAGE:-ai-coding-business-logic-benchmark:local}
if ! docker image inspect "$image" >/dev/null 2>&1; then
  echo "error: container image not found: $image" >&2
  echo "build it with: docker build -f containers/Dockerfile -t $image ." >&2
  exit 2
fi

docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --pids-limit 128 \
  --memory 1g \
  --cpus 1.0 \
  --ulimit nofile=256:256 \
  --tmpfs /tmp:rw,nosuid,nodev,noexec,size=256m \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$candidate_abs,dst=/candidate,readonly" \
  --mount "type=bind,src=$report_abs,dst=/reports" \
  "$image" \
  --candidate-dir /candidate \
  --candidate-name "$candidate_name" \
  --report-dir /reports \
  --json-report /reports/result.json \
  "$@"
