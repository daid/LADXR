#!/usr/bin/env python3

"""Sets up a small web server that hosts the LADXR web UI, and opens
the main page a browser.
"""

import argparse
import webbrowser
import http.server
import mimetypes
import os
import socketserver
import tarfile
import tempfile
import threading
import time


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SERVE_DIR = os.path.join(BASE_DIR, 'www')


parser = argparse.ArgumentParser(
    prog='LADXR Web Launcher',
    description='Launches the LADXR web UI locally and opens a browser')
parser.add_argument(
    '-p', '--port',
    default=8000,
    required=False,
    type=int,
    help='Port on which the web server will listen')
args = parser.parse_args()


class LADXRHandler(http.server.SimpleHTTPRequestHandler):
    """The request handler for the TCPServer.

    Everything in the directory www will be automatically served at
    the root url / (so www/index.html will be served as /index.html
    etc.)

    However, we need to set up a couple of custom routes:

    * All links going to /LADXR/gfx/ are outside the serving directory,
      so we need to serve them manally
    * /js/ladxr.tar.gz will be created on the fly and served
    """

    def __init__(self, *args, **kwargs):
        kwargs['directory'] = SERVE_DIR
        super().__init__(*args, **kwargs)

    def send_file_response(self, filename):
        self.send_response(200)
        self.send_header('Content-type', mimetypes.guess_type(filename))
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def do_GET(self):
        if self.path == '/js/ladxr.tar.gz':
            # Create the tgz file in a temporary directory and serve it
            with tempfile.TemporaryDirectory() as dirname:
                src = BASE_DIR
                dest = os.path.join(dirname, 'ladxr.tar.gz')
                with tarfile.open(dest, 'w:gz') as tar:
                    tar.add(src, arcname='')

                self.send_file_response(dest)
                return
        if self.path.startswith('/LADXR/gfx/'):
            # We are serving from LADXR/www/, but graphics are outside
            # our scope at LADXR/gfx/, so serve graphics manually:
            filename = os.path.join(
                BASE_DIR, self.path.removeprefix('/LADXR/'))
            self.send_file_response(filename)
            return
        else:
            # Serve directly from LADXR/www/
            return super().do_GET()


class ServerThread(threading.Thread):
    """Run TCP serven in a background thread so that we can launch a web
    browser in the main thread.
    """

    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        with socketserver.TCPServer(('', args.port), LADXRHandler) as httpd:
            httpd.serve_forever()


if __name__ == '__main__':
    try:
        thread = ServerThread()
        thread.start()
        url = f'http://localhost:{args.port}'
        print('If your browser doesn\'t open automatically, visit:')
        print(url)
        webbrowser.open(url)
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting threads.')
