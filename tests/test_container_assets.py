from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_container_wrapper_declares_core_isolation_flags():
    script = (ROOT / "scripts" / "run_candidate_container.sh").read_text(
        encoding="utf-8"
    )
    for flag in (
        "--network none",
        "--read-only",
        "--cap-drop ALL",
        "--security-opt no-new-privileges:true",
        "--pids-limit 128",
        "--memory 1g",
        "--cpus 1.0",
        "--tmpfs /tmp:",
        "readonly",
    ):
        assert flag in script


def test_container_image_uses_locked_dependencies_and_no_cache_provider():
    dockerfile = (ROOT / "containers" / "Dockerfile").read_text(encoding="utf-8")
    assert "FROM python:3.12.14-slim" in dockerfile
    assert "requirements.lock" in dockerfile
    assert "pip check" in dockerfile
    assert "PYTHONDONTWRITEBYTECODE=1" in dockerfile
    assert "no:cacheprovider" in dockerfile
