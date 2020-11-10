from datetime import datetime


class ComboReader:
    def __init__(self):
        self.credentials = {}

    def read(self, combo):
        self.credentials.update({email : password for email, password in map( lambda x: x.replace("\n", "").split(':'), open(combo, 'r').readlines() )})
        return self.credentials

class ComboWriter:
    def __init__(self, path='success/'):
        self.file = self.open()
        self.path = path

    def success(self, user, pwd):
        self.file.write(user + ":" + pwd + "\n")

    def open(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return open(f"success-{date}", "a")

    def __del__(self):
        self.file.close()

