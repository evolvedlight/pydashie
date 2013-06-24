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

            #'assets/javascripts/dashing.coffee',
            'assets/javascripts/dashing.gridster.coffee',

            'assets/javascripts/jquery.knob.js',
            'assets/javascripts/rickshaw.min.js',
            #'assets/javascripts/application.coffee',
            'assets/javascripts/app.js',
        ]
        nizzle = True
        if not nizzle:
            scripts = ['assets/javascripts/application.js']

        output = []
        for path in scripts:
            output.append('// JS: %s\n' % path)
            if '.coffee' in path:
                print('Compiling Coffee for %s ' % path)
                contents = coffeescript.compile_file(path)
            else:
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        if nizzle:
            f = open('/tmp/foo.js', 'w')
            for o in output:
                print >> f, o
            f.close()

            f = open('/tmp/foo.js', 'rb')
            output = f.read()
            f.close()
            current_app.javascripts = output
        else:
            current_app.javascripts = ''.join(output)

    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        'assets/stylesheets/application.css',
    ]
    output = ''
    for path in scripts:
        output = output + open(path).read()
    return Response(output, mimetype='text/css')

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join('assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    html = '%s.html' % widget_name
    path = os.path.join('widgets', widget_name, html)
    if os.path.isfile(path):
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
