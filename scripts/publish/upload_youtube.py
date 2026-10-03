"""Upload a rendered Kids Video to YouTube using the user OAuth secrets."""
from __future__ import annotations
import argparse, json, os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
SCOPES=["https://www.googleapis.com/auth/youtube.upload"]
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--video",type=Path,required=True);p.add_argument("--title",required=True);p.add_argument("--description",required=True);p.add_argument("--tags",default="kids,cartoon,original story,children");a=p.parse_args()
    if not a.video.exists(): raise SystemExit("VIDEO_FILE_MISSING")
    cid=os.environ.get("YOUTUBE_CLIENT_ID");cs=os.environ.get("YOUTUBE_CLIENT_SECRET");rt=os.environ.get("YOUTUBE_REFRESH_TOKEN")
    if not all((cid,cs,rt)): raise SystemExit("YOUTUBE_OAUTH_SECRET_MISSING")
    creds=Credentials(token=None,refresh_token=rt,token_uri="https://oauth2.googleapis.com/token",client_id=cid,client_secret=cs,scopes=SCOPES);creds.refresh(Request())
    youtube=build("youtube","v3",credentials=creds)
    body={"snippet":{"title":a.title[:100],"description":a.description[:5000],"tags":[t.strip() for t in a.tags.split(",") if t.strip()],"categoryId":"1","defaultLanguage":"en"},"status":{"privacyStatus":"private","selfDeclaredMadeForKids":True,"publicStatsViewable":False,"embeddable":True}}
    req=youtube.videos().insert(part="snippet,status",body=body,media_body=MediaFileUpload(str(a.video),mimetype="video/mp4",resumable=True))
    response=None
    while response is None: _,response=req.next_chunk()
    print(json.dumps({"status":"success","youtubeVideoId":response["id"],"privacyStatus":response.get("status",{}).get("privacyStatus","private"),"madeForKids":response.get("status",{}).get("selfDeclaredMadeForKids",True),"title":response.get("snippet",{}).get("title",a.title)}))
    return 0
if __name__=="__main__": raise SystemExit(main())