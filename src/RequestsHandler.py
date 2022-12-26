import cgi
from http.server import BaseHTTPRequestHandler
from SpeakerRecognizer import SpeakerRecognizer
from loguru import logger


class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond(400, 'text/html', 'Cannot GET')

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if not pdict.get('boundary'):
            return self.respond(status=500, response_text='boundary problem')
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['CONTENT-LENGTH'] = content_len
        if ctype == 'multipart/form-data':
            data = cgi.parse_multipart(self.rfile, pdict)
            nickname = data.get('nickname', [False])[0]
            message = data.get('message', [False])[0]
            if not all([nickname, message]):
                logger.error(f"One of arguments is empty! - nickname: {nickname}, message: {message}")
                return self.respond(status=400, response_text='nickname and message expected')
            if "spk" in data:
                speaker_recognizer = SpeakerRecognizer()
                speaker = speaker_recognizer.recognize(data.get("spk"))
            logger.debug(f"Received new message \"{message}\" from {nickname}")
            logger.debug(f"Speaker - {speaker}")
            self.respond(response_text=f"{nickname} - {message}")

    def handle_http(self, status, content_type, response_text):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(response_text, "UTF-8")

    def respond(self, status=200, content_type='text/html', response_text="ok"):
        content = self.handle_http(status, content_type, response_text)
        self.wfile.write(content)
