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
        upload_path = filename
        local_image_path = f"/opt/render/project/src/{filename}"

        gToken = Github(token)
        repo = gToken.get_repo(repo_name)

        with open(local_image_path, "rb") as f:
            content = f.read()

        try:
            file = repo.get_contents(upload_path)
            repo.update_file(upload_path, "Update image", content, file.sha)
            response = "Image updated successfully!"
        except Exception as e:
            response = f"Failed to update the file: {str(e)}"
        
        try:
            repo.create_file(upload_path, "Add image", content)
            response = "Image added successfully!"
        except Exception as e:
            response = f"Failed to add the file: {str(e)}"
            
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



