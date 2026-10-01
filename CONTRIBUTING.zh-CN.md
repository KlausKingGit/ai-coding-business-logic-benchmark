# 贡献指南｜中文

欢迎任何能让这个 benchmark **更可复现、更有区分度、更容易维护** 的贡献。

## 适合的贡献

例如：

- 围绕一个明确业务不变量新增 task；
- 增加能够识别“看起来正确但实际错误”实现的测试；
- 修复 evaluator / manifest / CI / 文档问题；
- 消除任务契约歧义，同时不静默改变原本的 benchmark 语义。

如果是较大的新 task，建议先开一个 **Task proposal** issue。

## 新 Task 的基本要求

一个可接受的 task 应当：

1. 使用稳定 ID，例如 `task_11_pagination_cursor`；
2. 聚焦一个或少数紧密相关的业务不变量；
3. 默认离线运行，不依赖账号、密钥、付费 API 或网络；
4. 提供 reference implementation，并通过全部测试；
5. 提供 deliberately flawed implementation，它应当合理、可运行，并通过至少一个有意义路径；
6. 测试必须确定性地暴露目标缺陷；
7. 明确记录 known limits，不夸大成生产可用系统；
8. 使用标准 `task.json` metadata；
9. 正常 CI 时间内完成；
10. 只使用虚构或允许再分发的数据。

已经发布的 task ID 不重新编号。

## Pull Request

如果改动会影响 benchmark 结果，请说明：

- 哪个业务不变量发生了变化；
- 为什么旧行为不足或存在歧义；
- 历史结果是否仍然可比较；
- benchmark version 是否需要升级。

提交前建议运行：

```bash
python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

## License

提交贡献即表示你同意该贡献按照本仓库的 MIT License 发布。

英文版本：[CONTRIBUTING.md](CONTRIBUTING.md)
