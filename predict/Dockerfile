# use python3 as the base image for the predict api"
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

# environment variable to access the shared model repository
ENV MODEL_REPO  /usr/src/assignment1/models

#run the api
CMD ["python3", "predict.py"]
