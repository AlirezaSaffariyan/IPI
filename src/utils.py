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
    Map average brightness to a line thickness, where darker areas produce thicker lines.

    Args:
        avg_brightness (float): Average brightness of the chunk.
        min_thickness (int): Minimum line thickness.
        max_thickness (int): Maximum line thickness.
        min_brightness (int): Minimum brightness value.
        max_brightness (int): Maximum brightness value.

    Returns:
        int: Calculated line thickness.
    """
    # Inverse mapping: darker (lower brightness) -> thicker (higher thickness)
    thickness = max_thickness - (avg_brightness - min_brightness) * (
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


def create_text_image(text, height, width, font_scale=1, thickness=2):
    """
    Create an image with repeated text to be hidden.

    Args:
        text (str): Text to hide.
        height (int): Image height.
        width (int): Image width.
        font_scale (float): Font size scaling factor (default: 1).
        thickness (int): Text thickness (default: 2).

    Returns:
        numpy.ndarray: Normalized text image (0-1).
    """
    T = np.zeros((height, width), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    for y in range(0, height, text_size[1] + 10):
        for x in range(0, width, text_size[0] + 10):
            cv2.putText(
                T, text, (x, y + text_size[1]), font, font_scale, 255, thickness
            )
    return T / 255.0
