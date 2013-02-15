import os
import json
import Queue
import random
import logging
import datetime
import collections
import coffeescript
import SocketServer
from repeated_timer import RepeatedTimer
from flask import Flask, render_template, Response, send_from_directory, request, current_app

app = Flask(__name__)

events_queue = {}
items = collections.deque()
last_events = {}
seedX = 0

@app.route("/")
def hello():
    return render_template('main.html', title='pyDashie')

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

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join(os.getcwd(), 'assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    base_directory = os.getcwd()
    path = os.path.join(base_directory, 'widgets', widget_name, '%s.html' % widget_name)
    return open(path).read()

@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_event_queue = Queue.Queue()
    events_queue[event_stream_port] = current_event_queue
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(events_queue)))
    
    #Start the newly connected client off by pushing the current last events
    for event in last_events.values():
        print 'Pushed %s' % event
        current_event_queue.put(event)
    return Response(pop_queue(current_event_queue), mimetype='text/event-stream')

def pop_queue(current_event_queue):
    while True:
        data = current_event_queue.get()
        print 'Popping data %s' % data
        yield data
        
def send_event(widget_id, body):
    body['id'] = widget_id
    body['updateAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
    formatted_json = 'data: %s\n\n' % (json.dumps(body))
    last_events[widget_id] = formatted_json
    for event_queue in events_queue.values():
        event_queue.put(formatted_json)
    
def sample_synergy():
    synergy_data = {'value': random.randint(0, 100)}
    send_event('synergy', synergy_data)                
    
def sample_buzzwords():
    my_little_pony_names = ['Rainbow Dash',
                            'Blossomforth',
                            'Derpy',
                            'Fluttershy',
                            'Lofty',
                            'Scootaloo',
                            'Skydancer']
    items = [{'label': pony_name, 'value': random.randint(0, 20)} for pony_name in my_little_pony_names]
    buzzwords_data = {'items':items}
    send_event('buzzwords', buzzwords_data)

def sample_convergence():
    global seedX
    if not seedX:
        seedX = 0
    items.append({'x':seedX, 
                  'y':random.randint(0,20)})
    seedX += 1
    if len(items) > 10:
        items.popleft()
    item_data = {'points': list(items)}
    send_event('convergence', item_data)

def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    del events_queue[event_stream_port]
    print('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(events_queue)))

if __name__ == "__main__":
    SocketServer.BaseServer.handle_error = close_stream
    
    refreshJobs = [
        (sample_synergy, 1,),
        (sample_buzzwords, 30,),
        (sample_convergence, 1,),
    ]

    timers = [RepeatedTimer(time, function) for function, time in refreshJobs]
    
    try:
        app.run(debug=True, port=5000, threaded=True, use_reloader=False, use_debugger=True)
    finally:
        for timer in timers:
            timer.stop()
