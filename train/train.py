import os
import requests
from flask import Flask, json, Response
from simpletransformers.question_answering import QuestionAnsweringModel
from random import sample

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/train/<model_name>', methods=['POST'])
def train_model(model_name):

    path = os.environ['MODEL_REPO'] + "/" + model_name
    request_questions = requests.get(os.environ['DB_API_QAS'])
    request_contexts = requests.get(os.environ['DB_API_CON'])
    questions = request_questions.json()
    contexts = request_contexts.json()

    train_data = []
    for i in range(0, len(questions)):
        result = {}
        result['context'] = contexts[questions[i][2] - 1][0]
        qas = []
        instance = {}
        instance['id'] = questions[i][5]
        instance['is_impossible'] = questions[i][4]
        instance['question'] = questions[i][3]
        answer = []
        ans = {}
        ans['text'] = questions[i][1]
        ans['answer_start'] = questions[i][0]
        answer.append(answer)
        instance['answers'] = answer
        qas.append(instance)
        result['qas'] = qas

        train_data.append(result)

    train_data_df = pd.DataFrame.from_dict(data)
     # train_data = [item for topic in train_data['data'] for item in topic['paragraphs']]
    train_data_df = sample(train_data_df, 100)
    if model_name == "bert":
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
        model.train_model(train_data_df)
        model.save_model(path, model=model.model)


    return json.dumps({'message': ' training has started on model ' + model_name}, sort_keys=False, indent=4), 200



app.run(host='0.0.0.0', port=5000, threaded=True)
