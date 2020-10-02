import os
import pandas as pd
import requests

from random import sample
from flask import Flask, json, Response
from simpletransformers.question_answering import QuestionAnsweringModel

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('train/<model>', methods=['POST'])
def train_model(model):
    api = os.environ['DB_API']
    #req = requests.get(api)
    #data = req.json()

    # train_data = pd.DataFrame.from_dict(data)
    #train_data = [item for topic in train_data['data'] for item in topic['paragraphs']]
    #train_data = sample(train_data, 100)
    if model == "bert":
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

        model = QuestionAnsweringModel('bert', "deepset/bert-large-uncased-whole-word-masking-squad2", args=train_args,
                                       use_cuda=False)
        #model.train_model(train_data)
        model.save_model(os.environ['MODEL_REPO'] + '/' + model, model=model.model)


    return json.dumps({'message': ' training has started on path ' + model}, sort_keys=False, indent=4), 200



app.run(host='0.0.0.0', port=5000)