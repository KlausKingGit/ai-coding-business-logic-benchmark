# 评测外部 Candidate｜中文说明

benchmark 现在可以直接评测仓库之外生成的代码，不需要修改已有 10 个 canonical task 或它们的测试。

## Candidate 目录结构

每个 task 提供一个同名 Python 文件：

```text
my-agent-output/
  task_01_order_api.py
  task_02_payment_reconciliation.py
  task_03_user_quota.py
  task_04_webhook_idempotency.py
  task_05_ai_summary_validation.py
  task_06_inventory_move_atomicity.py
  task_07_document_authorization.py
  task_08_optimistic_concurrency.py
  task_09_api_contract_drift.py
  task_10_unknown_write_outcome.py
```

每个文件需要暴露该 task 原有测试所使用的公开函数或 class。

具体接口以对应 task 的 README、测试和 reference implementation 为准。

## 全量运行

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent
```

## 只运行部分 Task

使用 `--task` 时，只需要提供被选中的 candidate 文件：

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --task task_08_optimistic_concurrency
```

可以重复传入 `--task` 来选择多个任务。

## 结果语义

测试 assertion 失败属于“评测结果”，本身不代表 runner 运行失败。

以下情况会使 runner 返回非零：

- candidate 文件无法加载；
- pytest collection / execution 发生基础设施错误；
- 没有得到有效测试结果。

外部 candidate 功能不会改变 canonical task、reference、flawed fixture 或已有测试的语义。
