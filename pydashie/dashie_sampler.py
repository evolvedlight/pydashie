import datetime
import json
from repeated_timer import RepeatedTimer

class DashieSampler:
    def __init__(self, app, interval):
        self._app = app
        self._timer = RepeatedTimer(interval, self._sample)

    def stop(self):
        self._timer.stop()

    def name(self):
        '''
        Child class implements this function
        '''
        return 'UnknownSampler'

    def sample(self):
        '''
        Child class implements this function
        '''
        return {}

    def _send_event(self, widget_id, body):
        body['id'] = widget_id
        body['updatedAt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0000')
        formatted_json = 'data: %s\n\n' % (json.dumps(body))
        self._app.last_events[widget_id] = formatted_json
        for event_queue in self._app.events_queue.values():
            event_queue.put(formatted_json)

    def _sample(self):
        data = self.sample()
        if data:
            self._send_event(self.name(), data)
