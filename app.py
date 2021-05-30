from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'random string'

app.config['MYSQL_HOST'] = '<your host name>'
app.config['MYSQL_USER'] = '<your user name>'
app.config['MYSQL_PASSWORD'] = '<your password>'
app.config['MYSQL_DB'] = '<database name>'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=data )

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        taskscontent = request.form['taskscontent']
        cur = mysql.connection.cursor()
        cur.execute(""" INSERT INTO tasks (taskscontent) VALUES (%s) """, (taskscontent,))
        mysql.connection.commit()
        flash("One Task Added to Board")
        return redirect(url_for('Index'))

@app.route('/delete/<string:idtasks_data>', methods = ['GET'])
def delete(idtasks_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE idtasks=%s", (idtasks_data,))
    mysql.connection.commit()
    flash("One Task Has Been Deleted")
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        idtasks_data = request.form['idtasks']
        taskscontent = request.form['taskscontent']
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE tasks SET taskscontent=%s WHERE idtasks=%s """, (taskscontent, idtasks_data))
        flash("Task Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/deleteall', methods = ['GET'])
def deleteall():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE TABLE tasks")
    mysql.connection.commit()
    flash("Tasks Board Cleared")
    return redirect(url_for('Index'))

@app.route('/sort')
def sort():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY taskscontent")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=data)

if __name__ == "__main__":
    app.run(debug=True)