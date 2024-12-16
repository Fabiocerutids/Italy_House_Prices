from flask import Flask, request, jsonify
from predict import predict_new_data

app = Flask(__name__)

@app.route("/predict", methods=['POST'])
def predict():
    pred = predict_new_data(request.json)
    return jsonify({'Prediction': pred})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)