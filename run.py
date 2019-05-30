import json
import time
import random
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

ACTIONS = ['get', 'set', 'ping']


def parse_request(bundle):
    try:
        result = json.loads(bundle, encoding='utf-8')
    except Exception:
        result = None
    return result


def make_response(type, errno, msg, data=None, str_mode=False):
    response = {
        'type': str(type),
        'error': errno,
        'msg': msg,
        'data': '' if data is None else data
    }
    return str(json.dumps(response)) if str_mode else json.dumps(response)


def do_action(inst, bundle):
    action = None
    data = None
    try:
        action = bundle['action']
        data = bundle['data']
    except Exception as e:
        inst.sendMessage(make_response('common', -1, 'Bad request'))
    if action is not None:
        if action not in ACTIONS:
            inst.sendMessage(make_response('common', -1, 'Unknown action'))
        else:
            try:
                if action == 'get':
                    if data['type'] == 'temp':
                        inst.sendMessage(make_response('temp', 0, 'success', {
                            'id:': 1,
                            'value': random.randint(0, 1000) / 10
                        }))
                    elif data['type'] == 'humi':
                        inst.sendMessage(make_response('humi', 0, 'success', {
                            'id:': 1,
                            'value': random.randint(0, 1000) / 10
                        }))
                    elif data['type'] == 'illu':
                        inst.sendMessage(make_response('illu', 0, 'success', {
                            'id:': 1,
                            'value': random.randint(0, 1000)
                        }))
                elif action == 'set':
                    inst.sendMessage(make_response('set', 0, 'success'))
                elif action == 'ping':
                    inst.sendMessage(make_response('pong', 0, 'pong'))
            except Exception:
                inst.sendMessage(make_response('common', -1, 'Missing argument'))


class CoreServer(WebSocket):

    def handleMessage(self):
        data = parse_request(self.data)
        if data is None:
            self.sendMessage(make_response('common', -1, 'Invalid request'))
        else:
            do_action(self, data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


if __name__ == '__main__':
    print('Initializing...')
    server = SimpleWebSocketServer('0.0.0.0', 18770, CoreServer)
    time.sleep(0.5)
    print('Server is listening...')
    server.serveforever()
