from evaluator.manifest import REQUIRED_TASK_FILES, load_benchmark

def test_manifest_loads_all_registered_tasks():
    benchmark, tasks = load_benchmark()
    assert benchmark["schema_version"] == "1.0"
    assert benchmark["benchmark_version"] == "0.3.0"
    assert len(tasks) == 10
    assert len({task.id for task in tasks}) == len(tasks)

def test_task_metadata_and_files_are_consistent():
    _, tasks = load_benchmark()
    for task in tasks:
        assert task.metadata["id"] == task.id
        assert task.metadata["title"] == task.title
        assert task.metadata["expected"]["reference"] == "pass_all"
        assert task.metadata["expected"]["flawed"] == "fail_at_least_one"
        for relative in REQUIRED_TASK_FILES:
            assert (task.path / relative).is_file()
