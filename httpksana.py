# -*- coding: utf-8 -*-
from Ksana import Ksana, Response, Responsejson, Responsefile,Redirctresponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from lib import gzips, deflated
import json
import brotli as _brotli
from base64 import b64decode
import asyncio

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

httpksana = Ksana()


def index(request):
    template = env.get_template('index.html')
    response = Response(template.render(), {}, content_type="text/html; charset=utf-8")
    return response


httpksana.route.add(r"^/$", index)


def ip(request):
    ipdict = {"ip": request.ip[0]}
    response = Responsejson(ipdict, {})
    return response


httpksana.route.add(r"^/ip", ip)


def useragent(request):
    useragentdict = {"user-agent": request.headers["User-Agent"]}
    response = Responsejson(useragentdict, {})
    return response


httpksana.route.add(r"^/user-agent", useragent)


def headers(request):
    headersdict = {"headers": request.headers}
    response = Responsejson(headersdict, {})
    return response


httpksana.route.add(r"^/headers", headers)


def get(request):
    getdict = {}
    getdict["args"] = request.args
    getdict["headers"] = request.headers
    getdict["origin"] = request.ip[0]
    getdict["url"] = request.absurl
    response = Responsejson(getdict, {})
    return response


httpksana.route.add(r"^/get", get)


def post(request):
    postdict = {}
    postdict["url"] = request.absurl
    postdict["args"] = request.args
    postdict["headers"] = request.headers
    postdict["origin"] = request.ip[0]
    postdict["formdata"] = request.formdata
    postdict["form"] = request.body
    response = Responsejson(postdict, {})
    return response


httpksana.route.add(r"^/post", post, methods=["POST"])
httpksana.route.add(r"^/patch", post, methods=["PATCH"])
httpksana.route.add(r"^/put", post, methods=["PUT"])
httpksana.route.add(r"^/delete", post, methods=["DELETE"])


