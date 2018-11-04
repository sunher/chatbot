#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import json



my_bot = ChatBot("Training demo")
my_bot.set_trainer(ListTrainer)
my_bot.train([
    "你叫什么名字？",
    "我叫ChatterBot。",
    "今天天气真好",
    "是啊，这种天气出去玩再好不过了。",
    "那你有没有想去玩的地方？",
    "我想去有山有水的地方。你呢？",
    "没钱哪都不去",
    "哈哈，这就比较尴尬了"
])
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        msg = json.loads(post_data.decode('utf-8'))["message"]
        message = my_bot.get_response(msg).text
        self._set_response()
        self.wfile.write(message.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting http...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()