import http.server
import socketserver
import brotli
import os
import io

PORT = 8000

class BrotliHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isfile(path):
            f = open(path, 'rb')
            self.send_response(200)
            self.send_header("Content-type", self.guess_type(path))
            if path.endswith('.html') or path.endswith('.js') or path.endswith('.css'):
                content = f.read()
                compressed_content = brotli.compress(content)
                f.close()
                self.send_header("Content-Encoding", "br")
                self.send_header("Content-Length", str(len(compressed_content)))
                self.end_headers()
                return io.BytesIO(compressed_content)
            else:
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
        else:
            return super().send_head()

Handler = BrotliHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
