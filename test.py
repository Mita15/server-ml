from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='34.125.138.164', port=80,debug=True)