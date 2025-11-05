#!/usr/bin/env python3
from github import Github
import http.server
import os
import re
import time

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Read raw POST body
        content_length = int(self.headers.get('Content-Length', 0))
        binary_data = self.rfile.read(content_length)

        # Extract filename from Content-Disposition header
        content_disposition = self.headers.get('Content-Disposition', '')
        filename = ''

        match = re.search(r'filename="?(?P<filename>[^"]+)"?', content_disposition)
        if match:
            filename = os.path.basename(match.group('filename'))

        # Fallback file name if no filename provided
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"
        else:
            # Ensure .png extension
            if not filename.lower().endswith(".png"):
                filename += ".png"

        token = "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"
        repo_name = "TshepoLucky/python_screenshot"
        file_path = filename
        upload_path = f"TshepoLucky/images/{filename}"

        gToken = Github(token)
        repo = g.get_repo(repo_name)

        with open(file_path, "rb") as f:
            content = f.read()

        try:
            repo.create_file(upload_path, "Upload image", content)
            print("✅ Image uploaded successfully!")
        except Exception as e:
            print("⚠️ Error:", e)


        # Save file in same directory as the script
        upload_dir = os.getcwd()
        upload_file = os.path.join(upload_dir, filename)

        try:
            with open(upload_file, "wb") as f:
                f.write(binary_data)
            response = f"File is valid and was successfully uploaded: {upload_file}"
        except Exception as e:
            response = f"Failed to write the file: {str(e)}"

        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b"Invalid request method. Only POST allowed.")

if __name__ == "__main__":
    PORT = 8080  # change if needed
    server = http.server.HTTPServer(("0.0.0.0", PORT), UploadHandler)
    print(f"Server running on http://127.0.0.1:{PORT}/ (CTRL+C to stop)")
    server.serve_forever()
