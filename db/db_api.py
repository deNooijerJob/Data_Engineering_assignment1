from flask import Flask, json, request, Response
import psycopg2 as ps
import os

app = Flask(__name__)
app.config["DEBUG"] = True
conn = None

def connect():
    conn = ps.connect(
        host=os.environ['PSQL_HOST'],
        port=os.environ['PSQL_PORT'],
        user=os.environ['PSQL_USR'],
        password=os.environ['PSQL_PASS'],
        database=os.environ['PSQL_DB']
    )
    return conn

@app.route('/db/test', methods=['GET'])
def test():
    return "test"

app.run(host='0.0.0.0', port=5000)
