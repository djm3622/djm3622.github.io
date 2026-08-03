#!/usr/bin/env python3
"""Obtain the Spotify refresh token used by the daily-selection workflow."""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import http.server
import json
import os
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser
from typing import Sequence

REDIRECT_URI = "http://127.0.0.1:8765/callback"
SCOPES = "playlist-read-private"


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    code: str | None = None
    returned_state: str | None = None
    error: str | None = None

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler uses this API.
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        type(self).code = query.get("code", [None])[0]
        type(self).returned_state = query.get("state", [None])[0]
        type(self).error = query.get("error", [None])[0]
        body = (
            b"Spotify authorization received. You can close this tab and return to the terminal."
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def _exchange_code(client_id: str, client_secret: str, code: str) -> str:
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
    request = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=urllib.parse.urlencode(
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            }
        ).encode("ascii"),
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    refresh_token = payload.get("refresh_token")
    if not isinstance(refresh_token, str) or not refresh_token:
        raise RuntimeError("Spotify did not return a refresh token")
    return refresh_token


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-id", default=os.environ.get("SPOTIFY_CLIENT_ID"))
    parser.add_argument("--no-browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    client_id = args.client_id or input("Spotify client ID: ").strip()
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET") or getpass.getpass(
        "Spotify client secret: "
    )
    if not client_id or not client_secret:
        raise SystemExit("A Spotify client ID and client secret are required")

    state = secrets.token_urlsafe(32)
    # Include a non-secret verifier in the state derivation to make accidental reuse obvious.
    state = hashlib.sha256(f"{state}:{client_id}".encode()).hexdigest()
    authorization_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
            "show_dialog": "true",
        }
    )

    server = http.server.HTTPServer(("127.0.0.1", 8765), CallbackHandler)
    print(f"Open this URL to authorize Spotify:\n\n{authorization_url}\n")
    if not args.no_browser:
        threading.Timer(0.25, webbrowser.open, args=(authorization_url,)).start()
    server.handle_request()
    server.server_close()

    if CallbackHandler.error:
        raise SystemExit(f"Spotify authorization failed: {CallbackHandler.error}")
    if CallbackHandler.returned_state != state or not CallbackHandler.code:
        raise SystemExit("Spotify returned an invalid authorization response")

    refresh_token = _exchange_code(client_id, client_secret, CallbackHandler.code)
    print("Authorization succeeded. Save this value as SPOTIFY_REFRESH_TOKEN:")
    print(refresh_token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
