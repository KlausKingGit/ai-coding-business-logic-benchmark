# AI Coding Business-Logic Benchmark｜中文说明

这是一个小型、可复现的开源评测基准，用来检查 **AI 生成的 Python 代码是否真正保持后端业务规则**，而不只是“代码能运行”。

项目最初来自 5 个 AI Coding 评测任务，目前已经演化为一个可以被他人运行、扩展、审查和维护的 OSS benchmark。

## 这个 benchmark 测什么

当前 10 个任务覆盖一组很常见、也很容易被“看起来正确”的代码漏掉的业务约束：

- 重复写入保护与 API 错误语义；
- 支付对账、去重与精确金额处理；
- 幂等重试必须返回原始结果；
- Webhook 的可重试性与失败原子性；
- 结构化 AI 输出与源数据一致性；
- 多步状态变更失败时必须保持原子性；
- 授权检查必须发生在写入之前；
- 旧版本状态不能覆盖新状态；
- API 改动不能静默破坏已有客户端契约；
- 外部写入结果未知时不能盲目重试。

每个 task 都包含：

- 面向人的任务契约说明；
- reference implementation；
- 一个“合理但有关键缺陷”的 flawed candidate；
- 两者共用的 pytest 测试；
- 人工 review notes；
- 机器可读的 `task.json` metadata。

## 快速开始

需要 Python 3.11+。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --list-tasks
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

只运行单个 task：

```bash
python evaluator/runner.py --candidate flawed --task task_10_unknown_write_outcome
```

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

## Benchmark 设计原则

这个项目不是为了把题目数量堆大，而是希望每个任务都满足：

1. **窄而清晰**：一个 task 聚焦一个或少数紧密相关的业务不变量。
2. **可复现**：默认离线运行，不依赖真实账号、密钥、线上 API 或时间敏感数据。
3. **可区分**：reference 必须通过全部测试；flawed candidate 应该看起来合理，但会被关键测试识别。
4. **不夸大能力**：通过测试不等于生产可用、安全、性能优秀或架构合理。
5. **历史可比较**：已经发布的 task ID 不重新编号，任何影响结果可比性的变更都必须说明。

详细规则参见：[中文 Benchmark Contract](docs/benchmark_contract.zh-CN.md)。

## 如何贡献

如果你想新增 task，建议先阅读：

- [中文贡献指南](CONTRIBUTING.zh-CN.md)
- [中文添加 Task 指南](docs/adding_a_task.zh-CN.md)

核心原则是：不要提交一个“大型完整系统题”，而应从一个具体、可测试的业务失败模式出发。

## 评分

默认 runner 使用：

`round(100 × passed / (passed + failed))`

这个分数只表示当前测试观测到的结果。测试收集或执行错误会使本次运行无效。

## 已知边界

为了让业务不变量更容易阅读和复现，部分 task 使用内存状态或模拟失败。因此它们不声称具备：

- 跨进程持久化保证；
- 分布式事务；
- 真实 webhook 身份验证；
- 完整生产 IAM；
- 对自由文本 LLM 输出的全面事实核验。

## License

MIT License。详见 [LICENSE](LICENSE)。

---

英文主文档：[README.md](README.md)
