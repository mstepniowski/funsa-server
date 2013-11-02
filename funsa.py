import redis
import json
from flask import Flask, request, abort


app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
app.debug = True


@app.route('/<uid>/inbox', methods=['GET', 'POST'])
def inbox(uid):
    if '#' in uid:
        abort(400)

    if request.method == 'POST':
        if not request.json or not 'sender' in request.json or not 'message' in request.json:
            abort(400)
        r.rpush('%s#inbox' % uid,
                '%s#%s' % (request.json['sender'], request.json['message']))
        return '{"status": "ok"}', 200
    else:
        result = []
        for c in range(10):
            blob = r.lpop('%s#inbox' % uid)
            if blob is None:
                break
            sender, message = blob.split('#', 1)
            print sender, message
            result.append({'sender': sender, 'message': message})
            print result
        return json.dumps(result)


if __name__ == '__main__':
    app.run()
