# Provenance Audit Workflow

## 1. Inspect

Read the applicable ECC rules and workflows.

Identify:
- authorized input artifacts;
- permitted output locations;
- expected transformation;
- verification criteria.

## 2. Capture Input Evidence

Before modifying state:
- identify the source artifact;
- compute its SHA-256 digest;
- record relevant source measurements.

## 3. Execute

Perform only the authorized transformation.
Do not modify original evidence unless explicitly authorized.

## 4. Capture Output Evidence

After execution:
- identify generated artifacts;
- compute their SHA-256 digests;
- record relevant output measurements.

## 5. Verify

Execute the requested verification.

Distinguish:
- expected result;
- observed result;
- verification status.

Do not report PASS without successful verification.

## 6. Produce Audit Record

Create a structured audit record containing:
- milestone identifier;
- input artifact and SHA-256;
- output artifact and SHA-256;
- transformation description;
- ECC rules and workflows used;
- verification method;
- expected result;
- observed result;
- agent-reported status.

## 7. Independent Verification

The host-side verifier must independently:
- recompute artifact hashes;
- verify input preservation;
- verify output correctness;
- validate the audit record;
- determine final PASS or FAIL.

An agent-reported PASS is not sufficient evidence of success.
