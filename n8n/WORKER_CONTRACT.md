# GitHub Worker Contract

## Render worker inputs

`kids-video-worker.yml` receives:
- `job_id`
- `job_json`
- `resumeUrl`

## Render worker responsibilities

1. Create original procedural cartoon artwork with Pillow.
2. Create narration locally with espeak-ng.
3. Build the scene manifest.
4. Render with `scripts/render/render_ffmpeg.py`.
5. Run `scripts/qc/validate_media.py`.
6. Upload the final MP4 as a GitHub Actions artifact.
7. Resume n8n with `jobId`, `status`, `stage`, and `artifactId`.

## YouTube publisher inputs

`youtube-publish.yml` receives:
- `job_id`
- `artifact_id`
- `title`
- `description`
- `resumeUrl`

## YouTube publisher

The publisher downloads the render artifact and uses:
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

The publisher sets:
- privacy status: `private`
- self declared Made for Kids: `true`
- public stats viewable: `false`

The publisher never makes a video public.

## Result

Success callback contains `status=success` and `youtubeVideoId`.
Failure callback contains `status=failed` and the failed stage.

No paid AI service is used anywhere in the worker.
