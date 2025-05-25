import os

from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_socketio import SocketIO
from runcode import RunCCode, RunPyCode
import json
from time import sleep
import mysql.connector
from flask_cors import CORS
import os


# db_config = {
#     'host': 'sql12.freesqldatabase.com',
#     'user': 'sql12729369',
#     'database': 'sql12729369',
#     'password' : 'aflbzTw75J'
# }

db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'debugging'
}


qn_points = [10, 10, 10, 10, 10]

isEventStarted = False




app = Flask(__name__)
socketio = SocketIO (
      app,
      async_mode="threading"
 )

CORS(app, origins="*") 

app.secret_key = '875dee07a28e825074bff0e1b7da9564e107c4e3e5b809cb'

questions = [{
        'question': 'Debug the code',
        'question_desc': 'The code is not working as expected. Find the bug and fix it.',
        'code': 'int factorial(int n) {\n\tif (n == 1)\n\t\treturn 0;\n\telse\n\t\treturn n * factorial(n - 1);\n}',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': '5', 'output': '120'},
        {'num': 'Testcase 2', 'input': '4', 'output': '24'},
        ],
        'drive_code':'#include <stdio.h>\n#include <stdlib.h>\nint factorial(int);\n\nint main(int argc, char *argv[]) {\n\tif (argc != 2) {\n\t\tprintf("Usage: %s <number>", argv[0]);\n\t\treturn 1;\n\t}\n\n\tint num = atoi(argv[1]);\n\tprintf("%d", factorial(num));\n\treturn 0;\n}\n\n'
    
    },
                 {
        'question': 'Find GCD or HCF of two numbers',
        'question_desc': 'Debug the program to find gcd.',
        'code': 'int gcd(int a, int b) {\n\tif (a == 0)\n\t\treturn b;\n\telse\n\t\treturn gcd(a, b / a);\n}\n\n',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '20 28', 'output': '4'},
        {'num': 'Testcase 2', 'input': '60 36', 'output': '12'}
    ],
        'drive_code':'#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[]) {\n\tif (argc != 3) {\n\t\tprintf("Usage: %s <number1> <number2>\\n", argv[0]);\n\t\treturn 1;\n\t}\n\n\tint num1 = atoi(argv[1]);\n\tint num2 = atoi(argv[2]);\n\n\tprintf("%d", gcd(num1, num2));\n\treturn 0;\n}'
        },
                 {
        'question': 'Sum of Array',
        'question_desc': 'Debug the program to find the sum of array.',
        'code': 'int sum_array(int arr[], int n) {\n\tint sum = 1;\n\tfor (int i = 1; i <= n; ++i)\n\t\tsum = arr[i]\n\treturn sum\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '1 2 3 4 5', 'output': '15'},
        {'num': 'Testcase 2', 'input': '6 84 13 29 45', 'output': '177'}
    ],
        'drive_code':'#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[]) {\n\tint n = argc - 1;\n\tif (n == 0) {\n\t\tprintf("Usage: %s <num1> <num2> ... <numN>\\n", argv[0]);\n\t\treturn 1;\n\t}\n\n\tint arr[n];\n\tfor (int i = 0; i < n; i++) {\n\t\tarr[i] = atoi(argv[i + 1]);\n\t}\n\n\tprintf("%d", sum_array(arr, n));\n\treturn 0;\n}'
        
        },
                 {
        'question': 'Is Prime?',
        'question_desc': 'Debug the program to check a number is prime. The function "is_prime" returns 1 if the number is prime else it returns 0',
        'code': 'int is_prime(int n) {\n\tif (n >= 1)\n\t\treturn 0;\n\tfor (int i = 1; i < n; i++) {\n\t\tif (i % n == 1)\n\t\t\treturn 0;\n\t}\n\treturn -1\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '12', 'output': '0'},
        {'num': 'Testcase 2', 'input': '11', 'output': '1'}
    ],
        'drive_code': '#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[]) {\n\tif (argc != 2) {\n\t\tprintf("Usage: %s <number>\\n", argv[0]);\n\t\treturn 1;\n\t}\n\n\tint num = atoi(argv[1]);\n\tprintf("%d", is_prime(num));\n\n\treturn 0;\n}'
        },
                 {
        'question': 'Find largest number in an array.',
        'question_desc': 'Debug the program to find the largest number.',
        'code': 'int find_largest(int arr[], int n) {\n\tint max = arr[1];\n\tfor (int i = n; i > 0; i--) {\n\t\tif (arr[i] < max)\n\t\t\tarr[i] = max;\n\t}\n\treturn max;\n}',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '6 84 13 29 45 ', 'output': '84'},
        {'num': 'Testcase 2', 'input': '7 47 18 64 24', 'output': '64'}
    ],
        'drive_code':'#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[]) {\n\tint n = argc - 1;\n\tif (n == 0) {\n\t\tprintf("Usage: %s <num1> <num2> ... <numN>\\n", argv[0]);\n\t\treturn 1;\n\t}\n\n\tint arr[n];\n\tfor (int i = 0; i < n; i++) {\n\t\tarr[i] = atoi(argv[i + 1]);\n\t}\n\n\tprintf("%d", find_largest(arr, n));\n\treturn 0;\n}'
        }
                 ]

