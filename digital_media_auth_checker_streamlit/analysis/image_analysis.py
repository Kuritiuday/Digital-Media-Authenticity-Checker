from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def generate_ela_image(image):

    temp_path = "temp.jpg"

    image.save(temp_path, quality=90)

    compressed = Image.open(temp_path)

    ela_image = ImageChops.difference(image, compressed)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    scale = 255.0 / max_diff if max_diff != 0 else 1

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    return ela_image


def analyze_image(image):

    width, height = image.size

    ela_image = generate_ela_image(image)

    ela_array = np.array(ela_image)

    ela_score = int(np.mean(ela_array))

    deepfake_score = min(100, ela_score * 2)

    real_score = 100 - deepfake_score

    status = "Deepfake Detected" if deepfake_score > 50 else "Authentic Media"

    result = {
        "ELA Score": ela_score,
        "Deepfake Probability (%)": deepfake_score,
        "Real Authenticity (%)": real_score,
        "Status": status
    }

    return result, ela_image