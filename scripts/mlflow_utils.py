from config import config
import mlflow
import onnx


mlflow.set_tracking_uri(config()["mlflow_tracking_uri"])


def load_challenger_model():
    model_name = config()["model_name"]
    model = mlflow.onnx.load_model(f"models:/{model_name}@challenger")
    onnx.save_model(model, f"{config()['layers_model_path']}/{model_name}.onnx")


def promote_challenger_model():
    mlflow_client = mlflow.MlflowClient()
    model_name = config()["model_name"]
    challenger_version = mlflow_client.get_model_version_by_alias(
        model_name, "challenger"
    ).version
    champion_version = mlflow_client.get_model_version_by_alias(
        model_name, "champion"
    ).version
    mlflow_client.set_registered_model_alias(model_name, "champion", challenger_version)
    mlflow_client.set_registered_model_alias(
        model_name, "ex-champion", champion_version
    )
    mlflow_client.delete_registered_model_alias(model_name, "challenger")
