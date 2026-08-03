from PIL import Image, ImageFilter, ImageOps
from scipy.ndimage import uniform_filter, gaussian_filter
import numpy as np
import os


class Image_Processor:

    def __init__(self, image_path, file_type=0):
        self.img = Image.open(image_path)
        self.original = self.img.copy()
        self.name = os.path.splitext(os.path.basename(image_path))[0]

        if file_type == 0:
            self.type = ".jpg"
        elif file_type == 1:
            self.type = ".png"
        else:
            self.type = ".jpg"

    def apply_blur(self):

        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        radius = 2

        kernel_size = radius * 2 + 1

        blurred = uniform_filter(arr, size=(kernel_size, kernel_size, 1))

        self.img = Image.fromarray(blurred.astype(np.uint8))

        print(f"Blurred {self.name}")

    def apply_blur_gaussian(self):

        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        self.img = Image.fromarray(
            gaussian_filter(arr, sigma=(1.7, 1.5, 0)).astype(np.uint8)
        )

        print(f"Gaussian Blur Applied")

    def apply_greyscale(self):

        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        weights = np.array([0.299, 0.587, 0.114])
        grey = (arr * weights).sum(axis=2)

        self.img = Image.fromarray(grey.astype(np.uint8))

        print(f"Greyscale Applied")

    def apply_vignette(self):
        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        height, width, _ = arr.shape

        center_x_position = width / 2
        center_y_position = height / 2

        y, x = np.ogrid[:height, :width]

        pixel_dist_from_center = np.sqrt(
            (x - center_x_position) ** 2 + (y - center_y_position) ** 2
        )

        corner_dist_from_center = np.sqrt(center_x_position**2 + center_y_position**2)

        distance_normalized = pixel_dist_from_center / corner_dist_from_center

        strength = 0.5
        mask = 1.0 - strength * (distance_normalized**2)

        output_arr = np.clip(arr * mask[..., np.newaxis], 0, 255).astype(np.uint8)

        self.img = Image.fromarray(output_arr)

        print(f"Vignette applied to image")

    def invert_image(self):

        arr = np.array(self.img.convert("RGB"), dtype=np.uint8)

        arr = 255 - arr

        self.img = Image.fromarray(arr)

        print(f"Image inverted")

    def apply_film_grain(self):
        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        height, width, _ = arr.shape

        sigma = 20
        noise_layer = (
            np.array(Image.effect_noise((width, height), sigma))[..., np.newaxis] - 128
        ) * 0.15
        # print(str(noise_layer.max()))

        self.img = Image.fromarray(
            np.clip((arr + noise_layer), 0, 255).astype(np.uint8)
        )

        print(f"Grain applied")

    # Make the image kind of brown
    def apply_sepia(self):
        arr = np.array(self.img.convert("RGB"), dtype=np.float32)

        sepia_matrix = np.array(
            [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
        )

        # arr @ sepia_matrix.T applies the matrix to every pixel's [R,G,B] at once
        sepia = arr @ sepia_matrix.T

        # Values can exceed 255 after the previous line, so this caps the values
        sepia = np.clip(sepia, 0, 255)

        self.img = Image.fromarray(sepia.astype(np.uint8))

        print(f"Sepia filter applied")

    # Edge finding
    def find_edges(self):

        self.img = self.img.convert("L").filter(ImageFilter.FIND_EDGES)

        print(f"Edges found")

    # Increase Saturation
    def boost_saturation(self):
        arr = np.array(self.img.convert("RGB"), dtype=np.uint8)

        weights = np.array([0.299, 0.587, 0.114])
        grey = (arr * weights).sum(axis=2, keepdims=True)
        result = grey + ((arr - grey) * 2)

        self.img = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

        print(f"Image saturated")

    def save_image(self):
        self.img.save(f"Updated_{self.name}{self.type}")
