from flask import Flask, request, jsonify
from predict import predict_new_data

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predict():
    pred_q05, pred_q50, pred_q95 = predict_new_data(request.json)
    return jsonify({'Q05':pred_q05,
                    'Q50':pred_q50,
                    'Q95':pred_q95})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)