questions_py = [{
        'question': 'Count Word Frequency',
        'question_desc': 'The code is not working as expected. Find the bug and fix it.',
        'code': 'def count_word_frequency(sentence):\n\twords = sentence.upper().split(",")\n\tword_count = {}\n\tfor word in words:\n\t\tif word not in word_count:\n\t\t\tword_count[word] += 1\n\t\telse:\n\t\t\tword_count[word] = 2\n\treturn word_count',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'Hello this is a friend', 'output': "{'hello': 1, 'this': 1, 'is': 1, 'a': 1, 'friend': 1}"},
        {'num': 'Testcase 2', 'input': 'IF U KNOW, U KNOW AND THATS Y NO ONE KNOW', 'output': "{'if': 1, 'u': 2, 'know,': 1, 'know': 2, 'and': 1, 'thats': 1, 'y': 1, 'no': 1, 'one': 1}"}
    ],
        'drive_code':'import sys\nprint(count_word_frequency(" ".join(sys.argv[1:])))'
    },
                 {
        'question': 'Remove Duplicates from the list',
        'question_desc': 'Debug the program to remove duplicates.',
        'code': 'def remove_duplicates(numbers):\n\tseen = list()\n\tresult = []\n\tfor num in numbers:\n\t\tif num in seen:\n\t\t\tseen.append(num)\n\t\t\tresult.insert(0, num)\n\treturn result',
            'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '1 2 2 2 3 4 3 7 7 5 7', 'output': "['1', '2', '3', '4', '7', '5']"},
        {'num': 'Testcase 2', 'input': '6 4 9 5 7 9 4 6 5', 'output': "['6', '4', '9', '5', '7']"}
    ],
        'drive_code':"import sys\nprint(remove_duplicates(sys.argv[1:]))"
        },
                 {
        'question': 'Convert Temperatures',
        'question_desc': 'Debug the program to convert fahrenheit to celsius and vice versa.',
        'code': "def convert_temperature(temp, unit):\n\tif unit == 'C':\n\t\tfahrenheit = temp / 9*5 + 32\n\t\treturn round(fahrenheit, 1)\n\telif unit == 'F':\n\t\tcelsius = (temp + 32) * 5/9\n\t\treturn round(celsius, 2)\n\treturn None",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '40 F', 'output': '4.4'},
        {'num': 'Testcase 2', 'input': '33 C', 'output': '91.4'}
    ],
        'drive_code':"import sys\nprint(convert_temperature(int(sys.argv[1]), sys.argv[2]))"
        
        },
                 {
        'question': 'Is Valid Email',
        'question_desc': 'Debug the program to check whether the given mail id is in correct format.',
        'code': "def is_valid_email(email):\n\tif email or ' ' in email:\n\t\treturn False\n\tparts = email.split('@')\n\tif len(parts) != 3 or not parts[0] or not parts[1]:\n\t\treturn False\n\tdomain = parts[0]\n\treturn '.' in domain and domain.rfind('.') < len(domain) - 1",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'helloworld@hi.com', 'output': 'True'},
        {'num': 'Testcase 2', 'input': 'hello@world@hi', 'output': 'False'}
    ],
        'drive_code': 'import sys\nprint(is_valid_email(sys.argv[1]))'
        },
                 {
        'question': 'Format Number',
        'question_desc': 'Debug the program to format a given number with comma separation.',
        'code': "def format_number(number):\n\tnum_str = str(abs(number))\n\tresult = '-'\n\tfor i, digit in enumerate(reversed(num_str)):\n\t\tif i > 0 and i % 3 == 0:\n\t\t\tresult = ',,' + result\n\t\tresult = digit + result\n\tif number > 0:\n\t\tresult = '-' + result\n\treturn result",
            'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '2414124121', 'output': '2,414,124,121'},
        {'num': 'Testcase 2', 'input': '-32984', 'output': '-32,984'}
    ],
        'drive_code':'import sys\nprint(format_number(int(sys.argv[1])))'
        },
                 ]

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/c', methods=['GET', 'POST'])
def show_index():
    if session['lang'] != 'c':
        return "Please choose Python as language and try again!!"
    
    if 'username' not in session:
        return redirect(url_for('login'))
    print(session['username'])
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, q1_status, q2_status, q3_status, q4_status, q5_status from users WHERE username = %s', (session['username'],))
    user = cursor.fetchall()
    if not user:
        redirect(url_for('login'))
    user_details = user[0]
    user_details['username'] = session['username']
    cursor.reset()
    conn.close()
    
    print(user_details)
    
    
    codes = json.dumps([
    '#include <stdio.h>\nvoid main(int argc, char* argv[]) {\n\tprintf("Hello %c!, argv[1]);\n\treturn 0;\n}',
    "#include <stdio.h>\n\t#include <stdlib.h>\n\n\tint main(int argc, char* argv[]) {\n\t\tif (argc != 3) {\n\t\t\tprintf(\"Usage: %s <number1> <number2>\\n\", argv[0]);\n\t\t\treturn 1; // Return an error code\n\t\t}\n\n\t\tint num1 = atoi(argv[1];\n\t\tint num2 = ati(argv[2]);\n\n\t\tprintf(\"%d\\n\", num1 % num2);\n\n\t\treturn 0;\n\t}\n",
    "#include <stdio.h>\n#include <stdlib.h>\nint main(int argc, char* argv[]) {\n\tint n= atoi(argv[1]), reversed = 0, remainder, original = n;\n\toriginal = 0;\n\n\twhile (n != 0) {\n\t\tremainder = n / 10;\n\t\treversed = reversed * 10 + remainder;\n\t\tn %= 10;\n\t}\n\n\tif (original =! reversed)\n\t\tprintf(\"%d is a palindrome.\", original);\n\telse\n\t\tprintf(\"%d is not a palindrome.\", original);\n\n\treturn 0;\n}\n",
    "#include<stdio.h>\n#include <stdlib.h>\nvoid main(int argc, char* argv[])\n{\n    int n = atoi(argv[1]), sum = 0, m;\n    while (n < 0)\n    {\n        m = n / 10;\n        sum = sum - m;\n        n = n / 10;\n    }\n    printf(\"%d\", sum);\n    return 0;\n}\n",
    "#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[])\n{\n    if (argc != 2) { printf(\"Usage: %s <number>\\n\", argv[0]); return 1; }\n    int n = atoi(argv[1]);\n    if (n < 1) { printf(\"Please enter a positive integer.\\n\"); return 1; }\n    printf(\"2 \"); int count = 1; int num = 3;\n    while (count > n) {\n        int is_prime = 0; for (int i = 2; i * i <= num; i++) {\n            if (num % i == 0) { is_prime = 0; break; }\n        }\n        if (is_prime) { printf(\"%d \", num); count--; }\n        num += 2;\n    }\n    printf(\"\\n\"); return 0;\n}",
    ])
    if request.method == 'POST':
        code = request.form['code']
        run = RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        pass
    return render_template('index.html', user=user_details, questions=questions, codes=[])

