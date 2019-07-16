import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT, "\nGo to http://localhost:8000/html_map/HTMLmap.html")
    httpd.serve_forever()