from churn import app
from churn.models import Result

@app.route('/')
def hello():
    return "Hello World!"