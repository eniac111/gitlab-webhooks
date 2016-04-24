# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import json

try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from .git import Repository


def start(configs, host="", port=8000):
    try:
        server = HTTPServer((host, port), GitlabWebhookHandler)
        server.context = configs
        configs.logger.info("GitLab webhooks server is starting...")
        server.serve_forever()
    except KeyboardInterrupt:
        configs.logger.info("GitLab webhooks server is shutting down.")
    finally:
        server.server_close()


class GitlabWebhookHandler(BaseHTTPRequestHandler):
    RESPONSE_MESSAGE = "Python GitLab webhook handler"

    @property
    def context(self):
        return self.server.context

    def do_POST(self):
        data_size = int(self.headers["Content-Length"])
        data = self.rfile.read(data_size)
        repo_url = "http://git.lo/blago/it-dns"
        repo = Repository("http://git.lo/blago/it-dns.git")
        repo.pull(branch="master")
        #json_data = json.loads(data.decode("utf-8"))

        #try:
        #    self.handle_commits_data(json_data)
        #except Exception as e:
        #    self.context.logger.exception("Error during parsing of data", json_data)
        #    self._send_response_message(self.RESPONSE_MESSAGE, status_code=500)
        #else:
        #    self._send_response_message(self.RESPONSE_MESSAGE)

#    def handle_commits_data(self, commits_json):
#        repo_url = commits_json["repository"]["homepage"]
#        repo_data = self.context.find_repo(repo_url)
#        if repo_data is None:
#            raise Exception("No configuration found for repository.", repo_url)
#
#        repo = Repository(repo_data["path"])
#        repo.pull(branch=repo_data.get("branch"))

    def _send_response_message(self, message, status_code=200):
        message = message.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def log_message(self, *args, **kwargs):
        self.context.logger.info(*args, **kwargs)
