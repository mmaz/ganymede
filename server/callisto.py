from flask import Flask, request,jsonify
from concurrent.futures import ThreadPoolExecutor, wait
from multiprocessing import Queue
from threading import Lock
import datetime
import time
import argparse
import yaml
import os

class JKeys:
    PROBLEMID = 'problemid'
    DATETIME  = 'datetime'
    SUBMITTER = 'submitter'
    STATUS    = 'status'
class JStates:
    ATTEMPTED = 'attempted'
    COMPLETED = 'completed'

UPDATERATE = 20

app = Flask(__name__)
lock = Lock()
submissions = {} # problemid: (date, name, etc..)
q = Queue()

@app.route("/submit", methods=['POST'])
def submit():
    p = request.get_json()
    pid = p[JKeys.PROBLEMID]
    print("Submission problem ID", pid)
    with lock:
        if pid not in submissions:
            submissions[pid] = {}
        submitter = p[JKeys.SUBMITTER]
        submissions[pid][submitter] = p
    return jsonify()

@app.route('/')
def hello_world():
    return 'CALLISTO'

def printstatus():
    report = []
    report.append('------------{:^30}----------'.format(datetime.datetime.now().strftime('%h %d %Y at %I:%M:%S%P')))
    with lock:
        sorted(submissions) # by key
        for pid in submissions.keys():
            results = submissions[pid]
            ns = len(results)
            nc = len([p for s,p in results.items() if p[JKeys.STATUS] == JStates.COMPLETED])
            na = len([p for s,p in results.items() if p[JKeys.STATUS] == JStates.ATTEMPTED])
            report.append('Problem ID {:4d}: {:4d} submitted, {:4d} completed, {:4d} attempted'.format(pid, ns, nc, na))
    return "\n".join(report)

@app.route('/status')
def status():
    s = printstatus()
    return "<pre>{}</pre>".format(s)

@app.route('/collect')
def collect():
    if KEY == request.args.get('key', ''):
        with open(PATH + os.path.sep + 'result.yml', 'w') as yaml_file:
            with lock:
                sorted(submissions)
                yaml.dump(submissions, yaml_file)
    return 'done'


def statusmonitor():
    while True:
        s = printstatus()
        print(s)
        time.sleep(UPDATERATE)
        
# def j(): return {'problemid':0, 'submitter':'meow', 'datetime':datetime.datetime.now().strftime('%h %d %Y at %I:%M:%S%P'), 'status':'completed'}
def test():
    p1 = {'problemid':0, 'submitter':'meow1', 'datetime':datetime.datetime.now().strftime('%h %d %Y at %I:%M:%S%P'), 'status':'completed'}
    p2 = {'problemid':0, 'submitter':'meow2', 'datetime':datetime.datetime.now().strftime('%h %d %Y at %I:%M:%S%P'), 'status':'completed'}
    p3 = {'problemid':0, 'submitter':'meow3', 'datetime':datetime.datetime.now().strftime('%h %d %Y at %I:%M:%S%P'), 'status':'attempted'}
    with lock:
        submissions[0] = { 'meow1': p1
                         , 'meow2': p2
                         , 'meow3': p3}

KEY = ''
PATH = ''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CALLISTO')
    parser.add_argument('key', metavar='K', type=str)
    parser.add_argument('path', metavar='P', type=str)
    args = parser.parse_args()
    KEY = args.key
    PATH = args.path

    tpool = ThreadPoolExecutor(max_workers=5)
    t = tpool.submit(statusmonitor)
    app.run(port=9876, host='0.0.0.0')