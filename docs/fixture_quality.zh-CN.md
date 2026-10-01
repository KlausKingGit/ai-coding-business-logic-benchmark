# Fixture 质量门｜中文说明

仓库中的 flawed candidate 不是为了“故意写一份很差的代码”，而是为了模拟：

> **大部分路径看起来合理，但在一个关键业务不变量上出错。**

## 冻结的质量预期

`fixture_expectations.json` 为每个 canonical task 记录：

- flawed candidate 至少要继续通过多少测试；
- 哪些目标测试必须继续失败，因为这些测试正是该 task 要暴露的核心缺陷。

同时 reference candidate 必须继续全 PASS。

## CI 如何验证

CI 只运行一次 reference / flawed，然后输出 JSON，再执行：

```bash
python -m evaluator.fixture_check \
  --reference-json reference.json \
  --flawed-json flawed.json
```

它能发现两类重要退化：

1. flawed fixture 变得过于破碎，已经不像“合理但有缺陷”的 AI-generated code；
2. flawed fixture 意外修复了目标缺陷，导致 task 不再真正测试原本的业务不变量。

质量预期被单独放在 `fixture_expectations.json`，因此不需要破坏 v0.1 已发布的 `task.json` metadata contract。
