import argparse
import os

import cv2

from decode import decode_image
from encode import encode_image
from preprocess import load_and_preprocess_image


def encode_main(args):
    """
    Encode an image with hidden text and save it with metadata.

    Args:
        args: Parsed command-line arguments.
    """
    # Determine output filename if not provided
    if not args.output_encoded:
        input_name = ".".join(os.path.basename(args.input_image).split(".")[:-1])
        args.output_encoded = os.path.join(
            args.output_path, f"{input_name}-encoded.png"
        )

    try:
        # Load and preprocess the image
        I = load_and_preprocess_image(args.input_image)

        # Encode the image
        E = encode_image(
            I,
            args.text_to_hide,
            args.output_encoded,
            p=args.stripe_period,
            min_thickness=args.min_thickness,
            max_thickness=args.max_thickness,
            strip_width=args.strip_width,
            chunk_height=args.chunk_height,
            amplitude=args.amplitude,
            font=getattr(cv2, args.font),
            font_scale=args.font_scale,
            font_thickness=args.font_thickness,
            text_angle=args.text_angle,
            spacing_x=args.spacing_x,
            spacing_y=args.spacing_y,
            letter_spacing=args.letter_spacing,
            stripe_type=args.stripe_type,
        )

        print(f"Encoded image saved to {args.output_encoded}")
    except ValueError as e:
        print(e)


def decode_main(args):
    """
    Decode the hidden text from an encoded image.

    Args:
        args: Parsed command-line arguments.
    """
    # Determine output filename if not provided
    if not args.output_decoded:
        input_name = ".".join(os.path.basename(args.input_encoded).split(".")[:-1])
        if input_name.endswith("-encoded"):
            input_name = input_name.removesuffix("-encoded")
        args.output_decoded = os.path.join(
            args.output_path, f"{input_name}-decoded.png"
        )

    try:
        # Decode the image
        D = decode_image(args.input_encoded)

        # Save the decoded image
        cv2.imwrite(args.output_decoded, D)
        print(f"Decoded image saved to {args.output_decoded}")
    except ValueError as e:
        print(e)


def main():
    """
    Main function to handle encode or decode operations based on command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Encode or decode an image with hidden text."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Operation to perform: encode or decode"
    )

    # Encoder subparser
    encode_parser = subparsers.add_parser(
        "encode", help="Encode an image with hidden text"
    )
    encode_parser.add_argument(
        "--input-image",
        required=True,
        help="Path to the input image (e.g., ../images/sample.jpg)",
    )
    encode_parser.add_argument(
        "--text-to-hide",
        default="SECRET",
        help="Text to hide in the image (default: SECRET)",
    )
    encode_parser.add_argument(
        "--output-encoded",
        help="Path to save the encoded image (default: ../outputs/<input_name>-encoded.png)",
    )
    encode_parser.add_argument(
        "--input-path",
        default="../images/",
        help="Base path for input images (default: ../images/)",
    )
    encode_parser.add_argument(
        "--output-path",
        default="../outputs/",
        help="Base path for output images (default: ../outputs/)",
    )
    encode_parser.add_argument(
        "--stripe-period",
        type=int,
        default=2,
        help="Period of the stripes (default: 2)",
    )
    encode_parser.add_argument(
        "--min-thickness",
        type=int,
        default=1,
        help="Minimum line thickness (default: 1)",
    )
    encode_parser.add_argument(
        "--max-thickness",
        type=int,
        default=5,
        help="Maximum line thickness (default: 5)",
    )
    encode_parser.add_argument(
        "--strip-width",
        type=int,
        default=5,
        help="Width of each vertical strip (default: 5)",
    )
    encode_parser.add_argument(
        "--chunk-height", type=int, default=5, help="Height of each chunk (default: 5)"
    )
    encode_parser.add_argument(
        "--amplitude",
        type=float,
        default=0.3,
        help="Strength of the hidden pattern (default: 0.3)",
    )
    encode_parser.add_argument(
        "--font",
        default="FONT_HERSHEY_SIMPLEX",
        help="OpenCV font type (default: FONT_HERSHEY_SIMPLEX)",
    )
    encode_parser.add_argument(
        "--font-scale",
        type=float,
        default=1.0,
        help="Font size scaling factor (default: 1.0)",
    )
    encode_parser.add_argument(
        "--font-thickness",
        type=int,
        default=1,
        help="Font thickness (default: 1)",
    )
    encode_parser.add_argument(
        "--text-angle",
        type=float,
        default=45,
        help="Text rotation angle in degrees (default: 45)",
    )
    encode_parser.add_argument(
        "--spacing-x",
        type=float,
        default=1.4,
        help="Horizontal text spacing multiplier (default: 1.4)",
    )
    encode_parser.add_argument(
        "--spacing-y",
        type=float,
        default=0.4,
        help="Vertical text spacing multiplier (default: 0.4)",
    )
    encode_parser.add_argument(
        "--letter-spacing",
        type=int,
        default=0,
        help="Pixel spacing between characters (default: 0)",
    )
    encode_parser.add_argument(
        "--stripe-type",
        default="binary",
        choices=["binary", "sinusoidal"],
        help="Stripe pattern type (default: binary)",
    )

    # Decoder subparser
    decode_parser = subparsers.add_parser(
        "decode", help="Decode hidden text from an encoded image"
    )
    decode_parser.add_argument(
        "--input-encoded",
        required=True,
        help="Path to the encoded image (e.g., ../outputs/sample-encoded.png)",
    )
    decode_parser.add_argument(
        "--output-decoded",
        help="Path to save the decoded image (default: ../outputs/<input_name>-decoded.png)",
    )
    decode_parser.add_argument(
        "--output-path",
        default="../outputs/",
        help="Base path for output images (default: ../outputs/)",
    )

    args = parser.parse_args()

    if args.command == "encode":
        encode_main(args)
    elif args.command == "decode":
        decode_main(args)


if __name__ == "__main__":
    main()
