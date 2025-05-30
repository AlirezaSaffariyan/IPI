import cv2

from decode import decode_image
from encode import encode_image
from preprocess import load_and_preprocess_image
from utils import generate_key_pattern


def main():
    """
    Main function to encode and decode an image with hidden text.
    """
    # Input parameters
    input_path = "../images/"
    input_image = "sample.jpg"
    input_image_name = ".".join(input_image.split(".")[:-1])
    image_path = f"{input_path}{input_image}"
    text_to_hide = "SECRET"
    output_path = "../outputs/"
    output_encoded = f"{output_path}{input_image_name}-encoded.png"
    output_decoded = f"{output_path}{input_image_name}-decoded.png"
    p = 2  # Stripe period
    min_thickness = 1  # Minimum line thickness
    max_thickness = 5  # Maximum line thickness
    strip_width = 5  # Width of each vertical strip
    chunk_height = 5  # Height of each chunk
    amplitude = 0.3  # Strength of the hidden pattern

    # Load and preprocess the image
    try:
        I = load_and_preprocess_image(image_path)
    except ValueError as e:
        print(e)
        return

    height, width = I.shape

    # Generate key pattern
    K = generate_key_pattern(height, width, p, stripe_type="binary")

    # Encode the image with hidden text and chunk-based lines
    E = encode_image(
        I,
        text_to_hide,
        p,
        min_thickness,
        max_thickness,
        strip_width,
        chunk_height,
        amplitude,
    )

    # Decode the image to reveal the text
    D = decode_image(E, K)

    # Save results
    cv2.imwrite(output_encoded, E)
    cv2.imwrite(output_decoded, D)
    print(f"Encoded image saved to {output_encoded}")
    print(f"Decoded image saved to {output_decoded}")


if __name__ == "__main__":
    main()
