# Security policy

This repository is a research prototype and simulator. Do not connect it directly to locks, alarms, valves, heaters, or other safety-critical devices.

Please report vulnerabilities privately through GitHub's security advisory feature. Do not open a public issue containing secrets, household identifiers, network topology, or exploit details.

The following are particularly relevant:

- bypassing device/action allowlists;
- executing a high-risk command without confirmation;
- prompt injection that reaches the executor;
- path traversal or sensitive data exposure in logs;
- unsafe parameter-boundary behavior.

