# import os
# import psycopg2
# from flask import Flask

# app = Flask(__name__)

# def get_db_connection():
#     conn = psycopg2.connect(
#         host=os.environ.get("DB_HOST", "localhost"),
#         database=os.environ.get("DB_NAME", "flaskdb"),
#         user=os.environ.get("DB_USER", "flaskuser"),
#         password=os.environ.get("DB_PASSWORD", "flaskpass"),
#         port=5432
#     )
#     return conn

# def init_db():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS greetings (
#             id SERIAL PRIMARY KEY,
#             name TEXT NOT NULL
#         );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# @app.route('/')
# def home():
#     return "Hello, Flask!"

# @app.route('/greet/<name>')
# def greet(name):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO greetings (name) VALUES (%s);", (name,))
#     conn.commit()
#     cur.close()
#     conn.close()
#     return f"Hello, {name}! Stored in database."

# if __name__ == '__main__':
#     init_db()
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask 
app = Flask(__name__) 

@app.route('/') 
def home(): 
    return "Hello, Flask!" 

@app.route('/greet/<name>') 
def greet(name): 
    return f"Hello, {name}!" 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)

