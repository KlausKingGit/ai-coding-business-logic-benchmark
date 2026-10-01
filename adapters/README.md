# Agent adapters

The benchmark deliberately keeps its core agent integration provider-neutral.

Instead of embedding vendor SDKs or API keys, it exports a stable task bundle that can be consumed by Codex, Claude Code, local coding agents, CI-driven agents, or custom automation.

Generate a bundle:

    python -m evaluator.agent_bundle --output-dir ./agent-bundle

Or export selected tasks:

    python -m evaluator.agent_bundle --output-dir ./agent-bundle \
      --task task_08_optimistic_concurrency \
      --task task_10_unknown_write_outcome

Each bundle contains:

- bundle.json — machine-readable task/output mapping;
- prompts/*.md — one provider-neutral task prompt per selected task;
- candidate/ — destination for generated Python implementations;
- README.md — execution handoff.

The bundle does not contain reference or flawed implementation source.

Provider-specific wrappers may be added later as thin layers on top of this contract. The benchmark core should not require a particular vendor, account, or network service.
