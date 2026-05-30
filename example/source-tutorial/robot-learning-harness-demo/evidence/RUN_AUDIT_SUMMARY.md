# Run Audit Summary

This summary records the verification result for the completed local workspace
`workspaces/source-tutorial-real-e2e-20260412/`.

Observed command:

```bash
uv run python scripts/pipeline.py audit --workspace workspaces/source-tutorial-real-e2e-20260412
```

Observed result:

- Pipeline: `source-tutorial`
- Current checkpoint: `DONE`
- Unit status: `DONE: 18`
- Target artifacts: all present
- Harness issues: none
- Audit verdict: PASS

The command output was used to create this portable exhibit. The tracked
fixture does not replace a live workspace audit.
