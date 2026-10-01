# 机器可读结果｜中文说明

runner 可以在原有 Markdown report 之外额外输出 JSON：

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --json-report reports/my-agent.json
```

## JSON 内容

当前格式使用：

`schema_version: "1.0"`

主要包含：

- benchmark id / version；
- candidate mode / name；
- Python/runtime 环境信息；
- 总 passed / failed / errors / score；
- 每个 task 的结构化结果；
- failed test identifier。

JSON 适合：

- CI 自动消费；
- 比较多个 Agent；
- 保存历史评测结果；
- 后续制作 dashboard / leaderboard；
- 让其他工具或 Agent 读取 benchmark 结果。

注意：`failed > 0` 是正常的评测结果，并不等于 runner 出错。collection / execution infrastructure error 会被单独记录，并使 runner 返回非零。
