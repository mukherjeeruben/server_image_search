from interface.prediction_model import predict, read_image
import requests


def predict_image(dataset):
    for item in dataset:
        try:
            image = read_image(requests.get(item['url']).content)
            item['title'] = item['title'] + " " + predict(image)
        except Exception as err:
            print(err)
            continue
    return dataset