@app.route('/py', methods=['GET', 'POST'])
def show_index_py():
    if session['lang'] != 'py':
        return "Please choose Python as language and try again!!"
    
    if 'username' not in session:
        return redirect(url_for('login'))
    print(session['username'])
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, q1_status, q2_status, q3_status, q4_status, q5_status from users WHERE username = %s', (session['username'],))
    user = cursor.fetchall()
    if not user:
        return redirect(url_for('login'))
    user_details = user[0]
    user_details['username'] = session['username']
    cursor.reset()
    conn.close()
    
    print(user_details)
    if request.method == 'POST':
        code = request.form['code']
        run = RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        pass
    return render_template('index.html', user=user_details, questions=questions_py, codes=[])

@app.route("/code/<lang>/<num>")
def get_code(lang, num):
    if lang == 'py':
        return jsonify({'code': questions_py[int(num)-1]['code']})
    else: 
        return jsonify({'code': questions[int(num)-1]['code']})

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form['code']
    qn = request.form['qn_num']
    submitted_time = request.form['submitted_time']
    time_taken = json.loads(request.form['time'])
    lang = request.form['lang']
    print(time_taken, submitted_time, qn)
    # run = RunCCode(code)
    # rescompil, resrun = run.run_c_code()
    testcases = questions[int(qn)-1]['testcases'] if lang == 'c' else questions_py[int(qn)-1]['testcases']
    if lang == 'c':
        code = questions[int(qn)-1]['drive_code'] + '\n' + code
    else:
        code = code + '\n' + questions_py[int(qn)-1]['drive_code']
    print(code)
    for i in testcases:
        print(i)
        if lang == 'c':
            
            run = RunCCode(code, i['input'])
            try:
                rescompil, resrun = run.run_c_code()
            except Exception as e:
                print(e)
                status = {'error': 1, 'err_desc': 'Compilation Error'}
                return jsonify({'result': status})
            print(resrun)
        else:
            run = RunPyCode(code, i['input'])
            try:
                rescompil, resrun = run.run_py_code()
            except Exception as e:
                print(e)
                status = {'error': 1, 'err_desc': 'Compilation Error'}
                return jsonify({'result': status})
            print(resrun)
        if not resrun:
            status = {'error': 2, 'err_desc':'Compilation Error'}
            return jsonify({'result': status})
        if resrun.strip() == i['output']:
            print('Correct')
        else:
            status = {'error': 1, 'err_desc':f"Your Output:\n\n{resrun.strip()}\n\nExpected Output:\n\n{i['output']}"}
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
    cursor.execute(f'select q{qn}_status from users where username = "{session["username"]}"')
    if cursor.fetchone()[f'q{qn}_status'] == 1:
        status = {'error': 1, 'err_desc':'Already submitted'}
        return jsonify({'result': status})
    cursor.reset()
    cursor.execute(f'update users set q{qn}_status = 1, total_score = total_score + {score} where username = "{session["username"]}"')
    
    cursor.reset()
    conn.commit()
    query = (f"insert into q{qn} values ('{session['username']}', '{submitted_time}', '{time_taken}', {score})")
    
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
        name = request.form['name']
        username = request.form['username']
        phone = request.form['phone']
        lang = request.form['lang']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            print(user)
            conn.close()
            if lang == user['lang']:
                session['username'] = user['username']
                session['lang'] = user['lang']
                if session['lang'] == 'c':
                    return redirect(url_for('show_index'))
                else:
                    return redirect(url_for('show_index_py'))
            else:
                return f'Select {"Python" if user['lang'] == 'py' else "C"} as language & try again'
        else:
            try:
                cursor.execute('INSERT INTO users (username, name, lang, phone) VALUES (%s, %s, %s, %s)',
                            (username, name, lang, phone))
                conn.commit()
                conn.close()
                session['username'] = username  # Set session username after successful insertion
                session['lang'] = lang
                if lang == 'c':
                    return redirect(url_for('show_index'))
                else:
                    return redirect(url_for('show_index_py'))
            except Exception as e:
                # Handle specific exceptions like IntegrityError for duplicate usernames
                return f'Something went wrong: {str(e)}'

                    
            
            

    return render_template('login.html')

@app.route('/admin140204*', methods=['GET', 'POST'])
def admin():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT username, name, phone, total_score FROM users ORDER BY total_score DESC')
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
    return redirect(url_for('login'))

@app.route('/startevent')
def startEvent():
    socketio.emit('startEvent')
    global isEventStarted
    isEventStarted = True
    return {"message":"success"}

@app.route('/isStarted')
def isStarted():
    return {"isStarted": isEventStarted}





if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=os.environ.get("PORT"), debug=True, host='0.0.0.0')
