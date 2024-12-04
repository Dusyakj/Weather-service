from flask import Flask, render_template, request
from operations import main

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    result = [None,None]
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                result = main(city)
            except Exception as e:
                result = f"Произошла ошибка: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
