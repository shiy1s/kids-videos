# Kids Video Production Setup

## GitHub

The repository already contains the YouTube secrets required by the publishing worker:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

Do **not** add `OPENAI_API_KEY`. It is not used.

## n8n GitHub credential

`Dispatch GitHub Worker` and `Dispatch YouTube Publisher` need the existing GitHub OAuth credential in n8n with permission to dispatch workflows and read Actions artifacts.

## YouTube

No YouTube credential needs to be stored in n8n. The GitHub publishing worker uses the three repository secrets above.

The refresh token is exchanged for a short-lived access token at Google's OAuth token endpoint. The upload uses the YouTube Data API with the `youtube.upload` scope.

## First controlled test

1. Keep `youtube kids` inactive.
2. Run **Manual Trigger** once.
3. Verify `Generate Story And Scene Plan` creates six scenes.
4. Verify `Dispatch GitHub Worker` starts `Kids Video Worker`.
5. Verify the worker creates six original procedural cartoon images.
6. Verify espeak-ng creates narration audio.
7. Verify FFmpeg creates a 1080x1920 MP4 and QC passes.
8. Verify n8n receives the artifact ID.
9. Verify `Dispatch YouTube Publisher` starts `Kids YouTube Publisher`.
10. Verify the video is uploaded as **private** and marked **Made for Kids**.
11. Verify `Track Publication` records the YouTube video ID.

Do not activate the daily schedule until this controlled run succeeds.

## Important

n8n being connected to GitHub does not expose GitHub Actions secrets to n8n. That is intentional: the YouTube secrets stay inside GitHub Actions and are consumed only by the publishing worker.

## Isolation

This project is independent of the Whop automation. Do not connect it to `shiy1s/whopautomation`, the Whop n8n workflow, Whop credentials, or Whop campaign data.
