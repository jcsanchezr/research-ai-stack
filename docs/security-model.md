# Security Model

## Goal

Allow an AI agent to use an external inference provider without granting the agent unrestricted Internet access or possession of the real provider credential.

## Trust boundaries

```text
Agent Plane
    │
    ▼
Provider Boundary
    │
    ▼
External Inference Provider
