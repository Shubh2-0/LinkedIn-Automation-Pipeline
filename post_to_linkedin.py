"""
LinkedIn Auto-Poster — Used by GitHub Actions
===============================================
Posts a carousel (PDF) + caption to LinkedIn automatically.
Determines which day to post based on schedule.json.

Usage: python post_to_linkedin.py
Env vars needed: LINKEDIN_ACCESS_TOKEN
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_FILE = os.path.join(SCRIPT_DIR, "schedule.json")
PDFS_DIR = os.path.join(SCRIPT_DIR, "pdfs")

IST = timezone(timedelta(hours=5, minutes=30))


def get_access_token():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("[ERROR] LINKEDIN_ACCESS_TOKEN not set")
        sys.exit(1)
    return token


def get_user_id(token):
    """Get LinkedIn user ID (person URN)."""
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code != 200:
        print(f"[ERROR] Failed to get user info: {resp.status_code} {resp.text}")
        sys.exit(1)
    return resp.json()["sub"]


def upload_pdf(token, user_id, pdf_path):
    """Upload PDF to LinkedIn and get document URN."""
    # Step 1: Register upload
    register_data = {
        "initializeUploadRequest": {
            "owner": f"urn:li:person:{user_id}",
        }
    }

    resp = requests.post(
        "https://api.linkedin.com/rest/documents?action=initializeUpload",
        json=register_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": "202401",
            "X-Restli-Protocol-Version": "2.0.0",
        },
    )

    if resp.status_code not in (200, 201):
        print(f"[ERROR] Register upload failed: {resp.status_code} {resp.text}")
        sys.exit(1)

    upload_data = resp.json()["value"]
    upload_url = upload_data["uploadUrl"]
    document_urn = upload_data["document"]

    # Step 2: Upload the PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    resp = requests.put(
        upload_url,
        data=pdf_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
            "LinkedIn-Version": "202401",
        },
    )

    if resp.status_code not in (200, 201):
        print(f"[ERROR] PDF upload failed: {resp.status_code} {resp.text}")
        sys.exit(1)

    print(f"  [OK] PDF uploaded: {document_urn}")
    return document_urn


def create_post(token, user_id, caption, document_urn, pdf_title):
    """Create LinkedIn post with document attachment."""
    post_data = {
        "author": f"urn:li:person:{user_id}",
        "commentary": caption,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "content": {
            "media": {
                "title": pdf_title,
                "id": document_urn,
            }
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    resp = requests.post(
        "https://api.linkedin.com/rest/posts",
        json=post_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": "202401",
            "X-Restli-Protocol-Version": "2.0.0",
        },
    )

    if resp.status_code in (200, 201):
        print(f"  [OK] Post created successfully!")
        return True
    else:
        print(f"  [ERROR] Post failed: {resp.status_code} {resp.text}")
        return False


def main():
    print("\n" + "=" * 50)
    print("  LINKEDIN AUTO-POSTER")
    print("=" * 50)

    # Load schedule
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    # Find today's post
    today = datetime.now(IST).strftime("%Y-%m-%d")
    print(f"\n  Today (IST): {today}")

    today_post = None
    for post in schedule["posts"]:
        if post["date"] == today:
            today_post = post
            break

    if not today_post:
        print(f"  [INFO] No post scheduled for today. Skipping.")
        return

    if today_post.get("posted", False):
        print(f"  [INFO] Already posted today. Skipping.")
        return

    print(f"  [OK] Found post: Day {today_post['day']} — {today_post['title']}")

    # Get token and user ID
    token = get_access_token()
    user_id = get_user_id(token)
    print(f"  [OK] User ID: {user_id}")

    # Upload PDF
    pdf_path = os.path.join(PDFS_DIR, today_post["pdf"])
    if not os.path.exists(pdf_path):
        print(f"  [ERROR] PDF not found: {pdf_path}")
        sys.exit(1)

    document_urn = upload_pdf(token, user_id, pdf_path)

    # Create post
    success = create_post(token, user_id, today_post["caption"], document_urn, today_post["title"])

    if success:
        # Mark as posted
        today_post["posted"] = True
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(schedule, f, indent=2, ensure_ascii=False)
        print(f"\n  [DONE] Day {today_post['day']} posted successfully!")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
