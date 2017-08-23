import sys
import numpy
import os
import pandas as pd
from flask import request, jsonify, render_template
from sklearn.externals import joblib
from wtforms import IntegerField
from churn import app, db
from flask_wtf import FlaskForm
from churn.models import churn_data_from_user

basedir = os.path.abspath(os.path.dirname(__file__))

try:
    print("try", file=sys.stderr)
    model = joblib.load(basedir+"/churn_model.pkl")
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
    # data = data.to_dict()
    # data.pop('csrf_token', None)
    # print(data, file=sys.stderr)
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
    churnData = churn_data_from_user()
    churnData.State = request.form['State']
    churnData.Account_Length = request.form['Account_Length']
    churnData.Area_Code = request.form['Area_Code']
    churnData.Intl_Plan = request.form['Intl_Plan']
    churnData.VMail_Plan = request.form['VMail_Plan']
    churnData.VMail_Message = request.form['VMail_Message']
    churnData.Day_Mins = request.form['Day_Mins']
    churnData.Day_Calls = request.form['Day_Calls']
    churnData.Eve_Mins = request.form['Eve_Mins']
    churnData.Eve_Calls = request.form['Eve_Calls']
    churnData.Night_Mins = request.form['Night_Mins']
    churnData.Night_Calls = request.form['Night_Calls']
    churnData.Intl_Mins = request.form['Intl_Mins']
    churnData.Intl_Calls = request.form['Intl_Calls']
    churnData.CustServ_Calls = request.form['CustServ_Calls']

    try:
        db.session.add(churnData)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

    db_data = churn_data_from_user()

    # for row in db_data.query.all():
    #     row = row.__dict__
    #     row = row.pop('_sa_instance_state', None)
    #     print(row, file=sys.stderr)

    user = db_data.query.order_by('-id').first()
    print(user, file=sys.stderr)
    user = user.__dict__
    user.pop('_sa_instance_state', None)
    user.pop('id', None)
    print(user, file=sys.stderr)


    form = OurForm()
    # print(request.form, file=sys.stderr)
    if form.validate_on_submit():
        prediction = churn_prediction(user)
        return jsonify({'prediction': int(prediction)})
    return jsonify(data=form.errors)
