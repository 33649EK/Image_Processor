import argparse
from PIL import Image
from .Image_Processor import Image_Processor


def main() -> None:

    # Set up cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", default="")
    parser.add_argument("-b", "--blur", action="store_true")
    parser.add_argument("-bg", "--blur_gaussian", action="store_true")
    parser.add_argument("-i", "--invert", action="store_true")
    parser.add_argument("-e", "--edge", action="store_true")
    parser.add_argument("-v", "--vignette", action="store_true")
    parser.add_argument("-s", "--sepia", action="store_true")
    parser.add_argument("-fg", "--film_grain", action="store_true")
    parser.add_argument("-g", "--grayscale", "--greyscale", action="store_true")
    parser.add_argument("-sat", "--saturate", action="store_true")
    args = parser.parse_args()

    # extraxt image filename from arguments
    image_to_open = args.filename.strip()

    # Ask user whether they want .jpg or .png as output
    file_type = int(
        input(
            "What file type would you like for the output image?\nPress 0 for '.jpg', or 1 for '.png': "
        )
    )

    # Create image object
    image = Image_Processor(image_to_open, file_type)

    # Following if statements apply any filters whose arguments stored true
    if args.film_grain:
        image.apply_film_grain()

    if args.blur:
        image.apply_blur()

    if args.blur_gaussian:
        image.apply_blur_gaussian()

    if args.grayscale:
        image.apply_greyscale()

    if args.sepia:
        image.apply_sepia()

    if args.saturate:
        image.boost_saturation()

    if args.vignette:
        image.apply_vignette()

    if args.edge:
        image.find_edges()

    if args.invert:
        image.invert_image()

    # save final image to current directory
    image.save_image()
