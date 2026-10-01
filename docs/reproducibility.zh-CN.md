# 可复现环境｜中文说明

仓库同时保留两种依赖视图，它们用途不同。

## 兼容范围

`requirements.txt` 是面向维护者的兼容范围声明，表示项目希望支持的依赖版本区间。

## 已验证的 Lock Snapshot

`requirements.lock` 保存 GitHub Actions 实际验证通过的精确依赖集合。

复现 CI 环境时使用：

```bash
python -m pip install -r requirements.lock
python -m pip check
```

`environment.snapshot.json` 另外记录：

- CI provider；
- runner image；
- Python patch version；
- snapshot 捕获时间；
- Python 版本相关的 NumPy 实际解析结果。

## 为什么 NumPy 使用环境 marker

本次成功 CI 中：

- Python 3.11.16 → NumPy 2.4.6
- Python 3.12.14 → NumPy 2.5.3

因此 lock 文件保留真实验证结果，而不是假设所有 Python minor version 都使用同一个 NumPy wheel。

## 可复现边界

目前 lock snapshot 只承诺 Python 3.11 / 3.12，因为这两个版本持续经过 CI 验证。

未来如果支持新的 Python minor version，应先加入 CI，通过后再生成新的环境 snapshot。

依赖锁定不能静默改变 task 的业务不变量，也不能破坏历史 benchmark 结果的可比性。
