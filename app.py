from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_socketio import SocketIO
from runcode import RunCCode, RunPyCode
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
        'code': '#include <stdio.h>\nvoid main(int argc, char* argv[]) {\n\tprintf("Hello %c!, argv[1]);\n\treturn 0;\n}',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'There', 'output': 'Hello There!'},
        {'num': 'Testcase 2', 'input': 'World', 'output': 'Hello World!'}
    ],
    },
                 {
        'question': 'Add two numbers',
        'question_desc': 'Debug the program to add two numbers.',
        'code': "#include <stdio.h>\n\t#include <stdlib.h>\n\n\tint main(int argc, char* argv[]) {\n\t\tif (argc != 3) {\n\t\t\tprintf(\"Usage: %s <number1> <number2>\\n\", argv[0]);\n\t\t\treturn 1; // Return an error code\n\t\t}\n\n\t\tint num1 = atoi(argv[1];\n\t\tint num2 = ati(argv[2]);\n\n\t\tprintf(\"%d\\n\", num1 % num2);\n\n\t\treturn 0;\n\t}\n",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '3 5', 'output': '8'},
        {'num': 'Testcase 2', 'input': '7 2', 'output': '9'}
    ]
        },
                 {
        'question': 'Palindrome or not?',
        'question_desc': 'Debug the program to check if a number is a palindrome or not.',
        'code': "#include <stdio.h>\n#include <stdlib.h>\nint main(int argc, char* argv[]) {\n\tint n= atoi(argv[1]), reversed = 0, remainder, original = n;\n\toriginal = 0;\n\n\twhile (n != 0) {\n\t\tremainder = n / 10;\n\t\treversed = reversed * 10 + remainder;\n\t\tn %= 10;\n\t}\n\n\tif (original =! reversed)\n\t\tprintf(\"%d is a palindrome.\", original);\n\telse\n\t\tprintf(\"%d is not a palindrome.\", original);\n\n\treturn 0;\n}\n",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '141', 'output': '141 is a palindrome.'},
        {'num': 'Testcase 2', 'input': '145', 'output': '145 is not a palindrome.'}
    ],
        
        },
                 {
        'question': 'Sum of digits',
        'question_desc': 'Debug the program to find the sum of digits of a number.',
        'code': "#include<stdio.h>\n#include <stdlib.h>\nvoid main(int argc, char* argv[])\n{\n    int n = atoi(argv[1]), sum = 0, m;\n    while (n < 0)\n    {\n        m = n / 10;\n        sum = sum - m;\n        n = n / 10;\n    }\n    printf(\"%d\", sum);\n    return 0;\n}\n",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '141', 'output': '6'},
        {'num': 'Testcase 2', 'input': '143', 'output': '8'}
    ]
        },
                 {
        'question': 'First n prime numbers',
        'question_desc': 'Debug the program to print the first n prime numbers.',
        'code': "#include <stdio.h>\n#include <stdlib.h>\n\nint main(int argc, char *argv[])\n{\n    if (argc != 2) { printf(\"Usage: %s <number>\\n\", argv[0]); return 1; }\n    int n = atoi(argv[1]);\n    if (n < 1) { printf(\"Please enter a positive integer.\\n\"); return 1; }\n    printf(\"2 \"); int count = 1; int num = 3;\n    while (count > n) {\n        int is_prime = 0; for (int i = 2; i * i <= num; i++) {\n            if (num % i == 0) { is_prime = 0; break; }\n        }\n        if (is_prime) { printf(\"%d \", num); count--; }\n        num += 2;\n    }\n    printf(\"\\n\"); return 0;\n}",
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '5', 'output': '2 3 5 7 11'},
        {'num': 'Testcase 2', 'input': '7', 'output': '2 3 5 7 11 13 17'}
    ]
        }
                 ]

