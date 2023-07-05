# import os
# import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


# Declare a flask app
app = Flask(__name__)


# Model saved with Keras model.save()
MODEL_PATH = 'L1L2_model.keras'

# Load your own trained model
model = load_model(MODEL_PATH)
print('Model loaded. Start serving...')


def model_predict(img, model):
    img = img.resize((180, 180))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)

    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)
        classes = {
            0: 'Asian-Green-Bee-Eater',
            1: 'Brown-Headed-Barbet',
            2: 'Cattle-Egret',
            3: 'Common-Kingfisher',
            4: 'Common-Myna',
            5: 'Common-Rosefinch',
            6: 'Common-Tailorbird',
            7: 'Coppersmith-Barbet',
            8: 'Forest-Wagtail',
            9: 'Gray-Wagtail',
            10: 'Hoopoe',
            11: 'House-Crow',
            12: 'Indian-Grey-Hornbill',
            13: 'Indian-Peacock',
            14: 'Indian-Pitta',
            15: 'Indian-Roller',
            16: 'Jungle-Babbler',
            17: 'Northern-Lapwing',
            18: 'Red-Wattled-Lapwing',
            19: 'Ruddy-Shelduck',
            20: 'Rufous-Treepie',
            21: 'Sarus-Crane',
            22: 'White-Breasted-Kingfisher',
            23: 'White-Breasted-Waterhen',
            24: 'White-Wagtail',
        }
        predicted_class_index = np.argmax(preds)
        # print(classes[predicted_class_index])

        # Process your result for human
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability

        result = classes[predicted_class_index]
        
        # # Serialize the result, you can add additional fields
        return jsonify(result=result, probability=pred_proba)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    # app.run(host='0.0.0.0', port=5000)
