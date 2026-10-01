# Architecture

The system applies one hard boundary: probabilistic language understanding may propose a **known intent label**, but it may not choose a device, action, or parameter.

```mermaid
flowchart LR
    U[Chinese user request] --> N[Normalize text]
    N --> R{High-precision rules}
    R -->|matched| I[Known intent]
    R -->|unknown and configured| L[Constrained LLM classifier]
    L --> I
    I --> P[Deterministic command planner]
    P --> W[47-device allowlist]
    W --> C[Capability and parameter checks]
    C --> H{High-risk action?}
    H -->|yes| X[Explicit confirmation]
    H -->|no| E[Simulated executor]
    X --> E
    E --> A[Append-only audit log]
```

## Trust boundaries

| Boundary | Input | Output | Failure behavior |
| --- | --- | --- | --- |
| Rule classifier | Free text | Known intent | Returns `unknown` |
| Optional LLM | Free text | One enum label | Invalid/error becomes `unknown` |
| Planner | Known intent | Allowlisted logical commands | Unknown intent yields no commands |
| Safety interlock | Commands | Findings and risk | Errors reject; high risk waits |
| Executor | Validated commands | Simulated state | Never receives unvalidated plans |

## Adding a real integration

Implement a new executor behind the same `execute(Command)` interface. Keep provider entity IDs outside model-visible prompts, map logical IDs to integration IDs in configuration, require device acknowledgements, and preserve idempotency plus audit logging. Start with low-risk lights or sockets; do not use the prototype confirmation flow as production-grade authentication.

