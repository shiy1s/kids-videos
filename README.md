# n8n YouTube Kids

Production-oriented automation for generating original child-directed cartoon videos.

## Current production architecture

```
n8n
  |
  +-- Story + scene planning
  +-- Safety and duration validation
  +-- Job payload
  |
  +-- GitHub Actions: Kids Video Worker
  |     +-- original scene image generation
  |     +-- narration generation
  |     +-- scene manifest
  |     +-- FFmpeg render
  |     +-- media QC
  |     +-- GitHub artifact
  |     +-- n8n resume callback
  |
  +-- Artifact download/decompression
  +-- Private YouTube upload
  +-- Publication tracking
```

## n8n

Production workflow: `youtube kids`

Workflow ID: `e96gnQMkBsnfkag7`

The workflow is deliberately inactive until GitHub and YouTube credentials are connected.

The n8n instance has a 180-second execution timeout. The GitHub worker handoff uses the GitHub node's Dispatch and Wait mechanism so the n8n execution can suspend while the external worker performs media generation/rendering.

## GitHub

Repository: `shiy1s/kids-videos`

Main worker:

`.github/workflows/kids-video-worker.yml`

The worker is deterministic after the AI asset calls: it generates the requested media, renders with the repository FFmpeg renderer, runs media QC, uploads the MP4 artifact, and calls the n8n resume URL.

## Publishing safety

YouTube upload is hard-coded to private mode in the workflow. The publish gate also refuses to continue unless the job explicitly says:

- privacyStatus = private
- madeForKids = true

Automatic public publishing is not enabled.

## Isolation

This project is completely separate from the Whop automation. It must not import, modify, or depend on `shiy1s/whopautomation` or its n8n workflow.

## Setup

See `SETUP.md`.
