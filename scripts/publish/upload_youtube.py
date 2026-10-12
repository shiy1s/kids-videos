"""Upload a rendered Kids Video only after verifying the expected YouTube channel."""
from __future__ import annotations
import argparse, json, os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

EXPECTED_CHANNEL_ID = "UC4lsyrsTBdJ0GVhOKgoUs4g"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--tags", default="kids,cartoon,original story,children")
    a = p.parse_args()

    if not a.video.exists():
        raise SystemExit("VIDEO_FILE_MISSING")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    if not all((client_id, client_secret, refresh_token)):
        raise SystemExit("YOUTUBE_OAUTH_SECRET_MISSING")

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )
    try:
        creds.refresh(Request())
    except Exception as exc:
        raise SystemExit(f"YOUTUBE_OAUTH_REFRESH_FAILED: {type(exc).__name__}") from None

    youtube = build("youtube", "v3", credentials=creds)

    # Fail closed: never upload unless this OAuth token resolves to HAPPY HIPPO.
    try:
        channel_response = youtube.channels().list(part="id,snippet", mine=True).execute()
    except Exception as exc:
        raise SystemExit(
            "YOUTUBE_CHANNEL_VERIFICATION_FAILED: check that the refresh token grants "
            "youtube.readonly as well as youtube.upload; no video was uploaded. "
            f"Error type: {type(exc).__name__}"
        ) from None

    channels = channel_response.get("items", [])
    if len(channels) != 1 or channels[0].get("id") != EXPECTED_CHANNEL_ID:
        found = [item.get("id") for item in channels]
        raise SystemExit(
            "YOUTUBE_CHANNEL_MISMATCH: expected HAPPY HIPPO channel "
            f"{EXPECTED_CHANNEL_ID}; OAuth returned {found}. No video was uploaded."
        )

    body = {
        "snippet": {
            "title": a.title[:100],
            "description": a.description[:5000],
            "tags": [tag.strip() for tag in a.tags.split(",") if tag.strip()],
            "categoryId": "1",
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": True,
            "publicStatsViewable": True,
            "embeddable": True,
        },
    }
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(a.video), mimetype="video/mp4", resumable=True),
    )
    response = None
    while response is None:
        _, response = request.next_chunk()

    print(json.dumps({
        "status": "success",
        "verifiedChannelId": EXPECTED_CHANNEL_ID,
        "youtubeVideoId": response["id"],
        "privacyStatus": response.get("status", {}).get("privacyStatus", "unknown"),
        "madeForKids": response.get("status", {}).get("selfDeclaredMadeForKids", True),
        "title": response.get("snippet", {}).get("title", a.title),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
