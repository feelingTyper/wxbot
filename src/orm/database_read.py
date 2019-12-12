import pymysql


class DatabaseRead:
    def __init__(self,
                 hostname,
                 user,
                 password,
                 database,
                 port,
                 charset,
                 timeout):
        self.db = None
        self.hostname = hostname
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.timeout = timeout

    def connect(self):
        self.db = pymysql.connect(host=self.hostname,
                user=self.user,
                password=self.password,
                db=self.database,
                port=self.port,
                charset=self.charset,
                connect_timeout=self.timeout,
                cursorclass=pymysql.cursors.DictCursor)
