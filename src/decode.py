import cv2
from PIL import Image

from preprocess import load_and_preprocess_image
from utils import generate_key_pattern


def decode_image(encoded_path):
    """
    Decode the hidden text from the encoded image using embedded metadata.

    Args:
        encoded_path (string): Path to the encoded image.

    Returns:
        numpy.ndarray: Decoded image showing the hidden text.

    Raises:
        ValueError: If metadata is missing or invalid.
    """
    # Load the encoded image
    E = load_and_preprocess_image(encoded_path)

    # Read metadata using Pillow
    try:
        E_pil = Image.open(encoded_path)
        metadata = E_pil.info
        p = int(metadata.get("stripe_period", 10))  # Default to 10 if missing
        stripe_type = metadata.get("stripe_type", "binary")  # Default to binary
    except Exception as e:
        raise ValueError(f"Could not read metadata from {encoded_path}: {e}")

    # Regenerate the key pattern
    height, width = E.shape
    K = generate_key_pattern(height, width, p, stripe_type=stripe_type)

    # Decode using absdiff
    D = cv2.absdiff(E, K)
    # Enhance contrast for better visibility
    D = cv2.normalize(D, None, 0, 255, cv2.NORM_MINMAX)
    return D
