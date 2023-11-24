import os


def config():
    tv_titles = [
        "Game of Thrones",
        "Breaking Bad",
        "Stranger Things",
        "The Walking Dead",
        "Friends",
        "The Big Bang Theory",
        "The Office",
        "Black Mirror",
        "True Detective",
        "Peaky Blinders",
    ]
    num_classes = len(tv_titles)
    dagshub_repo = "https://dagshub.com/PavloFesenko/gif_analyzer"
    mlflow_tracking_uri = f"{dagshub_repo}.mlflow"
    config_local = {
        "tv_titles": tv_titles,
        "num_classes": num_classes,
        "data_path": "../data",
        "test_gif_name": "0_GameofThrones_3o7abLOPn5UJ048sSY.gif",
        "models_path": "../models",
        "layers_model_path": "../layers/model",
        "model_name": "baseline",
        "tmp_gif_path": "../tmp.gif",
        "dagshub_repo": dagshub_repo,
        "mlflow_tracking_uri": mlflow_tracking_uri,
        "mlflow_experiment_name": "default",
    }
    config_aws = {
        "layers_model_path": "/opt",
        "tmp_gif_path": "/tmp/tmp.gif",
    }
    config_aws = config_local | config_aws
    if os.getenv("ENV") == "aws":
        return config_aws
    else:
        return config_local
