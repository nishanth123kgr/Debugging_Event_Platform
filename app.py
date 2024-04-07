from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_socketio import SocketIO
from runcode import RunCCode
import json
from time import sleep
import mysql.connector


db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'debugging',
    'auth_plugin' : 'mysql_native_password'
}


qn_points = [10, 10, 20, 20, 30]




app = Flask(__name__)
socketio = SocketIO (
      app,
      async_mode="threading"
 )

app.secret_key = '875dee07a28e825074bff0e1b7da9564e107c4e3e5b809cb'




@app.route('/', methods=['GET', 'POST'])
def show_index():
    
    if 'username' not in session:
        return redirect(url_for('login'))
    print(session['username'])
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, q1_status, q2_status, q3_status, q4_status from users WHERE username = %s', (session['username'],))
    user_details = cursor.fetchall()[0]
    user_details['username'] = session['username']
    cursor.reset()
    conn.close()
    
    print(user_details)
    questions = [{
        'question': 'Debug the code',
        'question_desc': 'The code is not working as expected. Find the bug and fix it.',
        'code': '#include <stdio.h>\nint main() {\n\tprintf("Hello World!");\n\treturn 0;\n}',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Nil', 'output': 'Hello Bey!'},
        {'num': 'Testcase 2', 'input': 'Nil', 'output': 'Hello World!'}
    ]
    },
                 {
        'question': 'Find the output',
        'question_desc': 'What will be the output of the following code?',
        'code': '#include <stdio.h>\nint main() {\n\tprintf("Hello World!");\n\treturn 0;\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Nil', 'output': 'Hello SSSS!'},
        {'num': 'Testcase 2', 'input': 'Nil', 'output': 'Hello DDDD!'}
    ]
        },
                 {
        'question': 'Write the code',
        'question_desc': 'Write a program to print "Hello World!"',
        'code': 'Nil',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Nil', 'output': 'Thizz!'},
        {'num': 'Testcase 2', 'input': 'Nil', 'output': 'Fizz!'}
    ]
        },
                 {
        'question': 'Write the code',
        'question_desc': 'Write a program to print "Hello World!"',
        'code': 'Nil',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Nil', 'output': 'Thizz!'},
        {'num': 'Testcase 2', 'input': 'Nil', 'output': 'Fizz!'}
    ]
        },
                 {
        'question': 'Find the output',
        'question_desc': 'What will be the output of the following code?',
        'code': '#include <stdio.h>\nint main() {\n\tprintf("Hello World!");\n\treturn 0;\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Nil', 'output': 'Hello SSSS!'},
        {'num': 'Testcase 2', 'input': 'Nil', 'output': 'Hello DDDD!'}
    ]
        }
                 ]
    
    codes = json.dumps([
    "#include <stdio.h>\\nint main() {\\n\\tprintf(\\\"Hello World!\\\");\\n\\treturn 0;\\n}",
    "#include <stdio.h>\\nint main() {\\n\\tprintf(\\\"Hello World!\\\");\\n\\treturn 0;\\n}",
    "Nil",
    "Nil",
    "#include <stdio.h>\\nint main() {\\n\\tprintf(\\\"Hello World!\\\");\\n\\treturn 0;\\n}",
    ])
    if request.method == 'POST':
        code = request.form['code']
        run = RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        pass
    return render_template('index.html', user=user_details, questions=questions, codes=codes)

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form['code']
    qn = request.form['qn_num']
    submitted_time = request.form['submitted_time']
    time_taken = json.loads(request.form['time'])
    print(time_taken, submitted_time, qn)
    print(code)
    run = RunCCode(code)
    rescompil, resrun = run.run_c_code()
    print(resrun)
    status = {'error': 0, 'output': resrun}
    if not resrun:
        status = {'error': 1, 'err_desc':'Compilation Error'}
        return jsonify({'result': status})
    
    if time_taken['minutes'] < 10:
        rate = 4
    elif time_taken['minutes'] < 20:
        rate = 3
    elif time_taken['minutes'] < 30:
        rate = 2
    else:
        rate = 1
        
    score = rate * qn_points[int(qn)-1]
    time_taken = f"{time_taken['minutes']}:{time_taken['seconds']}"
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'update users set q{qn}_status = 1 where username = {session["username"]}')
    cursor.reset()
    conn.commit()
    query = (f"insert into q{qn} values ('{session['username']}', '{submitted_time}', '{time_taken}', {score}, '{code}')")
    
    print(query)
    cursor.execute(query)
    cursor.reset()
    conn.commit()
    print(query)
    conn.close()
    
    return jsonify({'result': status})

@socketio.on('message')
def handle_message(message):
    print(message)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.reset()
        conn.close()
        if user:
            if password == user['password']:
                session['username'] = user['username']
                return redirect(url_for('show_index'))

        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_index'))





if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000, debug=True)