# Reproducible Evidence Capture (REC-M1)

## Purpose

REC-M1 provides independent verification of agent-generated
provenance records.

The initial implementation targets the ECC-M4 experiment.

## Architecture

The agent produces:

- input.txt
- output.txt
- audit.json

The host-side verifier independently checks:

- audit record structure;
- authorized artifact paths;
- SHA-256 integrity;
- input preservation against a supplied reference digest;
- correctness of the append_computed_sum transformation;
- consistency of reported verification results;
- ECC rule and workflow references.

An agent-reported PASS is not sufficient evidence of success.

## Evidence provenance

The files under experiments/ecc-m4/ are reconstructed fixtures.

They reproduce the known content and SHA-256 digests of the
ECC-M4 artifacts verified on the operational host.

They are not original copies collected directly from that host.

Input SHA-256:
5d4f21fe14cc96a1c1eda5e674fe897b47d461c4523b1e51eb97d78329fb0636

Output SHA-256:
e6071850fbf12b172d8d5341f651d26e5385aa332fcb40713d88a5547c146380

The reference input digest must come from a trusted source
independent of the agent being evaluated.

## Run the verifier

From the repository root:

python3 evidence/tools/verify_audit.py \
  --workspace evidence/experiments/ecc-m4 \
  --audit evidence/experiments/ecc-m4/audit.json \
  --original-input-sha256 \
  5d4f21fe14cc96a1c1eda5e674fe897b47d461c4523b1e51eb97d78329fb0636 \
  --report evidence/reports/ecc-m4-verification.json

Expected result:

- status: PASS
- exit code: 0

## Run regression tests

python3 -m unittest discover \
  -s evidence/tests \
  -p 'test_*.py' \
  -v

The initial regression suite contains 16 tests.

## Audit schema

schemas/audit.schema.json documents the initial audit contract
using JSON Schema Draft 2020-12.

The Python verifier implements explicit checks for the ECC-M4
contract. It is not a complete JSON Schema validation engine.

## Security boundaries

The verifier is intended to run against a controlled local
workspace without untrusted concurrent writers.

Direct symbolic links for the input and output artifacts are
rejected.

The implementation does not yet guarantee protection against:

- symbolic links in every intermediate path component;
- time-of-check/time-of-use races;
- arbitrary malicious filesystem changes during verification.

The verifier must not be treated as a sandbox.

## Scope

REC-M1 currently validates the ECC-M4 append_computed_sum
transformation.

Support for additional transformations and harnesses requires
explicit extensions and corresponding regression tests.

## Publication policy

Do not publish:

- API tokens or credentials;
- private host paths;
- operational secrets;
- unsanitized runtime logs;
- private infrastructure identifiers.

Only reviewed, sanitized evidence should be committed.
