import os
import pandas as pd
import requests
from flask import Flask, json, Response

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('train/<model>', methods=['POST'])
def train_model(model):
    api = os.environ['DB_API']
    req = requests.get(api)
    data = req.json()
    df = pd.DataFrame.from_dict(data)
    return json.dumps({'message': ' training has started on path ' + str(api)}, sort_keys=False, indent=4), 200



app.run(host='0.0.0.0', port=5000)