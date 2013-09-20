from example_samplers import *

def run(app, xyzzy):
    samplers = [
        SynergySampler(xyzzy, 3),
        BuzzwordsSampler(xyzzy, 2), # 10
        ConvergenceSampler(xyzzy, 1),
    ]

    try:
        app.run(debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print "Disconnecting clients"
        xyzzy.stopped = True
        
        print "Stopping %d timers" % len(samplers)
        for (i, sampler) in enumerate(samplers):
            sampler.stop()

    print "Done"
