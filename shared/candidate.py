"""Select the candidate implementation used by task tests."""
from __future__ import annotations

import importlib
import importlib.util
import os
from pathlib import Path
import re
import sys
from types import ModuleType

TASK_ID = re.compile(r"^task_\d{2}_[a-z0-9_]+$")


def _load_external(task: str) -> ModuleType:
    if not TASK_ID.fullmatch(task):
        raise ValueError(f"invalid task id: {task!r}")

    raw_dir = os.environ.get("EVAL_CANDIDATE_DIR")
    if not raw_dir:
        raise ValueError("EVAL_CANDIDATE_DIR is required for external candidates")

    candidate_dir = Path(raw_dir).expanduser().resolve()
    if not candidate_dir.is_dir():
        raise FileNotFoundError(f"external candidate directory not found: {candidate_dir}")

    path = candidate_dir / f"{task}.py"
    if not path.is_file():
        raise FileNotFoundError(f"external candidate file not found: {path}")

    module_name = f"_benchmark_external_{task}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load external candidate module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(module_name, None)
        raise
    return module


def load(task: str) -> ModuleType:
    candidate = os.environ.get("EVAL_CANDIDATE", "reference")
    if candidate == "external":
        return _load_external(task)
    if candidate not in {"reference", "flawed", "bad"}:
        raise ValueError("EVAL_CANDIDATE must be reference, flawed, bad, or external")
    module = "reference_solution" if candidate == "reference" else "flawed_candidate"
    return importlib.import_module(f"tasks.{task}.{module}")
