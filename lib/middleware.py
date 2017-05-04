#-*- coding: utf-8 -*-
import gzip,zlib
from six import BytesIO

def gzips(response):
    print("start gzips")
    content=response
    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(
        mode='wb',
        compresslevel=4,
        fileobj=gzip_buffer
    )
    gzip_file.write(content)
    gzip_file.close()
    gzip_data = gzip_buffer.getvalue()
    return gzip_data

def deflated(response):
    print("start deflate")
    return zlib.compress(response)