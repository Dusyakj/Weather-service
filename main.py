from flask import Flask, render_template, request
from operations import main as operations_main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {'start': None, 'end': None}
    if request.method == 'POST':
        start_lat = request.form.get('start_lat')
        start_lon = request.form.get('start_lon')
        start_time = request.form.get('start_time')

        end_lat = request.form.get('end_lat')
        end_lon = request.form.get('end_lon')
        end_time = request.form.get('end_time')

        try:
            start_weather = operations_main(float(start_lat), float(start_lon), start_time)
            end_weather = operations_main(float(end_lat), float(end_lon), end_time)
            result = {'start': start_weather, 'end': end_weather}
        except ValueError:
            result = {'start': None, 'end': "Неверный формат координат."}
        except Exception as e:
            result = {'start': None, 'end': f"Произошла ошибка: {e}"}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

