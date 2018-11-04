#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse

curdir = path.dirname(path.realpath(__file__))
sep = '/'

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
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
        "哈哈，这就比较尴尬了",
        "操你妈",
        "你麻痹"
    ])

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        self.handle_http_get()

    def do_POST(self):
        self.handle_http_request();

    def handle_http_get(self):
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        if(query == None):
            self.send_error(404, 'File Not Found: %s' % self.path)

        response = my_bot.get_response(query)
        print(response.text)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(response.text.encode("UTF-8"))


    def handle_http_request(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query

        if filepath.endswith(".html"):
            mimetype = 'text/html'
            sendReply = True
        if filepath.endswith(".jpg"):
            mimetype = 'image/jpg'
            sendReply = True
        if filepath.endswith(".gif"):
            mimetype = 'image/gif'
            sendReply = True
        if filepath.endswith(".js"):
            mimetype = 'application/javascript'
            sendReply = True
        if filepath.endswith(".css"):
            mimetype = 'text/css'
            sendReply = True
        if filepath.endswith(".json"):
            mimetype = 'application/json'
            sendReply = True
        if filepath.endswith(".woff"):
            mimetype = 'application/x-font-woff'
            sendReply = True
        if sendReply == True:
            # Open the static file requested and send it
            try:
                with open(path.realpath(curdir + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


def run():
    port = 8000
    print('starting server, port', port)


    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
