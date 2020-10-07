# use python3 as the base image for the train api"
FROM python:3.7.7-buster

# set the shared work directory for assignment1
WORKDIR /usr/src/assignment1

#copy the python imports
COPY requirements.txt .

# install the imports from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#copy all local files to workspace
COPY . .

#expose the container port
EXPOSE 5000

# environment variables
# DB_API -> POST address to acces the train data 
# MODEL_REPO -> shared model repository location
ENV DB_API  http://dbAPI:5000/db/test_json
ENV MODEL_REPO  /usr/src/assignment1/models

#run the api
CMD ["python3", "train.py"]
