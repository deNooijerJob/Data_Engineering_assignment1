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

#Set env variables
ENV PSQL_HOST  "psql"
ENV PSQL_PORT "5432"
ENV PSQL_USR "postgres"
ENV PSQL_PASS "DE2020_group6"
ENV PSQL_DB "de2020"

#run the api
CMD ["python3", "db_api.py"]