# Kids Video Production Setup

The production workflow is split between n8n and GitHub Actions.

## 1. GitHub repository secret

In `shiy1s/kids-videos`, add this Actions secret:

- `OPENAI_API_KEY`

The GitHub worker uses it only for image generation and text-to-speech.

Optional repository variables:
- `KIDS_IMAGE_MODEL` (default: `gpt-image-1-mini`)
- `KIDS_IMAGE_QUALITY` (default: `medium`)
- `KIDS_TTS_MODEL` (default: `gpt-4o-mini-tts`)
- `KIDS_TTS_VOICE` (default: `alloy`)

## 2. n8n GitHub credential

The workflow node `Dispatch GitHub Worker` needs a GitHub OAuth2 credential with access to:

- repository workflow dispatch
- repository Actions/artifact read access

The `Download Render Artifact` HTTP node uses the same GitHub OAuth2 credential as a predefined credential.

Select the credential in both nodes.

## 3. n8n YouTube credential

The nodes `Upload Private YouTube Video` and `Get Uploaded YouTube Video` need the YouTube OAuth2 credential for the channel that should receive the videos.

The workflow intentionally uploads with:

- privacy: `private`
- made for kids: `true`
- subscriber notification: disabled
- public stats: disabled

Do not change privacy to public while testing.

## 4. n8n workflow

Production workflow:

`youtube kids`

Workflow ID:

`e96gnQMkBsnfkag7`

It is currently inactive until credentials are connected.

Triggers:
- Manual Trigger
- Daily Schedule at 10:00 Asia/Kolkata

## 5. First test

After credentials are connected:

1. Keep the workflow inactive.
2. Use **Manual Trigger**.
3. Confirm story generation succeeds.
4. Confirm GitHub Actions starts `Kids Video Worker`.
5. Confirm the worker generates scene images and narration.
6. Confirm FFmpeg renders 1080x1920 MP4.
7. Confirm QC passes.
8. Confirm n8n receives the worker callback.
9. Confirm the artifact is downloaded and decompressed.
10. Confirm YouTube upload is **private**.
11. Confirm the tracking node records the returned YouTube video ID/status.

Only after a complete successful private run should activation be considered.

## Isolation

This project is independent of the Whop automation.

Do not connect this workflow to:
- `shiy1s/whopautomation`
- the Whop n8n workflow
- Whop credentials
- Whop campaign data

## Content rules

The generator is designed for original child-directed content. It rejects obvious unsafe content and instructs image generation to avoid copyrighted characters, logos, brands, frightening imagery, violence, sexual content, hate, dangerous instructions, and living-artist style imitation.
