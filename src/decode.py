import cv2


def decode_image(E, K):
    """
    Decode the image to reveal the hidden text.

    Args:
        E (numpy.ndarray): Encoded image.
        K (numpy.ndarray): Key pattern.

    Returns:
        numpy.ndarray: Decoded image showing the hidden text.
    """
    # Compute the absolute difference to reveal the text
    D = cv2.absdiff(E, K)
    # Enhance contrast for better visibility
    D = cv2.normalize(D, None, 0, 255, cv2.NORM_MINMAX)
    return D
