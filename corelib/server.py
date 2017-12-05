import socketserver
from corelib import config
from corelib import jim


class MessengerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class MessengerServer:

    def __init__(self, args, options_file):
        conf = self.__get_options(args, options_file)
        self.host = conf['DEFAULT']['HOST']
        self.port = conf['DEFAULT']['PORT']

    def run(self):
        with socketserver.TCPServer((self.host, self.port), MessengerHandler) as server:
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

    def response_200(self):
        msg = {
            "response": 200,
            "alert": "Необязательное сообщение/уведомление"
        }
        return jim.pack(msg)

    def response_402(self):
        msg = {
            "response": 402,
            "error": "This could be wrong password or no account with that name"
        }
        return jim.pack(msg)

    def response_409(self):
        msg = {
            "response": 409,
            "alert": "Someone is already connected with the given user name"
        }
        return jim.pack(msg)
