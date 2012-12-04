import os
import time
import random
import datetime
import coffeescript

from flask import Flask, render_template, Response
app = Flask(__name__)

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

@app.route('/events')
def events():
    def generate():
        while True:
            timeString = datetime.datetime.now().strftime('%F %T +0000')
            yield 'data: {"value":%s,"id":"synergy","updatedAt":"%s"}\n\n' % (random.randint(0, 100), timeString)
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')
        
if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
