# Benchmark Contract｜中文说明

这个 benchmark 的核心是：**确定性证据、稳定 task identity、明确能力边界**。

## Task identity

已经发布的 task ID 是稳定的，不因为目录排序或美观重新编号。

`benchmark.json` 中的顺序是 canonical order。

## Candidate 角色

每个 task 至少包含仓库提供的两个 candidate：

- **reference**：应通过该 task 的全部测试；
- **flawed**：故意保留一个现实、合理、可识别的缺陷，并至少失败一个目标测试。

flawed candidate 不应该“故意写得很烂”。如果它所有正常路径都失败，就不能很好地模拟真实 AI-generated code 的问题。

## 测试契约

测试优先验证对外可观察的业务不变量，而不是内部实现细节。

例如：

- 重复请求是否修改了已有状态？
- retry 是否返回第一次生成的原始结果？
- webhook 处理失败后是否被错误标记成永久完成？
- 结构化输出是否引入了源数据中不存在的事实？

除非内部结构本身属于 task contract，否则不应该要求某个固定 class layout。

## 默认离线与确定性

默认 task 不依赖：

- 网络；
- live API；
- 外部账号；
- credential；
- 时间敏感数据。

如果未来某个 task 确实需要不同执行模型，应显式修改 benchmark contract，而不是偷偷放宽规则。

## 评分

默认评分为：

`round(100 × passed / (passed + failed))`

测试 collection / execution error 会使运行无效。

这个分数**不代表**：

- 可读性；
- 生产安全性；
- 性能；
- 架构质量；
- 没有被测试覆盖的其他语义。

## 版本

`benchmark_version` 按 SemVer 意图管理：

- patch：不故意改变 benchmark outcome 的文档/基础设施更新；
- minor：新增 task 或向后兼容的 evaluator 功能；
- major：不兼容的 task 语义、评分规则或 manifest contract 变化。

即使 1.0 之前，也应明确记录兼容性变化。

## 历史可比性

任何导致旧结果与新结果不可直接比较的变化，都必须说明。

不要静默修改 task 核心不变量，然后继续把旧分数和新分数当作同一个 benchmark。
