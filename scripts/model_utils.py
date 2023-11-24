from config import config
import onnxruntime as ort


def predict(input):
    onnx_model_path = f"{config()['layers_model_path']}/{config()['model_name']}.onnx"
    session = ort.InferenceSession(onnx_model_path)
    prediction = session.run(None, {"time_distributed_input": input})[0]
    return prediction
