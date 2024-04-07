from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_socketio import SocketIO
from runcode import RunCCode
import json
from time import sleep
import mysql.connector
from flask_cors import CORS


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

CORS(app, origins=[
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://192.168.82.8:5000",
    # Add more origins as needed
]) 

app.secret_key = '875dee07a28e825074bff0e1b7da9564e107c4e3e5b809cb'

questions = [{
        'question': 'Debug the code',
        'question_desc': 'The code is not working as expected. Find the bug and fix it.',
        'code': '#include <stdio.h>\nint main(int argc, char* argv[]) {\n\tprintf("Hello %s!", argv[1]);\n\treturn 0;\n}',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'There', 'output': 'Hello There!'},
        {'num': 'Testcase 2', 'input': 'World', 'output': 'Hello World!'}
    ],
        'private_testcases': [
        {'num': 'Testcase 1', 'input': 'Friends', 'output': 'Hello Friends!'},
        {'num': 'Testcase 2', 'input': 'Globe', 'output': 'Hello Globe!'}
        ]
    },
                 {
        'question': 'Find the output',
        'question_desc': 'What will be the output of the following code?',
        'code': "#include <stdio.h>\n\t#include <stdlib.h>\n\n\tint main(int argc, char* argv[]) {\n\t\tif (argc != 3) {\n\t\t\tprintf(\"Usage: %s <number1> <number2>\\n\", argv[0]);\n\t\t\treturn 1; // Return an error code\n\t\t}\n\n\t\tint num1 = atoi(argv[1]);\n\t\tint num2 = atoi(argv[2]);\n\n\t\tprintf(\"%d\\n\", num1 + num2);\n\n\t\treturn 0;\n\t}\n",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '3 5', 'output': '8'},
        {'num': 'Testcase 2', 'input': '7 2', 'output': '9'}
    ]
        },
                 {
        'question': 'Write the code',
        'question_desc': 'Write a program to print "Hello World!"',
        'code': 'Nil',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Thizz', 'output': 'Thizz!'},
        {'num': 'Testcase 2', 'input': 'Fizz', 'output': 'Fizz!'}
    ],
        'private_testcases': [
        {'num': 'Testcase 1', 'input': 'Fizz', 'output': 'Fizz!'},
        {'num': 'Testcase 2', 'input': 'Rizz', 'output': 'Rizz!'}
        ]
        },
                 {
        },
                 {
        'question': 'Write the code',
        'question_desc': 'Write a program to print "Hello World!"',
        'code': 'Nil',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Thizz', 'output': 'Thizz!'},
        {'num': 'Testcase 2', 'input': 'Fizz', 'output': 'Fizz!'}
    ]
        },
                 {
        'question': 'Find the output',
        'question_desc': 'What will be the output of the following code?',
        'code': '#include <stdio.h>\nint main() {\n\tprintf("Hello World!");\n\treturn 0;\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'SSSS', 'output': 'Hello SSSS!'},
        {'num': 'Testcase 2', 'input': 'DDDD', 'output': 'Hello DDDD!'}
    ]
        }
                 ]


@app.route('/', methods=['GET', 'POST'])
def show_index():
    
    if 'username' not in session:
        return redirect(url_for('login'))
    print(session['username'])
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, q1_status, q2_status, q3_status, q4_status, q5_status from users WHERE username = %s', (session['username'],))
    user_details = cursor.fetchall()[0]
    user_details['username'] = session['username']
    cursor.reset()
    conn.close()
    
    print(user_details)
    
    
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
    for i in questions[int(qn)-1]['testcases']+questions[int(qn)-1]['private_testcases']:
        print(i)
        run = RunCCode(code, i['input'])
        rescompil, resrun = run.run_c_code()
        print(resrun)
        if not resrun:
            status = {'error': 1, 'err_desc':'Compilation Error'}
            return jsonify({'result': status})
        if resrun.strip() == i['output']:
            print('Correct')
        else:
            status = {'error': 1, 'err_desc':'Runtime Error'}
            return jsonify({'result': status})
    print(resrun)
    status = {'error': 0, 'output': resrun}
    
    
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
    cursor.execute(f'select q{qn}_status from users where username = {session["username"]}')
    if cursor.fetchone()[f'q{qn}_status'] == 1:
        status = {'error': 1, 'err_desc':'Already submitted'}
        return jsonify({'result': status})
    cursor.reset()
    cursor.execute(f'update users set q{qn}_status = 1, total_score = total_score + {score} where username = {session["username"]}')
    
    cursor.reset()
    conn.commit()
    query = (f"insert into q{qn} values ('{session['username']}', '{submitted_time}', '{time_taken}', {score}, '{code}')")
    
    cursor.execute(query)
    cursor.reset()
    conn.commit()
    conn.close()
    
    socketio.emit('refresh_admin')
    
    return jsonify({'result': status})

@socketio.on('connect')
def handle_message():
    print("Connected")



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

@app.route('/admin140204*', methods=['GET', 'POST'])
def admin():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT username, name, password, total_score FROM users ORDER BY total_score DESC')
    leader_board = cursor.fetchall()
    cursor.reset()
    submissions = []

    
    for i in range(1, 6):
        cursor.execute(f'SELECT * FROM `q{i}`')
        submissions.append(cursor.fetchall())
        cursor.reset()
        
    print(len(submissions))
    
    conn.close()
    return render_template('admin.html', leader_board_data=leader_board, submissions=submissions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_index'))





if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000, debug=True, host='0.0.0.0')