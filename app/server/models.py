import socketserver
from app.common import config
from app.common.jim import JIM, JimResponse


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        if JIM.unpack(data):
            self.request.sendall(JimResponse.status_200())


class Server:

    def __init__(self, args, options_file):
        conf = self.__get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']

    def run(self):
        with socketserver.TCPServer((self.host, self.port), Handler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()

    def __get_options(self, args, options_file):
        options = config.get_json_options(options_file)
        cl_options = config.get_command_options(args, "a:p:")
        for opt in cl_options:
            if opt[0] == "-a":
                options['DEFAULT']['HOST'] = opt[1]
            elif opt[0] == "-p":
                options['DEFAULT']['PORT'] = opt[1]
        return options

