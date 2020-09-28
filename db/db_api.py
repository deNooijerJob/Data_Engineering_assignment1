from flask import Flask, json, Request, Response
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


@app.route('/db/newTable/<table_name>', methods=['POST'])
def new_table(table_name):
    try:
        conn = connect()
        cur = conn.cursor()

        data = Request.get_json()
        columns = data['columns']
        types = data['types']
        attr = data['attr']

        query = "CREATE TABLE " + str(table_name)
        for i in range(0, len(columns)):
            query = query + columns[i] + " " + types[i] + " " + attr[i] + ","

        print(query)
        cur.execute(query)
        cur.close()
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print(error)
        return  json.dumps({'message': error}, sort_keys=False, indent=4), 500

    finally:
        if conn is not None:
            conn.close()

    return json.dumps({'message': ' ' + table_name + ' has been created'}, sort_keys=False, indent=4), 200


app.run(host='0.0.0.0', port=5000)