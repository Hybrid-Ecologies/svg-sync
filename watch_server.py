import argparse
import os
import io

import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import json

scanner_clients = []

class SVGWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True # accept all cross-origin traffic, not very secure...
    
    def open(self):
        scanner_clients.append(self)
        print("SVGWebSocket opened from: " + self.request.remote_ip)

    def on_message(self, message):
        print(json.loads(message))

    def on_close(self):
        scanner_clients.remove(self)
        print("SVGWebSocket closed from: " + self.request.remote_ip)


if __name__ == "__main__":

    # API
    parser = argparse.ArgumentParser(description='Start the streaming server.')
    parser.add_argument('--port', default=8888, type=int, help='Web server port (default: 8888)')
    args = parser.parse_args()

   
    script_path = os.path.dirname(os.path.realpath(__file__))
    static_path = script_path + '/static/'
  
    app = tornado.web.Application([
            (r"/svg", SVGWebSocket)
        ])

    app.listen(args.port)
    print("Starting server: http://localhost:" + str(args.port) + "/")
    host_ip_address = socket.gethostbyname(socket.gethostname())
    print("Host IP Address: " + host_ip_address)

    try:
        tornado.ioloop.IOLoop.current().start()
        # START OBSERVER

    except KeyboardInterrupt:
        print("Stopping server ...")
        
