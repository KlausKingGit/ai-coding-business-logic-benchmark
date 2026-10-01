# 容器隔离执行｜中文说明

仓库提供 Docker 执行路径，比直接在宿主机执行外部 candidate 提供更强的隔离边界。

## 构建镜像

    docker build -f containers/Dockerfile \
      -t ai-coding-business-logic-benchmark:local .

## 运行外部 Candidate

    scripts/run_candidate_container.sh \
      ./my-agent-output \
      my-agent

可以继续追加 --task、--task-timeout-seconds 等安全 runner 参数。

wrapper 自己管理 candidate/report 路径，因此不允许调用方覆盖 candidate-dir、candidate-name、report-dir、json-report 或 inherit-env。

## 默认隔离参数

运行时默认：

- 禁用 container 网络；
- root filesystem 只读；
- drop 全部 Linux capability；
- no-new-privileges；
- PID 数量限制；
- 内存限制；
- CPU 限制；
- 文件描述符限制；
- 有大小上限的 tmpfs；
- candidate 目录只读挂载；
- report 目录是唯一显式可写的宿主挂载；
- 使用当前宿主 UID/GID，而不是 root 运行。

## 安全边界

这比直接宿主执行更强，但仍不能宣称是“绝对安全 sandbox”。

Linux container 仍共享 host kernel；Docker/runtime 漏洞、kernel 漏洞、side channel 或实现错误仍然可能存在。

对于真正高风险代码，建议进一步使用一次性 VM 或专用 sandbox。
