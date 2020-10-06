import os
import pandas as pd
from flask import Flask, json, request, Response
from simpletransformers.question_answering import QuestionAnsweringModel

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/predict/<model_name>', methods=['POST'])
def predict(model_name):
    path = os.environ['MODEL_REPO'] + "/" + model_name
    model = QuestionAnsweringModel(model_name, path, use_cuda=False)
    question = request.get_json()

    result = model.predict(question)

    answers = pd.DataFrame(result[0][0]['answer'][0:3], columns=["Answers"])
    answers["probabilities"] = result[1][0]['probability'][0:3]
    df_no_indices = answers.to_string(index=False)

    return json.dumps(df_no_indices, sort_keys=False, indent=4), 200


app.run(host='0.0.0.0', port=5000, threaded=True)
