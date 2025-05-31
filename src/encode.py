import cv2
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from utils import (
    adjust_brightness,
    create_text_image,
    generate_key_pattern,
    generate_shifted_key,
    map_brightness_to_thickness,
)


def encode_image(
    I,
    text_to_hide,
    output_path,
    p=10,
    min_thickness=1,
    max_thickness=10,
    strip_width=10,
    chunk_height=50,
    amplitude=0.1,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=1,
    font_thickness=1,
    text_angle=0,
    spacing_x=1.2,
    spacing_y=1.2,
    letter_spacing=0,
    stripe_type="binary",
):
    """
    Encode the image into vertical lines with varying thickness per chunk, hide text, and save with metadata.

    Args:
        I (numpy.ndarray): Grayscale input image.
        text_to_hide (string): Text to hide.
        output_path (string): Path to save the encoded image.
        p (int): Period of the stripes (default: 10).
        min_thickness (int): Minimum line thickness (default: 1).
        max_thickness (int): Maximum line thickness (default: 10).
        strip_width (int): Width of each vertical strip (default: 10).
        chunk_height (int): Height of each chunk (default: 50).
        amplitude (float): Strength of the stripe pattern (default: 0.1).
        font (int): OpenCV font type (default: cv2.FONT_HERSHEY_SIMPLEX).
        font_scale (float): Font size scaling factor (default: 1).
        font_thickness (int): Font thickness (default: 1).
        text_angle (float): Text rotation angle in degrees (default: 0).
        spacing_x (float): Horizontal text spacing multiplier (default: 1.2).
        spacing_y (float): Vertical text spacing multiplier (default: 1.2).
        letter_spacing (int): Pixel spacing between characters (default: 0).
        stripe_type (string): Stripe pattern type ('binary' or 'sinusoidal', default: 'binary').

    Returns:
        numpy.ndarray: Encoded image.
    """
    height, width = I.shape

    # Adjust brightness to avoid extremes
    I_adjusted = adjust_brightness(I, min_val=15, max_val=240)

    # Generate key patterns and text image
    K = generate_key_pattern(height, width, p, stripe_type=stripe_type)

    K_shifted = generate_shifted_key(K, p // 2)
    T_normalized = create_text_image(
        text_to_hide,
        height,
        width,
        font,
        font_scale,
        thickness=font_thickness,
        angle=text_angle,
        spacing_x=spacing_x,
        spacing_y=spacing_y,
        letter_spacing=letter_spacing,
    )

    # Create the stripe pattern with hidden text
    E_stripe = K * (1 - T_normalized) + K_shifted * T_normalized

    # Create the line image with varying thickness per chunk
    line_image = np.zeros_like(I)
    for x in range(0, width, strip_width):
        for y in range(0, height, chunk_height):
            # Extract the chunk
            chunk = I_adjusted[y : y + chunk_height, x : x + strip_width]
            if chunk.size == 0:
                continue
            # Compute average brightness
            avg_brightness = np.mean(chunk)
            # Map to thickness (brighter = thicker)
            thickness = map_brightness_to_thickness(
                avg_brightness, min_thickness, max_thickness, 15, 240
            )
            # Draw line segment for this chunk
            start_x = x + (strip_width - thickness) // 2
            end_x = start_x + thickness
            line_image[y : y + chunk_height, start_x:end_x] = 255

    # Blend the line image with the stripe pattern
    E = line_image * (1 - amplitude) + E_stripe * amplitude
    E = np.clip(E, 0, 255).astype(np.uint8)

    # Save the image with metadata using Pillow
    E_pil = Image.fromarray(E)

    # Create a PngInfo container for metadata
    png_metadata = PngInfo()
    png_metadata.add_text("stripe_period", str(p))
    png_metadata.add_text("stripe_type", stripe_type)

    E_pil.save(output_path, exif=Image.Exif().tobytes(), pnginfo=png_metadata)

    return E
