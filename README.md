# research-ai-stack

Secure and reproducible infrastructure for experimenting with AI agent harnesses in research-software workflows.

The project separates agent execution, model inference, credentials, engineering context, and writable workspaces into explicit security boundaries.

## Architecture

```text
ECC (read-only)
      │
      ▼
Agent Harness
   DSH
      │
      │ OpenAI-compatible API
      │ dummy credential only
      ▼
Provider Gateway
      │
      │ real provider credential
      ▼
Blablador
```

The agent runtime has no direct Internet access and does not receive the real inference-provider credential.

## Current status

### Phase B — Secure DSH / Blablador integration

Completed:

- isolated DSH runtime;
- provider gateway;
- credential separation;
- restricted provider egress;
- custom OpenAI-compatible provider;
- Blablador `alias-code` inference;
- tool calling;
- controlled workspace writes;
- negative isolation tests.

### Phase C — Engineering Context and Control

ECC is mounted read-only into the agent runtime and currently validates:

- **ECC-M0** — context and rule consumption;
- **ECC-M1** — plan → execute → verify;
- **ECC-M2** — evidence over expectations;
- **ECC-M3** — authorization-gated remediation.

## Security properties

Validated properties include:

```text
Agent → direct Internet        BLOCKED
Agent → provider gateway       ALLOWED
Real provider credential       ABSENT from agent
Docker socket                  ABSENT from agent
Private host filesystem        ABSENT from agent
ECC                            READ ONLY
Workspace                      READ/WRITE
```

See [`docs/security-model.md`](docs/security-model.md).

## Repository structure

```text
.
├── ecc/
│   ├── rules/
│   ├── skills/
│   └── workflows/
├── infra/
│   ├── docker/
│   ├── policies/
│   └── provider-gateway/
├── docs/
│   └── validation/
└── workspaces/
    └── public/
```

Runtime state, credentials, generated workspace artifacts, and provider secrets are intentionally excluded from version control.

## ECC

Engineering Context and Control provides reusable behavioral contracts for research agents.

Current rules cover:

- planning;
- evidence discipline;
- verification;
- remediation authorization.

Current workflows include:

- plan → execute → verify;
- verify before done;
- failure handling;
- diagnose → authorize → remediate → verify.

ECC is intentionally independent of the inference provider and is intended to become portable across multiple agent harnesses.

## Planned work

- provenance and auditability;
- reproducible evidence capture;
- scientific-software workflows;
- language-specific engineering skills;
- HERMES integration;
- OpenHarness integration;
- comparative harness evaluation.

## Secrets

Provider credentials are not committed to this repository.

Create:

```text
infra/provider-gateway/secrets/blablador-token
```

locally and restrict its permissions:

```bash
chmod 600 infra/provider-gateway/secrets/blablador-token
```

The secret file is ignored by Git.

## License

MIT
