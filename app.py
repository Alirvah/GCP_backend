"""
A sample Hello World server.
"""
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import request

import numpy as np
import pandas as pd
import pickle
import io
from sklearn.preprocessing import StandardScaler


import glob

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)


@app.route('/check', methods=['POST'])
def check():

    data = request.get_json(force=True)

    inputLine = data['trans']

    modelFileName="storedModel.pckl"

    # load the model from disk
    loaded_model = pickle.load(open(modelFileName, 'rb'))

    # Header line
    csvHeader="""Time,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,Amount
    """

    # Create datafile
    TESTDATA=csvHeader+"\n"+str(inputLine)
    df = pd.read_csv(io.StringIO(TESTDATA), sep=",")

    # Prepare scaler
    sc=StandardScaler()
    sc.set_params(copy=True, with_mean=True, with_std=True)

    # Transform ammount column
    df['normAmount'] = 0 

    # Remove not needed columns
    df = df.drop (['Time', 'Amount'], axis = 1);

    # load the model from disk
    loaded_model = pickle.load(open(modelFileName, 'rb'))
    result1 = loaded_model.predict(df.iloc[[0]])[0]
    result = {"result":'OK' if result1 == 0 else 'FRAUD'}
    return jsonify(result)
        

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
