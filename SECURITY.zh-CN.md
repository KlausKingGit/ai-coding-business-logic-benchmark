# 安全说明｜中文

这个仓库包含离线 benchmark fixtures 和 evaluation harness，**不是生产服务**。

## 外部 Candidate 就是可执行代码

使用 `--candidate-dir` 时，runner 会 import 并执行外部提供的 Python。

除非你已经审查过，否则应把 AI-generated code 或第三方 candidate 当作**不可信代码**。

runner 默认提供两层有限保护：

- 外部 candidate 不会自动继承宿主机全部环境变量，而是使用清理后的环境；
- 每个 task 默认有 30 秒 pytest timeout。

这两项能降低误泄露和无限挂起风险，但**它们不是 sandbox**。

外部代码仍可能尝试：

- 读取当前 OS 用户有权限访问的文件；
- 写入当前用户有权限写入的位置；
- 消耗 CPU / 内存；
- 在宿主网络允许时访问网络；
- 启动子进程。

如果代码来源不可信，建议在不包含敏感数据/凭据的一次性容器、VM、CI job 或其他 sandbox 中运行。

只有在你明确知道 candidate 需要某个环境变量时才使用：

`--inherit-env NAME`

这意味着你主动允许 candidate 读取该变量的值。

## 仓库内容安全

不要在 issue、candidate fixture 或 PR 中提交：

- 密钥；
- 客户数据；
- 私有源码；
- proprietary prompt；
- 生产环境 endpoint。

## 报告安全问题

如果发现 benchmark tooling 可能导致意外代码执行、secret 泄露、隔离边界逃逸或影响贡献者运行环境，请优先使用 GitHub private vulnerability reporting / security advisory。

如果不可用，请私下联系维护者，不要直接公开 exploit 细节。

## 容器隔离路径

需要更强隔离时，请使用 docs/container_execution.zh-CN.md 中的 Docker 路径。

wrapper 会禁网、使用只读 root filesystem、drop Linux capabilities、启用 no-new-privileges、设置资源限制，并把 candidate 目录只读挂载。

这仍然不是“绝对安全 sandbox”。Linux container 共享 host kernel，container/runtime/kernel 漏洞不属于 benchmark 能保证的范围。
