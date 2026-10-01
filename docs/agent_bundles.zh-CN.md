# Provider-neutral Agent Bundle｜中文说明

benchmark 可以导出一个独立的 coding-agent 任务包：

    python -m evaluator.agent_bundle --output-dir ./agent-bundle

生成的 prompt 会包含：

- 公开 task contract；
- 目标 candidate 文件名；
- 离线/范围约束。

但不会包含：

- reference implementation；
- flawed implementation。

这样可以让不同 Agent 使用同一份任务 contract，而不把 benchmark 核心绑定到某一家 API、认证或网络服务。

Agent 将实现写入 candidate/ 后，直接使用已有 external-candidate runner 进行评测。

机器可读 bundle contract 位于 schemas/agent_bundle.schema.json。
