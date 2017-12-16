"""
Standalone userdb implementation for Katzenpost server.
"""
import json
from klein import run, route

userdb = {}

PROVIDER = "idefix"
SERVER = "0.0.0.0"
PORT = 7900


def success(action):
    return json.dumps({action: True})

def failure(action, request, message="", code=401):
    request.setResponseCode(code)
    return json.dumps(
        {action: False, 'message': message})


@route('/exists', methods=['POST'])
def exists(request):
    action = 'exists'
    print "ARGS", request.args
    try:
        key = request.args.get('user')[0]
    except Exception:
        key = None
    if not key:
        return failure(
            action, request, 'no user provided', 400)
    if key not in userdb.keys():
        return failure(action, request, 'user does not exist', 400)
    return success(action)


@route('/isvalid', methods=['POST'])
def isvalid(request):
    action = 'isvalid'
    try:
        key = request.args.get('key')[0]
    except Exception:
        key = None
    if not key:
        return failure(action, request, 'no key provided', 500)
    if key not in userdb.viewvalues():
        return failure(action, request, 'user is not valid', 401)
    return success(action)


# TODO authenticate
@route('/add', methods=['POST'])
def add(request):
    action = 'add'
    global userdb
    print "ARGS", request.args
    user = request.args.get('user')[0]
    key = request.args.get('key')[0]
    if not user or not key:
        return failure(action, request)
    if user in userdb.keys():
        return failure(
            action, request, 'username already registered, and can register only key for now', 401)
    try:
        provider = user.split('@')[1]
        if provider != PROVIDER:
            raise TypeError()
    except Exception:
        return failure(action, request, 'wrong username, does it belong to this provider?', 400)
    print "[%s:%s] Added" % (user, key)
    userdb[user] = key
    return success(action)


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
    return failure(action, request, 'not implemented', 500)

run(SERVER, PORT)
