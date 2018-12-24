import mitmproxy.http
from mitmproxy import ctx
import zlib
import json
import requests

class Counter:
    def __init__(self):
        self.url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync'
        self.orderSyncUrl = 'http://127.0.0.1:8000/api/syncOrderStatus'


    # def request(self, flow: mitmproxy.http.HTTPFlow):
    #     ctx.log.info("test url ++++ %s " % flow.request.url)
        
    def txt_wrap_by(self,start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        # ctx.log.info("resp test url ++++ %s " % flow.request.url)
        # ctx.log.info("test resp type ++++{}".format(type(flow.response.data.content).__name__))
        # ctx.log.info("test data  ++++ %s " % flow.response.data.content)
        # ctx.log.info("test data  ++++ %s " % flow.response.raw_content.decode('gbk'))
        # ctx.log.info("test raw_content ++++ %s " % flow.response.raw_content)
        # ctx.log.info("test data  ++++ %s " % flow.response.data.headers.get('Content-Encoding'))
        # html = zlib.decompress(flow.response.data.content, 16+zlib.MAX_WBITS)
        # ctx.log.info("gzip data  ++++ %s " % html.decode("utf8"))
        # 判断监听url
        # ctx.log.info("req  url ++++ %s " % flow.request.url)
        # ctx.log.info("self url ++++ %s " % self.url)
        # ctx.log.info("self url ++++ %s " % flow.request.url.find(self.url))
        if flow.request.url.find(self.url)!=-1:
            ctx.log.info("req url ++++ %s " % flow.request.url)
            # 支付信息为解压类型
            gzipped = flow.response.data.headers.get('Content-Encoding')
            if gzipped:
                html = zlib.decompress(flow.response.data.content, 16+zlib.MAX_WBITS)
                res = html.decode("utf8")
                ctx.log.info("compress gzip data  ++++ %s " % res)
                s1 =json.loads(res)
                
                if s1['AddMsgList']:
                    content =s1['AddMsgList'][0]['Content']
                    MsgType =s1['AddMsgList'][0]['MsgType']
                    ctx.log.info("AddMsgList logic++++ %s " % (MsgType==49))
                    if content and MsgType==49:
                        ctx.log.info("AddMsgList Content++++ %s " % content)
                        #付款备注
                        fkbz = self.txt_wrap_by('付款方备注：','<br/>',content)
                        ctx.log.info("付款方备注：++++ %s " % fkbz)
                        #付款金额
                        fkje = self.txt_wrap_by('收款金额：￥','<br/>',content)
                        ctx.log.info("收款金额：￥ ++++ %s " % fkje)
                        #请求参数
                        reqData = {'trxNo':fkbz,'amount':fkje,'status':'SUCCESS'}
                        #发送同步请求
                        resp = requests.post(self.orderSyncUrl,reqData)
                        ctx.log.info("请求接口返回 ++++ %s " % resp.raw)




addons = [
    Counter()
]