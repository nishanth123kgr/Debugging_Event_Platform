from flask import Flask, render_template, request
from flask_socketio import SocketIO



app = Flask(__name__)
socketio = SocketIO (
      app,
      async_mode="threading"
 )


@app.route('/', methods=['GET', 'POST'])
def show_index():
    if request.method == 'POST':
        return {'status': 'ok'}
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print(message)




if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=5000)