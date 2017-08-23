import sys

import pandas as pd
from flask import request, jsonify, render_template
from sklearn.externals import joblib
from wtforms import IntegerField
from churn import app
from flask_wtf import FlaskForm

try:
    print("try", file=sys.stderr)
    model = joblib.load("C:/Users/sauraraj/IdeaProjects/CustomerChurnPrediction/churn_model.pkl")
    print("model loaded", file=sys.stderr)
except Exception as e:
    print("No model found", file=sys.stderr)


class OurForm(FlaskForm):
    State = IntegerField("State")
    Account_Length = IntegerField("Account_Length")
    Area_Code = IntegerField("Area_Code")
    Intl_Plan = IntegerField("Intl_Plan")
    VMail_Plan = IntegerField("VMail_Plan")
    VMail_Message = IntegerField("VMail_Message")
    Day_Mins = IntegerField("Day_Mins")
    Day_Calls = IntegerField("Day_Calls")
    Eve_Mins = IntegerField("Eve_Mins")
    Eve_Calls = IntegerField("Eve_Calls")
    Night_Mins = IntegerField("Night_Mins")
    Night_Calls = IntegerField("Night_Calls")
    Intl_Mins = IntegerField("Intl_Mins")
    Intl_Calls = IntegerField("Intl_Calls")
    CustServ_Calls = IntegerField("CustServ_Calls")


def churn_prediction(data):
    data = data.to_dict()
    data.pop('csrf_token', None)
    if model:
        test = pd.DataFrame([data])
        prediction = model.predict(test)[0]
        print(prediction, file=sys.stderr)
        return prediction
    else:
        return "model not found"


@app.route('/')
def home():
    form = OurForm()
    return render_template('churn_form.html', form=form)


@app.route('/something/', methods=['post'])
def something():
    form = OurForm()
    print(request.form, file=sys.stderr)
    if form.validate_on_submit():
        prediction = churn_prediction(request.form)
        return jsonify({'prediction': int(prediction)})
    return jsonify(data=form.errors)
