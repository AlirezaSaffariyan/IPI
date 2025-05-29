import cv2


def load_and_preprocess_image(image_path):
    """
    Load an image and convert it to grayscale.

    Args:
        image_path (str): Path to the input image.

    Returns:
        numpy.ndarray: Grayscale image.

    Raises:
        ValueError: If the image cannot be loaded.
    """

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image at {image_path}")
    return image
