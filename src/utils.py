import cv2
import numpy as np


def adjust_brightness(image, min_val=15, max_val=240):
    """
    Adjust the brightness of the image to a new range to avoid extreme values.

    Args:
        image (numpy.ndarray): Grayscale image.
        min_val (int): Minimum brightness value (default: 15).
        max_val (int): Maximum brightness value (default: 240).

    Returns:
        numpy.ndarray: Adjusted image.
    """
    return cv2.normalize(image, None, min_val, max_val, cv2.NORM_MINMAX)


def map_brightness_to_thickness(
    avg_brightness, min_thickness, max_thickness, min_brightness, max_brightness
):
    """
    Map average brightness to a line thickness, where brighter areas produce thicker lines.

    Args:
        avg_brightness (float): Average brightness of the chunk.
        min_thickness (int): Minimum line thickness.
        max_thickness (int): Maximum line thickness.
        min_brightness (int): Minimum brightness value.
        max_brightness (int): Maximum brightness value.

    Returns:
        int: Calculated line thickness.
    """
    # Linear mapping: brighter (higher brightness) -> thicker (higher thickness)
    thickness = min_thickness + (avg_brightness - min_brightness) * (
        max_thickness - min_thickness
    ) / (max_brightness - min_brightness)
    return int(np.clip(thickness, min_thickness, max_thickness))


def generate_key_pattern(height, width, p, stripe_type="binary"):
    """
    Generate a vertical stripe pattern (key pattern K).

    Args:
        height (int): Image height.
        width (int): Image width.
        p (int): Period of the stripes.
        stripe_type (str): 'binary' or 'sinusoidal' (default: 'binary').

    Returns:
        numpy.ndarray: Stripe pattern image.
    """
    K = np.zeros((height, width), dtype=np.uint8)
    for x in range(width):
        if stripe_type == "binary":
            K[:, x] = 255 if (x % p) < p // 2 else 0
        elif stripe_type == "sinusoidal":
            K[:, x] = (255 * (1 + np.sin(2 * np.pi * x / p))) / 2
    return K


def generate_shifted_key(K, shift):
    """
    Shift the key pattern horizontally.

    Args:
        K (numpy.ndarray): Original key pattern.
        shift (int): Number of pixels to shift.

    Returns:
        numpy.ndarray: Shifted key pattern.
    """
    M = np.float32([[1, 0, shift], [0, 1, 0]])
    K_shifted = cv2.warpAffine(
        K, M, (K.shape[1], K.shape[0]), borderMode=cv2.BORDER_WRAP
    )
    return K_shifted


def create_text_image(
    text,
    height,
    width,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=1,
    thickness=2,
    angle=0,
    spacing_x=1.2,
    spacing_y=1.2,
    letter_spacing=0,
):
    """
    Create an image with repeated, rotated text to cover the entire image without overlap, with adjustable letter spacing.

    Args:
        text (str): Text to hide.
        height (int): Image height.
        width (int): Image width.
        font (int): OpenCV font type (default: cv2.FONT_HERSHEY_SIMPLEX).
        font_scale (float): Font size scaling factor (default: 1).
        thickness (int): Text thickness (default: 2).
        angle (float): Text rotation angle in degrees (default: 0).
        spacing_x (float): Horizontal spacing multiplier for text repetition (default: 1.2).
        spacing_y (float): Vertical spacing multiplier for text repetition (default: 1.2).
        letter_spacing (int): Pixel spacing between characters within each text instance (default: 0).

    Returns:
        numpy.ndarray: Normalized text image (0-1).
    """
    # Create a temporary canvas to calculate total text width with letter spacing
    temp_canvas = np.zeros((100, 1000), dtype=np.uint8)
    x_pos = 0
    char_positions = []
    for char in text:
        char_size = cv2.getTextSize(char, font, font_scale, thickness)[0]
        char_w = char_size[0]
        char_positions.append((char, x_pos, char_w))
        x_pos += char_w + letter_spacing

    # Total text width including letter spacing
    text_w = x_pos - letter_spacing if text else 0
    text_h = cv2.getTextSize(text[0] if text else "A", font, font_scale, thickness)[0][
        1
    ]

    # Account for rotation: calculate the bounding box of rotated text
    angle_rad = np.radians(angle)
    rotated_w = int(abs(text_w * np.cos(angle_rad)) + abs(text_h * np.sin(angle_rad)))
    rotated_h = int(abs(text_w * np.sin(angle_rad)) + abs(text_h * np.cos(angle_rad)))

    # Create a larger canvas to ensure coverage
    diagonal = int(np.sqrt(height**2 + width**2)) + max(rotated_w, rotated_h)
    canvas = np.zeros((diagonal, diagonal), dtype=np.uint8)

    # Use customizable step sizes for text repetition
    step_x = max(int(rotated_w * spacing_x), 1)
    step_y = max(int(rotated_h * spacing_y), 1)

    # Tile text across the canvas, starting from negative coordinates
    for y in range(-rotated_h, diagonal + rotated_h, step_y):
        for x_base in range(-rotated_w, diagonal + rotated_w, step_x):
            for char, x_offset, _ in char_positions:
                canvas = cv2.putText(
                    canvas,
                    char,
                    (x_base + x_offset, y + text_h),
                    font,
                    font_scale,
                    255,
                    thickness,
                )

    # Rotate the canvas
    if angle != 0:
        M = cv2.getRotationMatrix2D((diagonal / 2, diagonal / 2), angle, 1)
        canvas = cv2.warpAffine(canvas, M, (diagonal, diagonal), borderValue=0)

    # Crop to the original image size, centered
    start_x = (diagonal - width) // 2
    start_y = (diagonal - height) // 2
    T = canvas[start_y : start_y + height, start_x : start_x + width]

    # Ensure the output matches the image size
    if T.shape != (height, width):
        T = cv2.resize(T, (width, height), interpolation=cv2.INTER_NEAREST)

    return T / 255.0  # Normalize to 0-1
