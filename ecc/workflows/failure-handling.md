# Failure Handling

When verification fails:

1. Stop treating the expected result as true.
2. Preserve the observed state.
3. Re-run or independently check the failing condition once when useful.
4. Record:
   - expected value;
   - observed value;
   - verification method;
   - status: FAIL.
5. Do not modify source evidence solely to convert FAIL into PASS.
6. Report the failure clearly and continue only if the task explicitly requires remediation.
