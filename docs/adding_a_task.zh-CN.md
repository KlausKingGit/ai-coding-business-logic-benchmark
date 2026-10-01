# 添加一个 Task｜中文说明

好的 benchmark task 应该足够小，让读者快速理解；同时足够尖锐，能够区分“看起来合理”和“真正正确”的代码。

## 1. 先选择一个业务不变量

从具体失败模式出发，例如：

- 相同 retry 必须返回第一次的原始 response；
- 外部写入 outcome 未知时不能盲目重试；
- authorization 必须发生在 mutation 之前；
- stale version 不能覆盖更新后的状态。

不要从“实现一个完整生产支付系统”这种大任务开始。

## 2. 选择下一个稳定 ID

使用：

`task_NN_short_slug`

已经存在或已经发布的 ID 不复用、不重新编号。

## 3. 创建标准文件

```text
tasks/task_NN_short_slug/
  README.md
  task.json
  reference_solution.py
  flawed_candidate.py
  evaluation_notes.md
  tests/test_cases.py
```

## 4. 两个 candidate 都必须有信息量

reference 应尽量简洁，不需要展示复杂架构。

flawed candidate 应该“合理但错在关键点”。理想情况下，它能通过 happy path 和一些 edge cases，但漏掉目标 invariant。

## 5. 写有区分度的测试

至少一个测试必须因为 task 描述中的目标缺陷而让 flawed candidate 失败。

测试必须确定、离线、可复现。

## 6. 添加 metadata 并注册

复制一个已有 task 的 `task.json` 结构，然后把新 task 添加到 `benchmark.json`。

## 7. 验证

```bash
python -m evaluator.manifest
python -m pytest -q
python evaluator/runner.py --candidate reference --task task_NN_short_slug
python evaluator/runner.py --candidate flawed --task task_NN_short_slug
```

reference 必须全 PASS。flawed candidate 的评测过程本身应正常完成，并触发目标失败。

## 8. 说明历史可比性

如果你修改的是已有 task 而不是新增 task，需要解释旧 benchmark 结果是否仍可与新结果比较。
