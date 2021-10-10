import pyrebase


class Config_firebase:
    def __init__(self, path_db):
        self.path_db = path_db

    def database_fb(self):
        firebase = self.path_db
        config = pyrebase.initialize_app(firebase)
        db = config.database()
        return db
