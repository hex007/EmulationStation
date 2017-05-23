#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(saket)--(RiPlayServer)--(30/06/16 15:55)--(【ツ】)---
# `--(~/network.py$)--> 
import urllib2


__tag__ = 'network'


def get_page(request):
    connection = urllib2.urlopen(request)
    headers = connection.info()
    response = connection.read()

    print '<<<<<<<<<<<<<<<<<<'
    print connection.geturl()
    print 'HTTP', connection.getcode()
    print connection.info()
    print '<<<<<<<<<<<<<<<<<<'
    return headers, response


class MyRequest(urllib2.Request):
    def __init__(self, url, **args):
        urllib2.Request.__init__(self, url)
        if 'data' in args:
            self.add_data(args['data'])
        if 'cookie' in args:
            self.add_header('cookie', args['cookie'])

        self.response_headers = None
        self.response_content = None
        self.connection = None
        self.error = None


    def get_page(self):
        try:
            self.connection = urllib2.urlopen(self)
            self.response_headers = self.connection.info()
            self.response_content = self.connection.read()
            return self
        except urllib2.HTTPError as error:
            self.error = error
            print ("HTTP Error received: %d" % error.code) if error else "Unable to make connection"
            print error.message
            return error.code if error else None
        except Exception as error:
            self.error = error
            print ("Error received: %r" % error) if error else "Unable to make connection"
            print error.message
            return None
