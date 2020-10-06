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


@app.route('/db/<table_name>', methods=['GET'])
def get_content(table_name):
    try:
        conn = connect()
        cur = conn.cursor()

        query = "SELECT * FROM " + str(table_name)

        print(query)
        cur.execute(query)
        records = cur.fetchall()

        cur.close()
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print(error)
        return  json.dumps({'message': error}, sort_keys=False, indent=4), 500

    finally:
        if conn is not None:
            conn.close()

    return json.dumps(records, sort_keys=False, indent=4), 200


@app.route('/db/<table_name>', methods=['POST'])
def new_table(table_name):
    try:
        conn = connect()
        cur = conn.cursor()

        data = request.get_json()
        columns = data['columns']
        types = data['types']
        attr = data['attr']

        query = "CREATE TABLE " + str(table_name) + " ("
        for i in range(0, len(columns)):
            query = query + columns[i] + " " + types[i] + " " + attr[i]
            if i < len(columns) - 1:
                query = query + ", "

        query = query + ")"

        print(query)
        cur.execute(query)
        cur.close()
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print(error)
        return json.dumps({'message': error}, sort_keys=False, indent=4), 500

    finally:
        if conn is not None:
            conn.close()

    return json.dumps({'message': ' ' + table_name + ' has been created'}, sort_keys=False, indent=4), 200


@app.route('/db/<table_name>', methods=['PUT'])
def insert(table_name):
    try:
        conn = connect()
        cur = conn.cursor()

        data = request.get_json()

        for i in range(0, len(data)):

            query = "INSERT INTO " + str(table_name) + "("
            len_columns = len(data[i])
            c_columns, c_val = 0, 0

            for field in data[i]:
                c_columns += 1
                query = query + str(field)
                if c_columns < len_columns:
                    query = query + ", "

            query = query + ") VALUES ("

            for val in data[i]:
                c_val += 1
                query = query + "'" + str(data[i][val]) + "'"
                if c_val < len_columns:
                    query = query + ", "
            query = query + ")"
            cur.execute(query)

        cur.close()
        conn.commit()
    except (Exception, ps.DatabaseError) as error:
        print(error)
        return json.dumps({'message': error}, sort_keys=False, indent=4), 500

    finally:
        if conn is not None:
            conn.close()

    return json.dumps({'message': table_name + ' has been updated'}, sort_keys=False, indent=4), 200




app.run(host='0.0.0.0', port=5000)