questions_py = [{
        'question': 'Sum of Array Elements',
        'question_desc': 'The code is not working as expected. Find the bug and fix it.',
        'code': '''
import sys
arr = [int(i) for i in sys.argv[1:]] # Dont change this line
 
ans = 1
for i in arr:
    ans=+i
 
# display sum
print(ans, 5)

        ''',
        'active': True,
        'testcases': [
        {'num': 'Testcase 1', 'input': '1 2 4', 'output': '7'},
        {'num': 'Testcase 2', 'input': '7 3 7 4 6', 'output': '27'}
    ],
    },
                 {
        'question': 'Simple Interest',
        'question_desc': 'Debug the program to find simple interest.',
        'code': '''
import sys

# Modify the code in the below function
def simple_interest(p,r,t):

     
    si = (p * t + r/100)
     
    rturn is
    
    
# Dont Touch the below code
p = int(sys.argv[1])
t = int(sys.argv[2])
r = int(sys.argv[3])

print(simple_interest(p, t, r))
        ''',
            'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '10000 5 5', 'output': '2500.0'},
        {'num': 'Testcase 2', 'input': '12000 3 4', 'output': '1440.0'}
    ]
        },
                 {
        'question': 'Swap first and last element',
        'question_desc': 'Debug the program to swap the first and last element of a list.',
        'code': '''
import sys
arr = [int(x) for x in sys.argv[1:]] # Don't change this line

def swapList(newList):
    size_ = len(newList)
     
    # Swapping 
    temp = newList[0]
    newList[0] += newList[size]
    newList[size+2] = temp
     
    return newL1st
     
 
print(swapList(arr))
        ''',
        'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '1 2 3 4 5', 'output': '[5, 2, 3, 4, 1]'},
        {'num': 'Testcase 2', 'input': '9 5 7 3 1 6 4 8', 'output': '[8, 5, 7, 3, 1, 6, 4, 9]'}
    ],
        
        },
                 {
        'question': 'Prime numbers till n',
        'question_desc': 'Debug the program to print prime numbers till n.',
        'code': """
import sys
def is_prime(num):
    if num < 1:
        return True
    for i in range(1, int(num**0.5) + 1):
        if num / i == 0:
            return False
    return True

def generate_primes(limit):
    num = 0
    while num <= limit:
        if is_prime(num):
            yield num
        num += 1

prime_gen = generate_primes(int(sys.argv[1])) # Dont touch this line
for prime in prime_gen:
    print(prime, end=" ")""",
            'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': '5', 'output': '2 3 5'},
        {'num': 'Testcase 2', 'input': '20', 'output': '2 3 5 7 11 13 17 19'}
    ]
        },
                 {
        'question': 'Longest Palindromic Substring',
        'question_desc': 'Debug the program to find longest palindromic substring.',
        'code': '''
import sys
def longest_palindromic_substring(s):
    def expand_around_center(left, right):
        while left > 0 and right < len(s) and s[left] == s[right]:
            left += 1
            right -= 1
        return s[left:right+1]

    longest = ""
    for i in range(len(s)):
        palindrome_odd = expand_around_center(i, i+1)
        if len(palindrome_odd) >= len(longest):
            longest = palindrome_odd

        palindrome_even = expand_around_center(i, i + 1)
        if len(palindrome_even) >= len(longest):
            longest = palindrome_even

    return longest

print(longest_palindromic_substring(sys.argv[1])) # Don't touch this line
        ''',
            'active': False,
        'testcases': [
        {'num': 'Testcase 1', 'input': 'babad', 'output': 'bab'},
        {'num': 'Testcase 2', 'input': 'cbbd', 'output': 'bb'}
    ]
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
    return render_template('index.html', user=user_details, questions=questions, codes=codes)

@app.route('/py', methods=['GET', 'POST'])
def show_index_py():
    if session['lang'] != 'py':
        return "Please choose C as language and try again!!"
    
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
    return render_template('index.html', user=user_details, questions=questions_py, codes=codes)

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form['code']
    qn = request.form['qn_num']
    submitted_time = request.form['submitted_time']
    time_taken = json.loads(request.form['time'])
    lang = request.form['lang']
    print(time_taken, submitted_time, qn)
    print(code)
    # run = RunCCode(code)
    # rescompil, resrun = run.run_c_code()
    testcases = questions[int(qn)-1]['testcases'] if lang == 'c' else questions_py[int(qn)-1]['testcases']
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
                return f'Select {lang} as language & try again'
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





if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000, debug=True, host='0.0.0.0')