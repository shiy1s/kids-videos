# n8n Workflow Specification

Create the n8n workflow inside the dedicated `n8n youtube kids` folder.

## Workflow
1. Schedule Trigger
2. Generate Job Request
3. Content Safety Gate
4. Generate Story
5. Generate Scene Plan
6. Generate Asset Requests
7. Dispatch GitHub Worker
8. Poll Worker
9. QC Gate
10. Generate Metadata
11. Publish Gate
12. YouTube Upload
13. Track Publication

## State
Use a single jobId throughout the execution. Every external worker call must carry:
- jobId
- stage
- attempt
- repository
- workflow/version identifier

## Safety
The initial publishing mode must be PRIVATE. Do not enable automatic PUBLIC publishing until upload, metadata, made-for-kids handling, duplicate protection, and recovery are tested.

## Idempotency
A retry must reuse the same jobId and stage identity. A completed stage must not be executed again unless explicitly forced.
