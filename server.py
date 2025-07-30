#!/usr/bin/env python3
"""
Simple HTTP server that disables caching for development.
Run with: python server.py
Access at: http://localhost:8000 or http://your-ip:8000
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import socket

class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler that disables all caching"""
    
    def end_headers(self):
        # Add headers to completely disable caching
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Last-Modified', '0')
        self.send_header('ETag', '')
        super().end_headers()

    def log_message(self, format, *args):
        """Custom log format to show what files are being served"""
        print(f"[{self.address_string()}] {format % args}")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multi-threaded HTTP server for better performance"""
    allow_reuse_address = True

def get_local_ip():
    """Get the local IP address for network access"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "localhost"

def main():
    # Configuration
    PORT = 8000
    HOST = '0.0.0.0'  # Allow access from any IP
    
    # Change to script directory if running from elsewhere
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    # Create server
    server = ThreadedHTTPServer((HOST, PORT), NoCacheHTTPRequestHandler)
    local_ip = get_local_ip()
    
    print(f"🚀 Development server starting...")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"🌐 Local access: http://localhost:{PORT}")
    print(f"📱 Network access: http://{local_ip}:{PORT}")
    print(f"🚫 Cache disabled - all changes will reflect immediately!")
    print(f"⏹️  Press Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()

if __name__ == '__main__':
    main()
