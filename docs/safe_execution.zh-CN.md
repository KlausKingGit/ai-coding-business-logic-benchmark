# 外部 Candidate 的安全执行｜中文说明

外部 candidate 是 Python 程序，因此“进行评测”本质上就是**执行代码**。

## Runner 默认保护

使用 `--candidate-dir` 时：

1. pytest 子进程使用清理后的环境，不直接继承宿主机全部环境变量；
2. 每个 task 默认最多运行 30 秒，可以用 `--task-timeout-seconds` 调整。

如果确实需要向 candidate 显式传递某个宿主环境变量，可以：

```bash
python evaluator/runner.py \
  --candidate-dir ./candidate \
  --inherit-env MY_PUBLIC_SETTING
```

benchmark 自己使用的控制变量不能通过这个参数覆盖。

## 这些保护不等于 Sandbox

当前 runner **不会**提供完整安全隔离，例如：

- 文件系统隔离；
- 网络隔离；
- 内存限制；
- 完整 CPU quota；
- syscall filtering；
- 子进程树隔离。

对于真正不可信的代码，请使用外部隔离边界，例如：

- 一次性 container；
- VM；
- 受限制的 CI worker；
- 专用 sandbox。

并且不要把 secret 或私人数据放入该运行环境。

## 建议的信任模型

- 仓库自带 reference/flawed：项目可信 fixture；
- 你自己生成并审查过的代码：按自己的风险容忍度运行；
- 第三方或来源未知的 candidate：先隔离，再评测。
