# Architecture

## Overview

`research-ai-stack` separates agent execution, inference access, credentials, engineering context, and writable state.

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
