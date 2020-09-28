from flask import Flask, json, Request, Response
import psycopg2 as psql
import os

app = Flask(__name__)
app.config["DEBUG"] = True

conn = psql.connect(
    host=os.environ['PSQL_HOST'],
    port=os.environ['PSQL_PORT'],
    user=os.environ['PSQL_USR'],
    password=os.environ['PSQL_PASS'],
    database=os.environ['PSQL_DB']

)

@app.route('/db/ping', methods=['POST'])
def ping():
    # create a cursor
    cur = conn.cursor()

    # execute a statement
    cur.execute('SELECT version()')
    # display the PostgreSQL database server version
    db_version = cur.fetchone()

    return json.dumps({"message": "PostgreSQL database version:" + str(db_version)}, sort_keys=False, indent=4), 200

app.run(host='0.0.0.0', port=5000)