from flask import Flask, request, render_template, redirect, url_for
from src.pipeline.predictionpipeline import CustomData, PredictPipeline
from src.logger import logging

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('predict_datapoint'))

# Prediction route


@app.route('/predict', methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")

    else:
        data = CustomData(
            Airline=request.form.get('Airline'),
            Source=request.form.get('Source'),
            Destination=request.form.get('Destination'),
            Journey_Day=int(request.form.get('Journey_Day')),
            Journey_Month=int(request.form.get('Journey_Month')),
            Journey_Weekday=request.form.get('Journey_Weekday'),
            Departure_Part_of_Day=request.form.get('Departure_Part_of_Day'),
            Arrival_Part_of_Day=request.form.get('Arrival_Part_of_Day'),
            Duration_Hour=int(request.form.get('Duration_Hour')),
            Duration_Min=int(request.form.get('Duration_Min')),
            Total_Stops=request.form.get('Total_Stops')
        )

        final_data = data.get_data_as_dataframe()
        logging.info(f'{final_data}')

        predict_pipeline = PredictPipeline()

        pred = predict_pipeline.predict(final_data)

        # Rounding the prediction value up to 2 points
        result = round(pred[0], 2)

        return render_template("result.html", final_result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
