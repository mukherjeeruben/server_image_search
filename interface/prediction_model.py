from io import BytesIO
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import decode_predictions
import re as regular_expression

model = None


def read_image(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


def load_model():
    model = tf.keras.applications.Xception(weights="imagenet")
    print("Model loaded")
    return model


def predict(image: Image.Image):
    global model
    if model is None:
        model = load_model()

    image = np.asarray(image.resize((299, 299)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 127.5 - 1.0

    result = decode_predictions(model.predict(image), 1)[0]

    return regular_expression.sub('[^a-zA-Z0-9]+', ' ', result[0][1])



