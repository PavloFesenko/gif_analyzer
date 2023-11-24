import requests
import numpy as np
from PIL import Image, ImageOps


def save_gif(full_path, url):
    response = requests.get(url)
    gif = response.content
    with open(full_path, "wb") as f:
        f.write(gif)


def frames_from_gif(full_path, n_frames=10, output_size=(224, 224)):
    with Image.open(full_path) as gif:
        frame_count = gif.n_frames
        frame_step = max(1, int(frame_count / n_frames))
        frames = []
        for i in range(n_frames):
            try:
                n = i * frame_step + 1
                gif.seek(n)
                image = ImageOps.pad(gif, output_size, color="black").convert("RGB")
                frame = np.array(image, dtype=np.float32)
            except EOFError:
                frame = np.zeros_like(frame, dtype=np.float32)

            frames.append(frame)

    return np.array(frames)
