"""Select the candidate implementation used by task tests."""
import importlib
import os
from types import ModuleType

def load(task: str) -> ModuleType:
    candidate = os.environ.get("EVAL_CANDIDATE", "reference")
    if candidate not in {"reference", "flawed", "bad"}:
        raise ValueError("EVAL_CANDIDATE must be reference, flawed, or bad")
    module = "reference_solution" if candidate == "reference" else "flawed_candidate"
    return importlib.import_module(f"tasks.{task}.{module}")
