#!/usr/bin/env python
from __future__ import with_statement
from httplib2 import Http
from urllib import urlencode

import random
from protobufparser import pprint

def to_varint(value):
    ret = []
    bits = value & 0x7f
    value >>= 7
    while value:
        ret.append(chr(0x80|bits))
        bits = value & 0x7f
        value >>= 7
    ret.append(chr(bits))
    return ''.join(ret)

def encode_image(image):
    trailingBytes = "\x18\x4B\x20\x01\x30\x00\x92\xEC\xF4\x3B\x09\x18\x00\x38\xC6\x97\xDC\xDF\xF7\x25\x22\x00"
    size = len(image)
    x = to_varint(size)
    a = to_varint(size + 32)
    b = to_varint(size + 14)
    c = to_varint(size + 10)
    return "\x0A"+a+"\x0A"+b+"\x0A"+c+"\x0A"+x+image+trailingBytes

def gen_cssid():
    return "".join([random.choice(['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']) for i in xrange(16)])

class Goggles:
    def __init__(self):
        self.headers = {"Content-Type": "application/x-protobuffer", "Pragma": "no-cache"}
        self.url = "http://www.google.com/goggles/container_proto?cssid=%s"
        # the following string contains some magic ints and "iPhone OS 4.1 iPhone3GS" as "user-agent"
        self.activation_magic = "\x22\x00\x62\x3C\x0A\x13\x22\x02\x65\x6E\xBA\xD3\xF0\x3B\x0A\x08\x01\x10\x01\x28\x01\x30\x00\x38\x01\x12\x1D\x0A\x09\x69\x50\x68\x6F\x6E\x65\x20\x4F\x53\x12\x03\x34\x2E\x31\x1A\x00\x22\x09\x69\x50\x68\x6F\x6E\x65\x33\x47\x53\x1A\x02\x08\x02\x22\x02\x08\x01"
        self.init_cssid()

    def init_cssid(self):
        self.cssid = gen_cssid()
        h = Http()
        h.request("http://www.google.com/goggles/container_proto?cssid="+self.cssid, "POST", self.activation_magic,headers={"Content-Type": "application/x-protobuffer", "Pragma": "no-cache"})
                
    def send_image(self, image):
        h = Http()
        resp, content = h.request("http://www.google.com/goggles/container_proto?cssid="+self.cssid, "POST", encode_image(image),headers={"Content-Type": "application/x-protobuffer", "Pragma": "no-cache"})

        if resp['status']=='400':
           print "something's wrong."

        return content

if __name__ == "__main__":
    from optparse import OptionParser
    import sys, re
    usage = "usage: %prog [options] url/path-to-jpeg" 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args)==0:
        print "url or path of jpeg needed"
        sys.exit(1)
    if args[0].startswith("http"):
        img = ul.urlopen(args[0]).read()
    else:
        with open(args[0]) as jpg:
            img = jpg.read()
    if len(img)>140000:
        print "jpeg should be smaller than 140KB"
        sys.exit(1)
    g = Goggles()
    res = g.send_image(img)
    pprint(res)
    sys.exit()
