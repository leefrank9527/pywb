# import sys
#
# sys.tracebacklimit = 0
from gevent.monkey import patch_all

patch_all()
from gunicorn.app.base import BaseApplication
from pywb.apps.frontendapp import FrontEndApp


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    print("Detected Linux, Running Gunicorn")
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '5001'),
        'workers': 1,
        # 'threads': number_of_workers(),
        'timeout': 120,
    }
    app = FrontEndApp()
    StandaloneApplication(app, options).run()