def encodingutf8(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/UTF-8-demo.txt", {})
    return response


httpksana.route.add(r"^/encoding/utf8", encodingutf8)


def gzip(request):
    gzipdict = {}
    gzipdict["method"] = request.method
    gzipdict["headers"] = request.headers
    gzipdict["origin"] = request.ip[0]
    gzipdict["gzipped"] = True
    gzipdata = gzips(json.dumps(gzipdict).encode("utf-8"))
    response = Response(gzipdata, {}, encode="gzip")
    return response


httpksana.route.add(r"/gzip", gzip)


def deflate(request):
    deflatedict = {}
    deflatedict["method"] = request.method
    deflatedict["headers"] = request.headers
    deflatedict["origin"] = request.ip[0]
    deflatedict["deflateped"] = True
    deflatedata = deflated(json.dumps(deflatedict).encode("utf-8"))
    response = Response(deflatedata, {}, encode="deflate")
    return response


httpksana.route.add(r"^/deflate", deflate)


def brotli(request):
    brotlidict = {}
    brotlidict["method"] = request.method
    brotlidict["headers"] = request.headers
    brotlidict["origin"] = request.ip[0]
    brotlidict["brotli"] = True
    bytes = json.dumps(brotlidict).encode("utf-8")
    brotlidata = _brotli.compress(bytes)
    response = Response(brotlidata, {}, encode="br")
    return response


httpksana.route.add(r"^/brotli", brotli)

def responseheaders(request):
    response = Responsejson(request.args, {})
    return response

httpksana.route.add(r"^/response-headers", responseheaders)

def redirct_n_times(request,n=1):
    n=int(n)
    if n==1:
        return Redirctresponse("/get")
    else:
        return Redirctresponse("/redirect/{n}".format(n=n-1))
httpksana.route.add(r"^/redirect/(?P<n>.+?)", redirct_n_times)

def redirect_to(request):
    url=request.args.get("url","https://www.baidu.com/")
    print(url)
    return Redirctresponse(url)

httpksana.route.add(r"^/redirect-to",redirect_to)

def cookies(request):
    cookiesdict={}
    cookiesdict["cookies"]=request.cookiedict
    return Responsejson(cookiesdict,{})

httpksana.route.add(r"^/cookies$",cookies)

def cookieset(request):
    setdict=request.args
    print("set")
    response=Redirctresponse("/cookies")
    if setdict:
        for key ,value in setdict.items():
            response.set_cookie(key,value)
        response.body=json.dumps(setdict)
    return response

httpksana.route.add(r"^/cookies/set$",cookieset)

def cookiedelete(request):
    print(request.args)
    names=list(request.args)
    print(names)
    response = Redirctresponse("/cookies")
    if names:
        for name in names:
            response.delete_cookie(name,request,path="/cookies")
    response.body={}
    return response

httpksana.route.add(r"^/cookies/delete$",cookiedelete)

def basic_auth(request,user="user",password="password"):
    print("start auth")
    authorization=request.headers.get("Authorization")
    if authorization and authorization[:6]=="Basic ":
        suser,spassword=b64decode(authorization[6:]).decode("utf-8").split(":",1)
        if suser==user and spassword==password:
            return Redirctresponse("/get")
    response=Response(headers={"WWW-Authenticate": "Basic realm=localhost:8889"},status=401)
    return response

httpksana.route.add(r"^/basic-auth/(?P<user>.*)/(?P<password>.*?)$",basic_auth)

async def delay(request,time):
    await asyncio.sleep(int(time))
    delaydict = {}
    delaydict["args"] = request.args
    delaydict["headers"] = request.headers
    delaydict["origin"] = request.ip[0]
    delaydict["url"] = request.absurl
    response = Responsejson(delaydict, {})
    return response

httpksana.route.add(r"^/delay/(?P<time>.*?)$",delay)

def stream(request,time):
    if int(time)>100:
        time=100
    elif int(time)<0:
        time=0
    delaydict = {}
    delaydict["args"] = request.args
    delaydict["headers"] = request.headers
    delaydict["origin"] = request.ip[0]
    delaydict["url"] = request.absurl
    response=Response("\n".join([json.dumps(delaydict) for i in range(int(time))]))
    return response

httpksana.route.add(r"^/stream/(?P<time>.*?)$",stream)

def html(request):
    response=Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/html.html",content_type="text/html")
    return response

httpksana.route.add(r"^html$",html)

def robot(request):
    response=Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/robots.txt")
    return response

httpksana.route.add(r"^robots.txt$",robot)

def deny(request):
    response=Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/deny.txt")
    return response

httpksana.route.add(r"^deny$",deny)

def links(request,all,index):
    template = env.get_template('Links.html')
    all=[str(i) for i in range(int(all))]
    response = Response(template.render(all=all,index=index), {}, content_type="text/html; charset=utf-8")
    return response

httpksana.route.add(r"^links/(?P<all>.*)/(?P<index>.*)$",links)

def imagejpg(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/image.jpg",content_type="image/jpg",encode=True)
    return response

httpksana.route.add(r"^image/jpg$",imagejpg)

def imagepng(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/image.png", content_type="image/png",encode=True)
    return response

httpksana.route.add(r"^image/png$",imagepng)

def imagejpeg(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/image.jpeg",content_type="image/jpeg",encode=True)
    return response

httpksana.route.add(r"^image/jpeg$",imagejpeg)

def imagewebp(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/image.webp",content_type="image/webp",encode=True)
    return response

httpksana.route.add(r"^image/webp$",imagewebp)

def imagesvg(request):
    response = Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/image.svg",content_type="image/svg+xml",encode=True)
    return response

httpksana.route.add(r"^image/svg$",imagesvg)

def xml(request):
    response=Responsefile("/home/zgy/PycharmProjects/newweb/httpksana/templates/xml.xml",content_type="application/xml")
    return response

httpksana.route.add(r"^xml$",xml)

def form(request):
    template = env.get_template('form.html')
    response = Response(template.render(), {}, content_type="text/html; charset=utf-8")
    return response

httpksana.route.add(r"^form/post$",form)

if __name__ == '__main__':
    httpksana.run(("localhost", 8889))



