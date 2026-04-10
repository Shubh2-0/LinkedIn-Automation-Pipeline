"""
LinkedIn OAuth Token Generator — Run ONCE on laptop
====================================================
Opens browser → LinkedIn login → Gets access token → Saves to file
Token valid for 60 days. After 60 days, run this again.

Usage: python get_token.py
"""

import http.server
import urllib.parse
import webbrowser
import requests
import json
import os

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:3000/callback"
SCOPES = "openid profile w_member_social"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")

auth_code = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html><body style="font-family:Arial;text-align:center;padding:50px;background:#0D1117;color:#fff">
                <h1 style="color:#7EE787">Token Generated Successfully!</h1>
                <p>You can close this window now.</p>
                <p>Go back to the terminal.</p>
                </body></html>
            """)
        else:
            error = params.get("error", ["Unknown"])[0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Error: {error}</h1></body></html>".encode())

    def log_message(self, format, *args):
        pass  # suppress logs


def main():
    print("\n" + "=" * 50)
    print("  LINKEDIN TOKEN GENERATOR")
    print("=" * 50)

    # Step 1: Open browser for LinkedIn login
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope={urllib.parse.quote(SCOPES)}"
    )

    print("\n  Opening browser for LinkedIn login...")
    print("  Login and click 'Allow' when prompted.\n")
    webbrowser.open(auth_url)

    # Step 2: Start local server to catch the callback
    server = http.server.HTTPServer(("localhost", 3000), CallbackHandler)
    server.timeout = 120  # 2 min timeout
    print("  Waiting for authorization (2 min timeout)...")

    while auth_code is None:
        server.handle_request()

    server.server_close()

    if not auth_code:
        print("\n  [ERROR] No authorization code received.")
        return

    print(f"\n  [OK] Authorization code received!")

    # Step 3: Exchange code for access token
    print("  Exchanging for access token...")

    token_response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if token_response.status_code != 200:
        print(f"\n  [ERROR] Token request failed: {token_response.text}")
        return

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in", 0)

    if not access_token:
        print(f"\n  [ERROR] No access token in response: {token_data}")
        return

    # Save token
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": access_token, "expires_in": expires_in}, f, indent=2)

    print(f"\n  [OK] Access token saved to: {TOKEN_FILE}")
    print(f"  [OK] Token valid for: {expires_in // 86400} days")
    print(f"\n  ACCESS TOKEN (copy this for GitHub Secret):\n")
    print(f"  {access_token}")
    print(f"\n" + "=" * 50)
    print("  NEXT STEPS:")
    print("  1. Copy the access token above")
    print("  2. Go to your GitHub repo → Settings → Secrets")
    print("  3. Add secret: LINKEDIN_ACCESS_TOKEN = <paste token>")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
