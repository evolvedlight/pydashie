import os
from flask import Flask, render_template, Response, send_from_directory, request, current_app

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html', title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, 'javascripts'):
        import coffeescript
        scripts = [
            'assets/javascripts/jquery.js',
            'assets/javascripts/es5-shim.js',
            'assets/javascripts/d3.v2.min.js',
            'assets/javascripts/batman.js',
            'assets/javascripts/batman.jquery.js',
            'assets/javascripts/jquery.gridster.js',
            'assets/javascripts/jquery.leanModal.min.js',
            'assets/javascripts/dashing.coffee',
            'assets/javascripts/jquery.knob.js',
            'assets/javascripts/rickshaw.min.js',
            'assets/javascripts/application.coffee',
            'assets/javascripts/dashing.gridster.coffee'
        ]
        scripts = ['assets/javascripts/application.js']

        base_directory = os.getcwd()
        full_paths = [os.path.join(base_directory, script_name) for script_name in scripts]
        output = []
        for path in full_paths:
            print path
            if '.coffee' in path:
                print('Compiling Coffee for %s ' % path)
                contents = coffeescript.compile_file(path)
            else:
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        current_app.javascripts = ''.join(output)

    return Response(current_app.javascripts, mimetype='application/javascript')

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
    html = '%s.html' % widget_name
    base_directory = os.getcwd()
    path = os.path.join(base_directory, 'widgets', widget_name, html)
    if os.path.exists(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents

import Queue

class Z:
    pass
xyzzy = Z()
xyzzy.events_queue = {}
xyzzy.last_events = {}

@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_event_queue = Queue.Queue()
    xyzzy.events_queue[event_stream_port] = current_event_queue
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(xyzzy.events_queue)))

    #Start the newly connected client off by pushing the current last events
    for event in xyzzy.last_events.values():
        #print 'Pushed %s' % event
        current_event_queue.put(event)
    #return Response(pop_queue(current_event_queue), mimetype='text/event-stream')

    return Response(xyzzy.last_events.values(), mimetype='text/event-stream')

def pop_queue(current_event_queue):
    while True:
        data = current_event_queue.get()
        print 'Popping data %s' % data
        yield data

def close_stream(*args, **kwargs):
    print 'close_stream'
    event_stream_port = args[2][1]
    del events_queue[event_stream_port]
    print('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(events_queue)))

if __name__ == "__main__":
    import SocketServer
    SocketServer.BaseServer.handle_error = close_stream

    import example_app
    example_app.run(app, xyzzy)
