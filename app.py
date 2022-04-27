"""
A sample Hello World server.
"""
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

import numpy as np
import pandas as pd
import pickle
import io
from sklearn.preprocessing import StandardScaler

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


@app.route('/check')
def check():

    inputLine="4462,-2.30334956758553,1.759247460267,-0.359744743330052,2.33024305053917,-0.821628328375422,-0.0757875706194599,0.562319782266954,-0.399146578487216,-0.238253367661746,-1.52541162656194,2.03291215755072,-6.56012429505962,0.0229373234890961,-1.47010153611197,-0.698826068579047,-2.28219382856251,-4.78183085597533,-2.61566494476124,-1.33444106667307,-0.430021867171611,-0.294166317554753,-0.932391057274991,0.172726295799422,-0.0873295379700724,-0.156114264651172,-0.542627889040196,0.0395659889264757,-0.153028796529788,239.93"

    modelFileName="storedModel.pckl"

    # load the model from disk
    loaded_model = pickle.load(open(modelFileName, 'rb'))

    # Header line
    csvHeader="""Time,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,Amount
    """

    # Create datafile
    TESTDATA=csvHeader+"\n"+inputLine
    df = pd.read_csv(io.StringIO(TESTDATA), sep=",")

    # Prepare scaler
    sc=StandardScaler()
    sc.set_params(**{'copy': True, 'with_mean': True, 'with_std': True})

    # Transform ammount column
    df['normAmount'] = sc.fit_transform(df['Amount'].values.reshape (-1,1))

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
