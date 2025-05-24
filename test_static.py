from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return '<img src="/static/1.jpg">'
if __name__ == '__main__':
    app.run(debug=True) 