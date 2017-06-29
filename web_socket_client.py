#!/usr/bin/env python3

'''
setup installing the python modules
sudo -H pip3 install bottle gevent gevent-websocket

setup running the server process
python3 web_socket_client.py
'''

from bottle import request, Bottle, abort

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def main ():
    ''' Main function. '''
    app = Bottle()

    class Handler(object):
        '''
        Sockets handlers.
        '''
        def __init__(self):
            self.sockets = []

        def handle_websocket(self):
            '''
            Handle websockets.
            '''
            wsock = request.environ.get('wsgi.websocket')
            if not wsock:
                abort(400, 'Expected WebSocket request.')

            self.sockets += [wsock]

            while True:
                try:
                    message = wsock.receive()
                except WebSocketError as wse:
                    dir(wse)
                
                try:
                    for wsocki in self.sockets:
                        wsocki.send("Your message was: %r" % message)
                except WebSocketError as wse:
                    dir(wse)

    handler = Handler()

    @app.route('/websocket')
    def handle():
        ''' utility '''
        handler.handle_websocket()


    server = WSGIServer(("0.0.0.0", 8080), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
