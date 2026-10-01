# Agent Adapter｜中文说明

benchmark 的核心 Agent 集成保持 provider-neutral。

也就是说，不在核心仓库里绑定某一家 SDK、API key 或账号，而是导出稳定的 task bundle。Codex、Claude Code、本地 coding agent、CI agent 或自定义自动化都可以消费同一个 bundle。

生成全量 bundle：

    python -m evaluator.agent_bundle --output-dir ./agent-bundle

只导出部分 task：

    python -m evaluator.agent_bundle --output-dir ./agent-bundle \
      --task task_08_optimistic_concurrency \
      --task task_10_unknown_write_outcome

bundle 包含：

- bundle.json：机器可读的 task / output 映射；
- prompts/*.md：每个 task 一个 provider-neutral prompt；
- candidate/：Agent 应写入生成代码的位置；
- README.md：运行交接说明。

bundle 不会包含 reference/flawed implementation 源码。

以后如果增加 Codex / Claude Code 等特定 wrapper，它们应该只是建立在这个稳定 contract 上的薄适配层，而不是让 benchmark 本身依赖某一家服务。
