from config import config
import fastapi
import mangum
import numpy as np
import PIL
import onnxruntime
import gif_utils
import model_utils
import json


app = fastapi.FastAPI()
handler = mangum.Mangum(app)


@app.get("/hello")
async def hello():
    print(f"FastAPI: {fastapi.__version__}")
    print(f"NumPy: {np.__version__}")
    print(f"Pillow: {PIL.__version__}")
    print(f"ONNX runtime: {onnxruntime.__version__}")
    onnx_model_path = f"{config()['layers_model_path']}/{config()['model_name']}.onnx"
    with open(onnx_model_path, "r"):
        print(f"{config()['model_name']}.onnx is read")
    return {"message": "Hello World"}


@app.get("/{url:path}")
async def predict(url: str):
    gif_path = f'{config()["tmp_gif_path"]}'
    gif_utils.save_gif(gif_path, url)
    frames = gif_utils.frames_from_gif(gif_path)
    frames = np.expand_dims(frames, axis=0)
    prediction = model_utils.predict(frames)
    return {"url": url, "prediction": json.dumps(prediction.tolist())}
