from flask import Flask, json, Request, Response

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/db/ping', methods=['POST'])
def ping():
    return json.dumps({"message": "alive"}, sort_keys=False, indent=4), 200

app.run(host='0.0.0.0', port=5000)