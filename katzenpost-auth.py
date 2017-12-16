"""
Standalone userdb implementation for Katzenpost server.
"""
import json
from klein import run, route

userdb = {}

PROVIDER = "localhost"
SERVER = "localhost"
PORT = 7900

def success(action):
    return json.dumps({action: True})

def failure(action, message=""):
    return json.dumps(
        {action: False, message: message})


@route('/exists', methods=['POST'])
def exists(request):
    action = 'exists'
    print "ARGS", request.args
    try:
        key = request.args.get('user')[0]
    except Exception:
        key = None
    if not key:
        request.setResponseCode(500)
        return failure('exists', 'no user provided')
    if key not in userdb.keys():
        request.setResponseCode(401)
        return failure(action, 'user does not exist')
    return success(action, 'user exists')


@route('/isvalid', methods=['POST'])
def isvalid(request):
    action = 'isvalid'
    try:
        key = request.args.get('key')[0]
    except Exception:
        key = None
    if not key:
        request.setResponseCode(500)
        return failure(action, 'no key provided')
    if key not in userdb.viewvalues():
        request.setResponseCode(401)
        return failure(action, 'user is not valid')
    return success(action, 'user is valid')


# TODO authenticate
@route('/add', methods=['POST'])
def add(request):
    action = 'add'
    global userdb
    user = request.args.get('user')[0]
    key = request.args.get('key')[0]
    if not user or not key:
        return failure(action)
    try:
        provider = user.split('@')[1]
        if provider != PROVIDER:
            raise TypeError()
    except Exception:
        request.setResponseCode(401)
        return failure(action, 'wrong')
    print "[%s:%s] Added" % (user, key)
    userdb[user] = key
    return success(action, 'user added')


@route('/list')
def list(request):
    action = 'list'
    global userdb
    for k, v in userdb.items():
        print "[%s:%s]" % (k, v)
    return success(action)

@route('/del', methods=['POST'])
def delete(request):
    action = 'del'
    request.setResponseCode(500)
    return failure(action, 'not implemented')

run(SERVER, PORT)
