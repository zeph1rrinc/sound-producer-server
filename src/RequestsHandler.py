import cgi
from http.server import BaseHTTPRequestHandler
from loguru import logger

from utils import recognize


class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond(400, 'text/html', 'Cannot GET')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
        if ctype == 'multipart/form-data':
            data = cgi.parse_multipart(self.rfile, pdict)
            nickname = data.get('nickname', [False])[0]
            file = data.get('upload_file', [False])[0]
            size = data.get('size', [False])[0]
            if not all([nickname, file, size]):
                logger.error("One of arguments is empty!")
                return self.respond(status=400, response_text='nickname and upload_file expected')
            rec_result = recognize(size, file, nickname)
            if not rec_result:
                return self.respond(status=400, response_text="Empty record!")
        self.respond()

    def handle_http(self, status, content_type, response_text):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_text, "UTF-8")

    def respond(self, status=200, content_type='text/html', response_text="ok"):
        content = self.handle_http(status, content_type, response_text)
        self.wfile.write(content)
