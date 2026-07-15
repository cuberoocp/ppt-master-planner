#!/usr/bin/env python3
"""PPT Master Planner — Review server.

Local HTTP server for layout direction review and visual review.
Users submit feedback via browser, server validates with one-time approval keys.

Usage:
  python scripts/review_server.py <project_dir> [--port PORT] [--approval-key KEY]
"""

import argparse
import json
import os
import secrets
import sys
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs


SESSION_ID = secrets.token_hex(8)
APPROVAL_KEY = None


class ReviewHandler(BaseHTTPRequestHandler):
    """HTTP handler for review pages and feedback submission."""

    project_dir = None
    approval_key = None

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _load_json(self, rel_path: str) -> dict:
        full = Path(self.project_dir) / rel_path
        if not full.exists():
            return {}
        with open(full, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, rel_path: str, data: dict):
        full = Path(self.project_dir) / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _verify_key(self, params: dict) -> bool:
        key = params.get("approval_key", [""])[0]
        return key == self.approval_key

    def _provenance(self, route: str, params: dict = None) -> dict:
        return {
            "source": "review_server",
            "session_id": SESSION_ID,
            "route": route,
            "timestamp": datetime.now().isoformat(),
            "approval_key_required": True,
            "approval_key_verified": bool(params and self._verify_key(params)),
        }

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/layout":
            layout_html = Path(self.project_dir) / "_internal" / "01_layout_plan" / "01_layout_direction.html"
            if layout_html.exists():
                self._send_html(layout_html.read_text(encoding="utf-8"))
            else:
                self._send_html(f"<html><body><h1>Layout Review</h1><p>Layout direction page not yet generated.</p><p>Run: python scripts/generate_layout_html.py {self.project_dir}</p></body></html>")

        elif path == "/review":
            review_html = Path(self.project_dir) / "_internal" / "05_review" / "02_visual_review.html"
            if review_html.exists():
                self._send_html(review_html.read_text(encoding="utf-8"))
            else:
                self._send_html(f"<html><body><h1>Visual Review</h1><p>Review page not yet generated.</p><p>Run: python scripts/generate_review_html.py {self.project_dir}</p></body></html>")

        elif path == "/status":
            self._send_json({
                "session_id": SESSION_ID,
                "project": Path(self.project_dir).name,
                "approval_key_required": True,
                "approval_key_set": self.approval_key is not None,
            })

        elif path == "/shutdown":
            self._send_json({"message": "Server shutting down"})
            Thread(target=self.server.shutdown).start()

        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length else ""

        try:
            params = parse_qs(body) if "=" in body else json.loads(body) if body else {}
        except json.JSONDecodeError:
            try:
                params = parse_qs(body)
            except Exception:
                params = {}

        if not isinstance(params, dict):
            try:
                params = json.loads(body) if body else {}
            except Exception:
                params = {}

        route = parsed.path
        provenance = self._provenance(route, params)

        if route == "/layout-feedback":
            layout_feedback = self._load_json("_internal/01_layout_plan/layout_feedback.json")

            approved = params.get("approved", params.get("all_approved", False))
            if isinstance(approved, str):
                approved = approved.lower() in ("true", "1", "yes")

            key_verified = self._verify_key(params) if approved else False

            feedback = {
                "approval": {
                    "approved": approved,
                    "all_approved": approved,
                    "approval_key_required": True,
                    "approval_key_verified": key_verified,
                    "provenance": provenance,
                    "comments": params.get("comments", ""),
                    "timestamp": datetime.now().isoformat(),
                }
            }

            if approved and not key_verified:
                self._send_json({"error": "Approval key required for approval"}, 403)
                return

            self._save_json("_internal/01_layout_plan/layout_feedback.json", feedback)
            self._send_json({"status": "ok", "approved": approved, "key_verified": key_verified})

        elif route == "/review-feedback":
            feedback = self._load_json("_internal/05_review/feedback.json")

            all_approved = params.get("all_approved", params.get("approved", False))
            if isinstance(all_approved, str):
                all_approved = all_approved.lower() in ("true", "1", "yes")

            key_verified = self._verify_key(params) if all_approved else False

            feedback_entry = {
                "approval": {
                    "all_approved": all_approved,
                    "approval_key_required": True,
                    "approval_key_verified": key_verified,
                    "provenance": provenance,
                    "comments": params.get("comments", ""),
                    "timestamp": datetime.now().isoformat(),
                },
                "page_feedback": params.get("page_feedback", {}),
            }

            if all_approved and not key_verified:
                self._send_json({"error": "Approval key required for approval"}, 403)
                return

            self._save_json("_internal/05_review/feedback.json", feedback_entry)

            batch_id = params.get("batch_id", f"batch_{int(time.time())}")
            batches_dir = Path(self.project_dir) / "_internal" / "05_review" / "batches"
            batches_dir.mkdir(parents=True, exist_ok=True)
            self._save_json(f"_internal/05_review/batches/{batch_id}.json", feedback_entry)

            self._send_json({
                "status": "ok",
                "all_approved": all_approved,
                "key_verified": key_verified,
                "batch_id": batch_id,
            })

        else:
            self._send_json({"error": "Not found"}, 404)


def main():
    global APPROVAL_KEY
    parser = argparse.ArgumentParser(description="PPT Master Planner — review server")
    parser.add_argument("project_dir", help="Project directory")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--approval-key", help="One-time approval key (auto-generated if not set)")
    args = parser.parse_args()

    APPROVAL_KEY = args.approval_key or secrets.token_hex(16)

    ReviewHandler.project_dir = args.project_dir
    ReviewHandler.approval_key = APPROVAL_KEY

    server = HTTPServer(("127.0.0.1", args.port), ReviewHandler)
    print(f"[REVIEW SERVER]")
    print(f"  Layout review URL:  http://127.0.0.1:{args.port}/")
    print(f"  Visual review URL:  http://127.0.0.1:{args.port}/review")
    print(f"  Session ID:         {SESSION_ID}")
    print(f"  Approval key:       {APPROVAL_KEY}")
    print(f"  One-time key:       {APPROVAL_KEY}")
    print()
    print("  User must open the review URL in browser, enter the approval key,")
    print("  and submit approval. The server validates the key before accepting.")
    print()
    print("  Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[REVIEW SERVER] Stopped")
        server.server_close()


if __name__ == "__main__":
    from threading import Thread
    main()
