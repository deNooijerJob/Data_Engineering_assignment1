
import os
import requests
from flask import Flask, json, Response
from simpletransformers.question_answering import QuestionAnsweringModel
from random import sample
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/train/<model_name>', methods=['POST'])
def train_model(model_name):
    api = os.environ['DB_API']
    path = os.environ['MODEL_REPO'] + "/" + model_name

    request_test = requests.get(api)
    train_data = request_test.json()[0][0]
    model = None
    if model_name == "bert":
        if not os.path.exists(path):
            train_args = {
                'learning_rate': 3e-5,
                'num_train_epochs': 2,
                'max_seq_length': 384,
                'doc_stride': 128,
                'overwrite_output_dir': True,
                'reprocess_input_data': False,
                'train_batch_size': 2,
                'gradient_accumulation_steps': 8,
            }

            model = QuestionAnsweringModel(model_name, "mrm8488/bert-tiny-5-finetuned-squadv2", args=train_args,
                                           use_cuda=False)

            model.save_model(path, model=model.model)
            return json.dumps({'message': 'BERT has been downloaded, in order to train request again'}, sort_keys=False, indent=4), 200
        else:
            model=QuestionAnsweringModel(model_name, path+"/", use_cuda=False)
            model.train_model(train_data)
            model.save_model(path, model=model.model)
            return json.dumps({'message': 'Model has been trained on database train data'}, sort_keys=False, indent=4), 200

    return json.dumps({'message': model_name + 'has not yet been implemented'}, sort_keys=False, indent=4), 404



app.run(host='0.0.0.0', port=5000, threaded=True)
