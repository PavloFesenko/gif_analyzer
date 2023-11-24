import pytest
import boto3
import requests
import json
import numpy as np


@pytest.fixture(scope="session")
def lambda_name(pytestconfig):
    return pytestconfig.getoption("lambda_name")


@pytest.fixture(scope="session")
def lambda_url(lambda_name):
    lambda_client = boto3.client("lambda")
    lambda_url_config = lambda_client.get_function_url_config(FunctionName=lambda_name)
    url = lambda_url_config["FunctionUrl"]
    return url


def test_hello(lambda_url):
    response = requests.get(f"{lambda_url}/hello")
    response_status = response.status_code
    response_message = response.json()["message"]

    assert response_status == 200
    assert response_message == "Hello World"


def test_predict(lambda_url):
    gif_url = "https://media.giphy.com/media/3o7abLOPn5UJ048sSY/giphy.gif"
    response = requests.get(f"{lambda_url}/{gif_url}")
    response_status = response.status_code
    response_prediction = json.loads(response.json()["prediction"])
    argmax_prediction = np.argmax(response_prediction[0])

    assert response_status == 200
    assert argmax_prediction == 0
