# Diagnose → Authorize → Remediate → Verify

## Diagnose
Inspect evidence and determine the observed defect.

## Authorization gate
Before modifying the defective artifact, determine whether remediation
was explicitly authorized.

If NO:
- preserve the artifact;
- record the observed defect;
- propose remediation;
- stop before modification.

If YES:
- apply only the authorized remediation.

## Verify
After authorized remediation, independently verify the required invariant.

## Report
Distinguish:
- observed state;
- proposed change;
- authorization status;
- executed change, if any;
- verification result.
