from flask import Flask
from multiprocessing import Process

class Artist(object):

    def __init__(self, diary):

        self.diary = diary
        
        app = Flask(__name__)
            
        @app.route('/')
        def index():
            return "Commencing awesomeness."

        # Assign to self, so other methods can interact with it.
        self.app = app

    def start(self):
        #self.app.run()
        self.flask_ps = Process(target=self.app.run)
        self.flask_ps.start()

    def stop(self):
        print "[!] Telling the artist to pack his things.."
        self.flask_ps.terminate()
