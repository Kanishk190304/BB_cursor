import http.server
import socketserver
import os
import sys
import webbrowser
from urllib.parse import urlparse, parse_qs

PORT = 8000

class FinancialAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve homepage by default
        if path == '/' or path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/home.html', 'rb') as file:
                content = file.read()
                # Replace template tags with actual content
                content = content.replace(b'{% extends "base.html" %}', b'')
                content = content.replace(b'{% load static %}', b'')
                content = content.replace(b'{% block title %}Student Financial Stability - Home{% endblock %}', b'<title>Student Financial Stability - Home</title>')
                content = content.replace(b'{% block content %}', b'')
                content = content.replace(b'{% endblock %}', b'')
                content = content.replace(b'{% block extra_js %}', b'<script>')
                content = content.replace(b'{% endblock %}', b'</script>')
                content = content.replace(b'{% static', b'static')
                content = content.replace(b'%}', b'')
                self.wfile.write(content)
            return
            
        # Serve dashboard
        elif path == '/dashboard/' or path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/dashboard.html', 'rb') as file:
                content = file.read()
                # Replace template tags with actual content
                content = content.replace(b'{% extends "base.html" %}', b'')
                content = content.replace(b'{% load static %}', b'')
                content = content.replace(b'{% block title %}Dashboard - Student Financial Stability{% endblock %}', b'<title>Dashboard - Student Financial Stability</title>')
                content = content.replace(b'{% block content %}', b'')
                content = content.replace(b'{% endblock %}', b'')
                content = content.replace(b'{% block extra_js %}', b'<script>')
                content = content.replace(b'{% endblock %}', b'</script>')
                content = content.replace(b'{% static', b'static')
                content = content.replace(b'%}', b'')
                self.wfile.write(content)
            return
            
        # Serve static files
        elif path.startswith('/static/'):
            try:
                file_path = path[1:]  # Remove leading /
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    if path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    elif path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg'):
                        self.send_header('Content-type', 'image/png')
                    else:
                        self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(file.read())
                    return
            except FileNotFoundError:
                pass
        
        # Default handling for other paths
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Starting server at http://localhost:{PORT}")
print("Visit:")
print(f"- Home page: http://localhost:{PORT}/")
print(f"- Dashboard: http://localhost:{PORT}/dashboard/")
print("Press Ctrl+C to stop the server")

# Open browser automatically
webbrowser.open(f"http://localhost:{PORT}/")

# Create server
handler = FinancialAppHandler
httpd = socketserver.TCPServer(("", PORT), handler)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
    httpd.server_close()
    sys.exit(0) 