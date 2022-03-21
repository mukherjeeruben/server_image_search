from interface.prediction_model import predict, read_image
import requests


def predict_image(dataset):
    for item in dataset:
        try:
            image = read_image(requests.get(item['url'], timeout=5).content)
            item['title'] = item['title'] + " " + predict(image)
        except Exception as err:
            continue
    return dataset