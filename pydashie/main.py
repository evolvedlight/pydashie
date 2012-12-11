import os
import json
import random
import Queue
import datetime
import collections
import coffeescript

from repeated_timer import RepeatedTimer

from flask import Flask, render_template, Response
app = Flask(__name__)

events_queue = Queue.Queue()
items = collections.deque()
seedX = 0

@app.route("/")
def hello():
    return render_template('main.html', title='pyDashie Dashboard')

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


@app.route('/events')
def events():
    return Response(pop_queue(), mimetype='text/event-stream')

def pop_queue():
    while True:
        yield events_queue.get()
        
def sample_synergy():
    synergy_data = {'value': random.randint(0, 100), 
                    'id': 'synergy', 
                    'updateAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')}
    formatted_json = 'data: %s\n\n' % (json.dumps(synergy_data))
    events_queue.put(formatted_json)
    
def sample_buzzwords():
    items = [
             {'label': 'Test',
              'value': random.randint(0, 20)},
             {'label': 'Test2',
              'value': random.randint(0, 20)},
             ]
    item_data = {'items': items, 
                    'id': 'buzzwords', 
                    'updateAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')}
    formatted_json = 'data: %s\n\n' % (json.dumps(item_data))
    events_queue.put(formatted_json)

def sample_convergence():
    print 'Added convergence'
    global seedX
    if not seedX:
        seedX = 0
    items.append({'x':seedX, 
                  'y':random.randint(0,20)})
    seedX += 1
    if len(items) > 10:
        items.popleft()
    item_data = {'points': list(items), 
                    'id': 'convergence', 
                    'updateAt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')}
    formatted_json = 'data: %s\n\n' % (json.dumps(item_data))
    events_queue.put(formatted_json)
    
if __name__ == "__main__":
    rt = RepeatedTimer(1, sample_synergy)
    rt2 = RepeatedTimer(1, sample_buzzwords)
    rt3 = RepeatedTimer(1, sample_convergence)
    try:
        print 'Before app run'
        app.run(debug=True, port=5000, threaded=True)
    finally:
        rt.stop()
        rt2.stop()
        rt3.stop()