# GitHub worker contract

n8n dispatches the render workflow with a manifest path, unique jobId, and stage name.

The worker must:
1. render deterministically
2. run media QC
3. upload the resulting video as a GitHub Actions artifact
4. expose the workflow run ID to n8n
5. never publish directly

Publishing remains a separate gated stage.
