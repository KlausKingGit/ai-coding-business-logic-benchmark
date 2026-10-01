from evaluator.fixture_check import validate_fixture_results


TASKS = ["task_01_example"]
EXPECTATIONS = {
    "schema_version": "1.0",
    "tasks": {
        "task_01_example": {
            "minimum_passed": 3,
            "must_fail_tests": ["test_target_defect"],
        }
    },
}


def report(*, passed, failed, errors=0, failed_tests=None):
    return {
        "tasks": [
            {
                "id": "task_01_example",
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "score": 75,
                "failed_tests": failed_tests or [],
            }
        ]
    }


def test_fixture_quality_accepts_plausible_targeted_flaw():
    problems = validate_fixture_results(
        task_ids=TASKS,
        expectations=EXPECTATIONS,
        reference_payload=report(passed=4, failed=0),
        flawed_payload=report(
            passed=3,
            failed=1,
            failed_tests=["test_target_defect"],
        ),
    )
    assert problems == []


def test_fixture_quality_rejects_overly_broken_flaw():
    problems = validate_fixture_results(
        task_ids=TASKS,
        expectations=EXPECTATIONS,
        reference_payload=report(passed=4, failed=0),
        flawed_payload=report(
            passed=1,
            failed=3,
            failed_tests=["test_target_defect"],
        ),
    )
    assert any("expected at least 3" in problem for problem in problems)


def test_fixture_quality_rejects_missing_target_failure():
    problems = validate_fixture_results(
        task_ids=TASKS,
        expectations=EXPECTATIONS,
        reference_payload=report(passed=4, failed=0),
        flawed_payload=report(
            passed=3,
            failed=1,
            failed_tests=["test_other_failure"],
        ),
    )
    assert any("target defect no longer exposed" in problem for problem in problems)


def test_fixture_quality_rejects_reference_regression():
    problems = validate_fixture_results(
        task_ids=TASKS,
        expectations=EXPECTATIONS,
        reference_payload=report(passed=3, failed=1, failed_tests=["test_regression"]),
        flawed_payload=report(
            passed=3,
            failed=1,
            failed_tests=["test_target_defect"],
        ),
    )
    assert any("reference fixture must pass all tests" in problem for problem in problems)
