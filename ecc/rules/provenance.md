# Provenance and Auditability

1. Preserve original input artifacts unless explicitly authorized to modify them.
2. Record the identity and SHA-256 digest of every relevant input artifact.
3. Record the identity and SHA-256 digest of every generated output artifact.
4. Derive hashes and measurements from actual files using available tools.
5. Never invent hashes, timestamps, measurements, command results, or verification outcomes.
6. Record the transformation performed and the verification method used.
7. Distinguish expected results from observed results.
8. Record the ECC rules and workflows used during execution.
9. Preserve failed artifacts and report discrepancies without altering evidence.
10. Treat agent-generated audit records as claims requiring independent verification.
