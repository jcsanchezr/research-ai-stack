# Remediation and Authorization

1. Detecting a defect does not imply authorization to modify it.
2. Separate:
   - diagnosis;
   - proposed remediation;
   - authorized execution.
3. When remediation is not explicitly authorized:
   - preserve the defective artifact;
   - report the defect;
   - propose a concrete remediation;
   - do not apply it.
4. Modify an artifact only when the task explicitly authorizes remediation.
5. After authorized remediation:
   - verify the resulting state;
   - report what changed;
   - preserve evidence sufficient to explain the correction.
6. Never expand remediation beyond the explicitly authorized scope.
