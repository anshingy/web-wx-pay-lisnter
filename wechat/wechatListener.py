import mitmproxy.http
from mitmproxy import ctx

class wechatListener:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        flow.request.url


addons = [
    wechatListener()
]