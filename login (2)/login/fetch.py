from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def display_data():
    conn = sqlite3.connect('D:\MCA sem3\project\login\rto-dbs.sql')  # Replace with your database path
    cursor = conn.cursor()

    query = """SELECT name, registration_number, image_path, ... 
                FROM RTO_Registration 
                ORDER BY name ASC"""  # Adjust query as needed

    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()

    return render_template('fetch.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
