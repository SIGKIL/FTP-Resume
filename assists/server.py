from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pathlib import Path
BASE_DIR = Path(__file__).parent
authorizer = DummyAuthorizer()
authorizer.add_user("user1", "blabla", BASE_DIR)
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("192.168.1.100", 2121), handler)
server.serve_forever()