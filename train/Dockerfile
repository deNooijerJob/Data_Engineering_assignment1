# use python3 as the base image for the db api"
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

ENV DB_API_QAS  http://dbAPI:5000/db/questions
ENV DB_API_CON  http://dbAPI:5000/db/contexts
ENV MODEL_REPO  /usr/src/assignment1/models

#Set env variables


#run the api
CMD ["python3", "train.py"]
