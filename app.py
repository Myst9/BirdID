from flask import Flask, request, render_template, jsonify
from gevent.pywsgi import WSGIServer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from util import base64_to_pil


app = Flask(__name__)

MODEL_PATH = 'L1L2_model.keras'
model = load_model(MODEL_PATH)
print('Model loaded. Starting server...')


def model_predict(img, model):
    img = img.resize((180, 180))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)

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
    result = classes[predicted_class_index]

    return (preds, result)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)
        
        # Make prediction
        prediction = model_predict(img, model)
        pred = prediction[0]
        result = prediction[1]
        pred_probability = "{:.3f}".format(np.amax(pred)) 
        
        return jsonify(result=result, probability=pred_probability)

    return None


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
