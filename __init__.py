import json as _json
import datetime as _datetime
import requests as _requests
import random as _random

HOST = '0.0.0.0'

class JKeys:
    PROBLEMID = 'problemid'
    DATETIME  = 'datetime'
    SUBMITTER = 'submitter'
    STATUS    = 'status'
class JStates:
    ATTEMPTED = 'attempted'
    COMPLETED = 'completed'

def configure(host):
    global HOST
    if not isinstance(host, str):
        return
    HOST=host
    return

def update(submitter, pid, b):
    if not (isinstance(submitter, str) and isinstance(b, bool) and isinstance(pid, int)):
        return
    msg = {}
    msg[JKeys.PROBLEMID] = pid
    msg[JKeys.SUBMITTER] = submitter
    endpoint = "http://{}:9876/submit".format(HOST)
    msg[JKeys.DATETIME] = _datetime.datetime.now().strftime('%h %d %Y at%I:%M:%S%P')
    if b:
        msg[JKeys.STATUS] = JStates.COMPLETED
    else:
        msg[JKeys.STATUS] = JStates.ATTEMPTED
    try:
        _requests.post(endpoint, json=msg)
    except:
        pass

