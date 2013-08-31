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
        app.diary = diary

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/api/load')
        def api_load():
            load_record = app.diary.read('LoadAvg')
            return jsonify({
                'load': load_record, 
                'l': len(load_record) 
            })

        @app.route('/api/mem_info')
        def api_mem_info():
            mem_info_record = app.diary.read('MemInfo')
            return jsonify({
                'mem_info': mem_info_record,
                'l': len(mem_info_record)
            })

        @app.route('/api/apache')
        def api_apache():
            apache_activity = app.diary.read('Apache2')
            return jsonify({
                'apache_activity': apache_activity,
                'l': len(apache_activity),
            })

        @app.route('/api/postgres')
        def api_postgres():
            postgres_stats = app.diary.read('Postgres')
            return jsonify({
                'postgres_stats': postgres_stats,
                'l': len(postgres_stats)
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
