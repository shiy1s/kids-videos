# Architecture

## Separation of responsibilities

### n8n
Owns:
- schedule/trigger
- job creation
- orchestration
- calling AI/content providers
- dispatching GitHub Actions
- polling worker results
- recording state
- deciding whether a job may advance

### GitHub Actions
Owns:
- deterministic media workers
- rendering
- media QC
- publishing worker execution
- artifacts/logs

### Content lifecycle
```
TRIGGER
  -> STORY
  -> SCRIPT
  -> SCENE PLAN
  -> ASSET GENERATION
  -> AUDIO
  -> RENDER
  -> QC
  -> METADATA
  -> PUBLISH
  -> TRACK
```

No production publishing step should run unless the upstream job has a successful QC result.
