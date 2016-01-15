import http.server
import sys
import socket
import itertools


HOST_NAME = ''
PORT_NUMBER = 8080

def getLocalIP():
    return list(itertools.chain(
            *[l for l in (
                [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], 
                [[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
            ) if l]
        ))

class LocalInfoHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.send("<html><head><title>Local info</title></head>")
        s.send("<body>")
        s.send("<p>You accessed path: %s</p>" % s.path)
        version = sys.version_info
        s.send("<p>Python version: %s.%s.%s</p>" %(version.major, version.minor, version.micro))
        s.send("<p>Local time: %s</p>" % s.date_time_string())
        s.send("<p>Local interfaces: %s</p>" % getLocalIP())
        s.send("<p>Your address and port are: %s</p>" % str(s.client_address))
        s.send("</body></html>")
    def send(s, dataString):
        s.wfile.write(dataString.encode())

if __name__ == '__main__':
    print "Local interfaces: %s" % getLocalIP()
    httpd = http.server.HTTPServer((HOST_NAME, PORT_NUMBER), LocalInfoHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
