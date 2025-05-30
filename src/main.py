import cv2

from decode import decode_image
from encode import encode_image
from preprocess import load_and_preprocess_image


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
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font type
    font_scale = 1  # Font size scaling
    text_angle = 45  # Text rotation angle in degrees
    spacing_x = 1.4  # Horizontal text spacing multiplier
    spacing_y = 0.4  # Vertical text spacing multiplier
    letter_spacing = 0  # Pixel spacing between characters
    stripe_type = "binary"  # Stripe pattern type

    # Load and preprocess the image
    try:
        I = load_and_preprocess_image(image_path)
    except ValueError as e:
        print(e)
        return

    # Encode the image with hidden text and save with metadata
    E = encode_image(
        I,
        text_to_hide,
        output_encoded,
        p,
        min_thickness,
        max_thickness,
        strip_width,
        chunk_height,
        amplitude,
        font,
        font_scale,
        text_angle,
        spacing_x,
        spacing_y,
        letter_spacing,
        stripe_type,
    )

    # Decode the image using the encoded file
    try:
        D = decode_image(output_encoded)
        cv2.imwrite(output_decoded, D)
        print(f"Encoded image saved to {output_encoded}")
        print(f"Decoded image saved to {output_decoded}")
    except ValueError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
