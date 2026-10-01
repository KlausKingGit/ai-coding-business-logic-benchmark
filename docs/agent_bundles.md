# Provider-neutral agent bundles

The benchmark can export a self-contained task handoff for coding agents.

    python -m evaluator.agent_bundle --output-dir ./agent-bundle

The generated prompts contain the public task contract and expected candidate filename, but intentionally omit repository reference/flawed implementations.

This keeps the benchmark usable with different agents without baking vendor-specific APIs, authentication, or network dependencies into the evaluation core.

After the agent writes its implementations into candidate/, evaluate them with the normal external-candidate runner.

The machine-readable bundle contract is documented by schemas/agent_bundle.schema.json.
