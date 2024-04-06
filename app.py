from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from runcode import RunCCode



app = Flask(__name__)
socketio = SocketIO (
      app,
      async_mode="threading"
 )


@app.route('/', methods=['GET', 'POST'])
def show_index():
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
                 ]
    if request.method == 'POST':
        code = request.form['code']
        run = RunCCode(code)
        rescompil, resrun = run.run_c_code()
        if not resrun:
            resrun = 'No result!'
    else:
        pass
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form['code']
    print(code)
    run = RunCCode(code)
    rescompil, resrun = run.run_c_code()
    print(resrun)
    status = {'error': 0, 'output': resrun}
    if not resrun:
        status = {'error': 1, 'err_desc':'Compilation Error'}
    return jsonify({'result': status})

@socketio.on('message')
def handle_message(message):
    print(message)




if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000, debug=True)