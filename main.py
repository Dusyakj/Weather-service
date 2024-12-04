from flask import Flask

from operations import main

app = Flask(__name__)



@app.route('/')
def home():
    return data


if __name__ == '__main__':
    data = main('Москва')
    app.run(debug=True)
