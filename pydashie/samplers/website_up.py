from pydashie.dashie_sampler import DashieSampler

import requests

class WebsiteUpSampler(DashieSampler):
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
        self._last = 0
        self.page = 'http://www.google.com'

    def name(self):
        return 'website_up'

    def sample(self):
        try:
            r = requests.get(self.page)
            assert r.status_code == 200
            up='UP'
        except:
            up='DOWN'
        s = {'text':up}
        return s