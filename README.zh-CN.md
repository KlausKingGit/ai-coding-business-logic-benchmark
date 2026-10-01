# AI Coding Business-Logic Benchmark｜中文说明

这是一个小型、可复现的开源评测基准，用来检查 **AI 生成的 Python 代码是否真正保持后端业务规则**，而不只是“代码能运行”。

当前 benchmark version：**0.2.0**。仓库保留 10 个 canonical task；v0.2 只增强评测 harness、可复现性、结果格式、fixture 质量门和安全边界，不删除 task，也不弱化已有测试。

## 快速开始

需要 Python 3.11+。如果希望复现持续验证的 CI 环境，优先使用 lock snapshot：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip check

python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

`requirements.txt` 继续保留兼容版本范围；`requirements.lock` 用于复现 Python 3.11/3.12 CI 的精确解析结果。

详见：[可复现环境](docs/reproducibility.zh-CN.md)。

## 评测你自己的 AI-generated code

准备一个目录，每个 task 放一个同名 Python 文件：

```text
my-agent-output/
  task_01_order_api.py
  ...
  task_10_unknown_write_outcome.py
```

然后运行：

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --json-report reports/my-agent.json
```

可以用多个 `--task` 只评测选定任务。

详见：

- [外部 Candidate](docs/external_candidates.zh-CN.md)
- [JSON 结果](docs/results.zh-CN.md)

## 安全提醒

**外部 candidate 会被当作 Python 代码执行。**

runner 默认：

- 不把宿主机完整环境变量传给外部 candidate；
- 每个 task 设置 30 秒 timeout。

但这**不是完整 sandbox**。第三方或来源未知代码应在一次性 container、VM、受限制 CI worker 或专用 sandbox 中运行。

详见：[安全执行说明](docs/safe_execution.zh-CN.md) 与 [SECURITY.zh-CN.md](SECURITY.zh-CN.md)。

## 使用 Docker 提高隔离强度

对于不可信 external candidate，可以使用仓库提供的容器执行路径：

    docker build -f containers/Dockerfile -t ai-coding-business-logic-benchmark:local .
    scripts/run_candidate_container.sh ./my-agent-output my-agent

wrapper 默认禁网、只读 root filesystem、drop capabilities、no-new-privileges、资源限制，并把 candidate 只读挂载。

详见：[容器隔离执行](docs/container_execution.zh-CN.md)。

## 当前 10 个任务

| Task | 核心业务不变量 |
|---|---|
| `task_01_order_api` | 重复订单不能覆盖已经存储的状态 |
| `task_02_payment_reconciliation` | 重复 payment ID 不能被重复计入 |
| `task_03_user_quota` | 相同重试必须返回第一次的原始结果 |
| `task_04_webhook_idempotency` | 处理失败的 webhook 必须仍然可以重试 |
| `task_05_ai_summary_validation` | 结构化输出必须和输入事实一致 |
| `task_06_inventory_move_atomicity` | 后续记录失败时不能留下半完成库存变更 |
| `task_07_document_authorization` | 未授权请求不能先修改状态再报错 |
| `task_08_optimistic_concurrency` | stale version 不能覆盖更新后的状态 |
| `task_09_api_contract_drift` | API 变化不能破坏已有客户端依赖的兼容保证 |
| `task_10_unknown_write_outcome` | 写入结果未知时不能因为超时而自动重试 |

## Fixture 质量

reference 必须全 PASS。

flawed candidate 不是“故意写烂的代码”，而应该在大量正常路径上表现合理，同时稳定暴露目标业务缺陷。

`fixture_expectations.json` 冻结了：

- 每个 flawed fixture 的最低通过数量；
- 必须继续失败的目标测试。

CI 会自动验证。

详见：[Fixture 质量门](docs/fixture_quality.zh-CN.md)。

## Benchmark 设计原则

1. **窄而清晰**：一个 task 聚焦一个或少数紧密相关的业务不变量。
2. **可复现**：默认离线运行，不依赖真实账号、密钥、线上 API 或时间敏感数据。
3. **可区分**：reference 全 PASS；flawed 合理但在关键 invariant 上失败。
4. **不夸大能力**：通过测试不等于生产可用、安全、性能优秀或架构合理。
5. **历史可比较**：已经发布的 task ID 不重新编号，影响可比性的变更必须说明。

## 如何贡献

- [中文贡献指南](CONTRIBUTING.zh-CN.md)
- [中文添加 Task 指南](docs/adding_a_task.zh-CN.md)
- [中文 Benchmark Contract](docs/benchmark_contract.zh-CN.md)

## License

MIT License。详见 [LICENSE](LICENSE)。

英文主文档：[README.md](README.md)
