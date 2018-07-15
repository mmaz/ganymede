import json as _json
import datetime as _datetime
import random as _random
import warnings as _warnings
with _warnings.catch_warnings():
    _warnings.simplefilter("ignore")
    import requests as _requests

HOST = '0.0.0.0'
SUBMITTER = "YOUR NAME HERE"

class JKeys:
    PROBLEMID = 'problemid'
    DATETIME  = 'datetime'
    SUBMITTER = 'submitter'
    STATUS    = 'status'
class JStates:
    ATTEMPTED = 'attempted'
    COMPLETED = 'completed'

def name(yourname):
    global SUBMITTER
    if not isinstance(yourname, str):
        return
    SUBMITTER = yourname
    return

def configure(host):
    global HOST
    if not isinstance(host, str):
        return
    HOST=host
    return

def update(pid, b):
    if not (isinstance(b, bool) and isinstance(pid, int)):
        return
    msg = {}
    msg[JKeys.PROBLEMID] = pid
    msg[JKeys.SUBMITTER] = SUBMITTER
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

