import SimpleHTTPServer
import SocketServer

port = 8002

handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("",port), handler)

print "serving at localhost:{0}".format(port)
httpd.serve_forever()
