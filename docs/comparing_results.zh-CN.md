# 结果对比与历史运行｜中文说明

v0.3 tooling 可以直接消费已有 JSON report，不需要重新执行 candidate。

## 对比两次结果

```bash
python -m evaluator.compare \
  reports/baseline.json \
  reports/candidate.json \
  --markdown-output reports/comparison.md \
  --json-output reports/comparison.json
```

会输出：

- 总 score 差异；
- passed / failed / errors 差异；
- 每个 task 的 score delta。

## 汇总历史运行

可以传入多个 JSON，也可以直接传一个包含 JSON report 的目录：

```bash
python -m evaluator.history reports/history \
  --markdown-output reports/history.md \
  --json-output reports/history.json
```

## 可比性保护

默认情况下，如果以下任意条件不同，工具会拒绝比较：

- benchmark id；
- benchmark version；
- 实际评测 task 集合。

如果某次运行包含 infrastructure / execution error，也会拒绝当作有效历史结果比较。

这样可以避免为了方便展示而把本来不可比较的结果硬放在同一张表里。
