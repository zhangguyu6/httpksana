# HTTKsana 

HTTP server built on [Ksnan](https://github.com/zhangguyu6/ksana) to serve useful endpoints for testing purposes. Its goal is to be as close as possible to [HTTPBin](http://httpbin.org).

## Endpoints

* /    	This page.
* /ip    Returns Origin IP.
* /user-agent    Returns user-agent.
* /headers   Returns header dict.
* /response-headers  Returns given response headers.
* /get  Returns GET data.
* /post  Returns POST data.
* /put  Returns PUT data.
* /patch  Returns PATCH data.
* /delete  Returns DELETE data.
* /encoding/utf8   Returns page containing UTF-8 data.
* /gzip  Returns gzip-encoded data.
* /deflate   Returns deflate-encoded data.
* /brotli  Returns brotli-encoded data.
* /response-headers?key=val  Returns given response headers.
* /redirect/:n   302 Redirects *n* times.
* /redirect-to?url=foo  302 Redirects to the foo URL.
* /relative-redirect/:n  302 Relative redirects  n  times.
* /cookies  Returns cookie data. 
* /cookies/set?name=value Sets one or more simple cookies. 
* /cookies/delete?name1=&name2= Deletes one or more simple cookies.
* /basic-auth/:user/:passwd  Challenges HTTPBasic Auth. default "user":"passwd".
* /delay/:n  Delays responding for  **n** seconds.
* /html Renders an HTML Page.
* /stream/:n  Streams **min(n, 100)** lines.
* /robots.txt  Returns some robots.txt rules. 
* /deny  Denied by robots.txt file.
* /links/:n  Returns page containing **n** HTML links.
* /image/jpg  Returns a jpg image. 
* /image/png  Returns a PNG image. 
* /image/jpeg  Returns a JPEG image. 
* /image/webp Returns a WEBP image. 
* /image/svg  Returns a SVG image.
* /form/post  HTML form that submits to  /post .
* /xml  Returns some XML.

