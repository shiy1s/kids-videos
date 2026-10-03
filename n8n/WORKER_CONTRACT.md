# GitHub Worker Contract

## Inputs

n8n dispatches `kids-video-worker.yml` with:

- `job_id`
- `job_json`
- `resumeUrl` supplied automatically by n8n GitHub Dispatch and Wait

The job JSON must contain:

- `jobId`
- `content.topic`
- `content.ageRange`
- `content.language`
- `content.story`
- `content.characterBible`
- `content.styleBible`
- `content.scenes[]`
- `video.width`
- `video.height`
- `video.fps`

## Worker responsibilities

1. Generate one original image per scene.
2. Generate narration audio for each scene.
3. Build a scene manifest with image/audio paths.
4. Render with `scripts/render/render_ffmpeg.py`.
5. Run `scripts/qc/validate_media.py`.
6. Upload the final MP4 as a GitHub Actions artifact.
7. POST a JSON completion result to the n8n resume URL.
8. POST a failure result to the same resume URL when the job fails.

The worker never publishes to YouTube directly.

## Result

Success:

```json
{
  "jobId": "kids-...",
  "status": "success",
  "stage": "render_qc",
  "artifactId": 123456
}
```

Failure:

```json
{
  "jobId": "kids-...",
  "status": "failed",
  "stage": "render_qc"
}
```
