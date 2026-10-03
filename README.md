# Kids Videos Automation

Production-oriented automation for creating and publishing original, child-friendly cartoon videos.

## Architecture
- n8n: orchestration, scheduling, workflow state
- GitHub Actions: deterministic workers and rendering
- FFmpeg: final assembly/rendering
- AI services: story/script/asset generation through replaceable adapters
- YouTube API: publishing and publication tracking

## Isolation
This repository is independent of the existing Whop automation project. Do not import, modify, or depend on `shiy1s/whopautomation` or its n8n workflow.

## Safety
- Create original content; do not imitate living artists or copyrighted franchises.
- Avoid unsafe, frightening, sexual, hateful, violent, or otherwise inappropriate content for children.
- Do not publish until automated QC passes.
- Never commit API keys, OAuth refresh tokens, or other secrets.

## Project stages
1. Content ideation
2. Script generation
3. Scene/asset planning
4. Asset generation
5. Voice/music generation
6. FFmpeg rendering
7. Automated QC
8. Metadata generation
9. YouTube publishing
10. Publication tracking
