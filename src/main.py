from http.server import HTTPServer
from loguru import logger
from datetime import datetime
from os import makedirs
from os.path import exists, join

from RequestsHandler import RequestHandler


def run(server_class=HTTPServer, handler_class=RequestHandler):
    PORT = 65525
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    logger.debug("Server started on port", PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    if not exists("../logs"):
        makedirs("../logs")
    logger.add(join("../logs", f"log_{datetime.today().strftime('%Y-%m-%d')}.log"), rotation="1 day")
    run()
