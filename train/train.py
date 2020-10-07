
import os
import requests
from flask import Flask, json, Response
from simpletransformers.question_answering import QuestionAnsweringModel
from random import sample
import pandas as pd

app = Flask(__name__) # create flask app 
app.config["DEBUG"] = True

# train the bert model
@app.route('/train/<model_name>', methods=['POST'])
def train_model(model_name):
    api = os.environ['DB_API'] # get the request path
    path = os.environ['MODEL_REPO'] + "/" + model_name # get the model repository location

    request_test = requests.get(api) # get the train data from db
    train_data = request_test.json()[0][0] # format the data as json
    model = None # init model
    if model_name == "bert": # if the model selected is bert then
        if not os.path.exists(path): # check whether BERT already exsits
            # set the arguments for training
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
            #download the bert model
            model = QuestionAnsweringModel(model_name, "mrm8488/bert-tiny-5-finetuned-squadv2", args=train_args,
                                           use_cuda=False)

            model.save_model(path, model=model.model) # save the model in the repository
            return json.dumps({'message': 'BERT has been downloaded, in order to train request again'}, sort_keys=False, indent=4), 200 # return result
        else: # if there is a BERT model available
            model=QuestionAnsweringModel(model_name, path+"/", use_cuda=False) # load the model
            model.train_model(train_data) # train the model on the fetched data
            model.save_model(path, model=model.model) # save the updated model
            return json.dumps({'message': 'Model has been trained on database train data'}, sort_keys=False, indent=4), 200 # return the result

    return json.dumps({'message': model_name + 'has not yet been implemented'}, sort_keys=False, indent=4), 404 # return the result



app.run(host='0.0.0.0', port=5000, threaded=True)
