class Proxy:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.fails = 0 # Set default