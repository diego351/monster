from flask import Flask
from flask import render_template
from flask import jsonify
from multiprocessing import Process
from time import sleep
from time import time

class Artist(object):

    def __init__(self, diary):

        self.diary = diary
        
        app = Flask(__name__, template_folder='../assets/templates')
        app.debug = True
        app.diary = diary
            
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/api/load')
        def api_load():
            load_record = app.diary.read_load()
            return jsonify({
                'load': load_record, 
                'l': len(load_record) 
            })

        @app.route('/api/mem_info')
        def api_mem_info():
            mem_info_record = app.diary.read_mem_info()
            return jsonify({
                'mem_info': mem_info_record,
                'l': len(mem_info_record)
            })

        # Assign to self, so other methods can interact with it.
        self.app = app

    def start(self):
        self.flask_ps = Process(target=self.app.run)
        self.flask_ps.start()

    def stop(self):
        print "Stop called @", time()
        sleep(1)
        print "[!] Telling the artist to pack his things.."
        self.flask_ps.terminate()
