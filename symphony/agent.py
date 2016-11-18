#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Purpose:
        Agent API Methods
'''

__author__ = 'Matt Joyce'
__email__ = 'matt.joyce@symphony.com'
__copyright__ = 'Copyright 2016, Symphony'

import ast
import json
import requests


class Agent():

    def __init__(self, url, crt, key, session, keymngr):
        self.__url__ = url
        self.__crt__ = crt
        self.__key__ = key
        self.__session__ = session
        self.__keymngr__ = keymngr

    def test_echo(self, test_string):
        ''' echo test '''

        headers = {'Content-Type': 'application/json',
                   'sessionToken': self.__session__,
                   'keyManagerToken': self.__keymngr__}

        data = '{ "message": "'"%s"'" }' % test_string

        # HTTP POST query to keymanager authenticate API
        try:
            response = requests.post(self.__url__ + 'agent/v1/util/echo',
                                     headers=headers,
                                     data=data,
                                     cert=(self.__crt__, self.__key__),
                                     verify=True)
        except requests.exceptions.RequestException as e:
            print e
            return None
        # load json response as list
        status_code = response.text
        # return the token
        return status_code

    def create_datafeed(self):
        ''' create datafeed '''
        # https://your-pod.symphony.com/:8444/agent/v1/datafeed/create
        headers = {'Content-Type': 'application/json',
                   'sessionToken': self.__session__,
                   'keyManagerToken': self.__keymngr__}

        # HTTP POST query to keymanager authenticate API
        try:
            response = requests.post(self.__url__ + 'agent/v1/datafeed/create',
                                     headers=headers,
                                     cert=(self.__crt__, self.__key__),
                                     verify=True)
        except requests.exceptions.RequestException as e:
            print e
            return None
        # load json response as list
        datafeed = json.loads(response.text)
        # return the token
        return datafeed['id']

    def read_datafeed(self, streamid):
        ''' get datafeed '''
        headers = {'Content-Type': 'application/json',
                   'sessionToken': self.__session__,
                   'keyManagerToken': self.__keymngr__}

        # HTTP POST query to keymanager authenticate API
        try:
            response = requests.get(self.__url__ + 'agent/v2/datafeed/' + str(streamid) + '/read',
                                    headers=headers,
                                    cert=(self.__crt__, self.__key__),
                                    verify=True)
        except requests.exceptions.RequestException as e:
            print e
            return None
        # load json response as list
        datafeed = response.text
        datastat = response.status_code
        if datastat == 200:
            datafeed = ast.literal_eval(datafeed)
        # return the token
        return datafeed, datastat

    def send_message(self, threadid, msgFormat, message):
        ''' send message to threadid/stream '''
        headers = {'content-type': 'application/json',
                   'sessionToken': self.__session__,
                   'keyManagerToken': self.__keymngr__}
        data = '{ "format": "%s", "message": "'"%s"'" }' % (msgFormat, message)
        # HTTP POST query to keymanager authenticate API
        try:
            response = requests.post(self.__url__ + 'agent/v2/stream/' + threadid + '/message/create',
                                     headers=headers,
                                     data=data,
                                     cert=(self.__crt__, self.__key__),
                                     verify=True)
        except requests.exceptions.RequestException as e:
            print e
            return None
        # load json response as list
        string = response.text
        # return the token
        return string
