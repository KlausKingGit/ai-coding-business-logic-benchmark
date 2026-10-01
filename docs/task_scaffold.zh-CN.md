# Task Scaffold｜中文说明

可以生成一个尚未注册的 task 起始目录：

    python -m evaluator.scaffold \
      --output-dir /tmp/task_11_pagination_cursor \
      --task-id task_11_pagination_cursor \
      --title "Pagination cursor" \
      --summary "Preserve cursor progression without skipping or duplicating items." \
      --area pagination \
      --tag pagination \
      --tag cursor

脚手架会生成：

- 标准 task 文件结构；
- task.json；
- README；
- reference/flawed 占位文件；
- evaluation notes；
- 一个故意失败的 placeholder test；
- fixture quality expectation 示例。

它不会自动修改 benchmark.json，也不会自动写入 fixture_expectations.json。

这是刻意的安全边界：脚手架只是草稿，不应该因为“文件生成成功”就自动变成 canonical benchmark task。
