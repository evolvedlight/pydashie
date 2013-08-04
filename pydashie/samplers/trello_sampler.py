from pydashie.dashie_sampler import DashieSampler

import random
import trello

class TrelloSampler(DashieSampler):
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
        self._last = 0
        self.key = '0667001bfafc26b53864fd08124159f0'
        self.secret = 'cb6a56444019998b879015c53a17f695700e6dd2f6f147870f27aff89e156c2b'
        self.token= 'b4c5cdbfcda87de13c3a8b487d4c24b0ad9536672e24675d50aa1e08d9d89c67'
        self.api = trello.TrelloApi

    def name(self):
        return 'trello'

    def sample(self):
        s = {'value': 1,
             'current': 2,
             'last': self._last}
        self._last = s['current']
        return s