import http.server

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.lower().endswith('.mp4'):
            self.send_header('Content-Disposition', 'attachment; filename="FAI_Create_Ad_120s_1080x1920.mp4"')
        super().end_headers()

http.server.ThreadingHTTPServer(('0.0.0.0', 8765), H).serve_forever()
