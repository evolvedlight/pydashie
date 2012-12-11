import os
import json
import time
import random
import Queue
import datetime
import coffeescript

#from repeated_timer import RepeatedTimer

from flask import Flask, render_template, Response
app = Flask(__name__)

#events_queue = Queue.Queue()

@app.route("/")
def hello():
    return render_template('main.html')

@app.route("/assets/application.js")
def javascripts():
#    scripts = [
#        'assets/javascripts/jquery.js',
#        'assets/javascripts/es5-shim.js',
#        'assets/javascripts/d3.v2.min.js',
#        'assets/javascripts/batman.js',
#        'assets/javascripts/batman.jquery.js',
#        'assets/javascripts/jquery.gridster.js',
#        'assets/javascripts/jquery.leanModal.min.js',
#        'assets/javascripts/dashing.coffee',
#        'assets/javascripts/jquery.knob.js',
#        'assets/javascripts/rickshaw.min.js',
#        'assets/javascripts/application.coffee',
#        'assets/javascripts/dashing.gridster.coffee'
#    ]
    scripts = ['assets/javascripts/application.js']
    
    base_directory = os.getcwd()
    full_paths = [os.path.join(base_directory, script_name) for script_name in scripts]
    output = ''
    for path in full_paths:
        if '.coffee' in path:
            print('Compiling Coffee on %s ' % path)
            output = output + coffeescript.compile(open(path).read())
        else:
            output = output + open(path).read()
    return Response(output, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        'assets/stylesheets/application.css',
    ]
    base_directory = os.getcwd()
    full_paths = [os.path.join(base_directory, script_name) for script_name in scripts]
    output = ''
    for path in full_paths:
        output = output + open(path).read()
    return Response(output, mimetype='text/css')

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    base_directory = os.getcwd()
    path = os.path.join(base_directory, 'widgets', widget_name, '%s.html' % widget_name)
    return open(path).read()

#@app.route('/events')
#def events():
#    print 'In Events'
#    return Response(pop_queue(), mimetype='text/event-stream')
@app.route('/events')
def events():
    def generate():
        while True:
            timeString = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
            yield 'data: {"value":%s,"id":"synergy","updatedAt":"%s"}\n\n' % (random.randint(0, 100), timeString)
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')

#def pop_queue():
#    print 'In Pop Queue'
#    while True:
#        yield sample_widgets()#events_queue.get()
#        time.sleep(2)
#        print 'Read from Queue'
#        
#def sample_widgets():
#    synergy_data = {'value': random.randint(0, 100), 
#                    'id': 'synergy', 
#                    'updateAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')}
#    events_queue.put('data: {%s}\n\n' % (json.dumps(synergy_data)))
#    print 'Put some data in Queue'
#    
if __name__ == "__main__":
    #rt = RepeatedTimer(1, sample_widgets)
    app.run(debug=True, port=5000, threaded=True)
#    try:
#        print 'Before app run'
#        
#    finally:
#        pass#rt.stop()
