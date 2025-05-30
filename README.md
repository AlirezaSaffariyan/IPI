# IPI (Invisible Personal Information)

This project provides a Python-based tool to encode hidden text within an image using vertical line patterns and decode the text from the encoded image. The encoding process embeds text in a grayscale image by combining vertical lines (with thickness based on image brightness) and a stripe pattern that conceals the text. The decoding process reveals the hidden text using metadata embedded in the encoded image, eliminating the need for a separate key file.

## Features

- **Encoding**: Hide text in an image using vertical lines and stripe patterns.
  - Vertical lines vary in thickness based on image brightness (brighter areas = thicker lines).
  - Customizable text properties: font, scale, rotation angle, horizontal/vertical spacing, and letter spacing.
  - Embeds stripe pattern metadata (`stripe_period`, `stripe_type`) in the encoded image for self-contained decoding.
- **Decoding**: Reveal hidden text from an encoded image alone, using embedded metadata.
- **Separated Workflows**: Encode or decode images independently via a command-line interface.
- **Image Processing**: Adjusts brightness to a range of 15–240 for consistent encoding.
- **Dependencies**: Uses OpenCV, NumPy, and Pillow for image processing and metadata handling.

## Project Structure

```bash
IPI/
├── src/
│ ├── main.py # Command-line interface for encoding/decoding
│ ├── preprocess.py # Image loading and preprocessing
│ ├── utils.py # Utility functions (brightness, patterns, text)
│ ├── encode.py # Encoding logic with metadata
│ └── decode.py # Decoding logic using metadata
├── images/ # Input images (e.g., sample.jpg)
├── outputs/ # Encoded/decoded images (e.g., sample-encoded.png)
├── requirements.txt # Dependencies
├── LICENSE # Project LICENSE
└── README.md # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- A sample grayscale or color image (e.g., `sample.jpg`) in the `images/` folder

## Installation

- **Clone the Repository**:

```bash
git clone https://github.com/AlirezaSaffariyan/IPI.git
cd IPI
```

- **Install Dependencies**:

  ```bash
  pip install -r src/requirements.txt
  ```

  The `requirements.txt` includes:

  - `numpy==2.2.6`
  - `opencv-python==4.11.0.86`
  - `pillow==11.2.1`

- **Prepare an Input Image**:
  - Place a sample image (e.g., `sample.jpg`) in the `images/` folder.
  - The program converts color images to grayscale automatically.

## Usage

The program supports two commands: `encode` to hide text in an image and `decode` to reveal hidden text. Run commands from the `src/` directory.

### Encoding

Hide text in an image and save the encoded image with metadata.

```bash
cd src
python main.py encode --input-image ../images/sample.jpg
```

**Output**: Saves `../outputs/sample-encoded.png`.

**Optional Parameters**:

```bash
python main.py encode --input-image ../images/sample.jpg --output-encoded ../outputs/custom-encoded.png --text-to-hide HELLO --stripe-period 4 --spacing-x 1.2 --spacing-y 0.6
```

### Decoding

Reveal hidden text from an encoded image.

```bash
cd src
python main.py decode --input-encoded ../outputs/sample-encoded.png
```

**Output**: Saves `../outputs/sample-encoded-decoded.png`.

**Optional Parameters**:

```bash
python main.py decode --input-encoded ../outputs/sample-encoded.png --output-decoded ../outputs/custom-decoded.png
```

### Help

View available options:

```bash
python main.py --help
python main.py encode --help
python main.py decode --help
```

## Parameters

### Encoding Parameters

`--input-image` (required): Path to the input image (e.g., `../images/sample.jpg`).

`--text-to-hide`: Text to hide (default: `SECRET`).

`--output-encoded`: Output path for the encoded image (default: `../outputs/<input_name>-encoded.png`).

`--input-path`: Base path for input images (default: `../images/`).

`--output-path`: Base path for output images (default: `../outputs/`).

`--stripe-period`: Stripe pattern period (default: `2`).

`--min-thickness`: Minimum line thickness (default: `1`).

`--max-thickness`: Maximum line thickness (default: `5`).

`--strip-width`: Width of vertical strips (default: `5`).

`--chunk-height`: Height of each chunk (default: `5`).

`--amplitude`: Strength of the hidden pattern (default: `0.3`).

`--font`: OpenCV font (default: `FONT_HERSHEY_SIMPLEX`; options: `FONT_HERSHEY_DUPLEX`, etc.).

`--font-scale`: Font size scaling (default: `1.0`).

`--text-angle`: Text rotation angle in degrees (default: `45`).

`--spacing-x`: Horizontal text repetition spacing multiplier (default: `1.4`).

`--spacing-y`: Vertical text repetition spacing multiplier (default: `0.4`).

`--letter-spacing`: Pixel spacing between characters (default: `0`).

`--stripe-type`: Stripe pattern type (`binary` or `sinusoidal`, default: `binary`).

### Decoding Parameters

`--input-encoded` (required): Path to the encoded image (e.g., `../outputs/sample-encoded.png`).

`--output-decoded`: Output path for the decoded image (default: `../outputs/<input_name>-decoded.png`).

`--output-path`: Base path for output images (default: `../outputs/`).

## How It Works

- **Encoding**:
  - Loads a grayscale image (converts color images automatically).
  - Adjusts brightness to a 15–240 range.
  - Divides the image into vertical strips and chunks, drawing lines with thickness based on chunk brightness (brighter = thicker).
  - Embeds text using a stripe pattern, controlled by `stripe_period` and `stripe_type`.
  - Saves the encoded image as a PNG with metadata for decoding.
- **Decoding**:

  - Loads the encoded image and reads its metadata (`stripe_period`, `stripe_type`).
  - Regenerates the stripe pattern (key) using the metadata.
  - Computes the absolute difference between the encoded image and key to reveal the hidden text.
  - Saves the decoded image showing the text.

## Example

- **Encode**:

  ```bash
  python main.py encode --input-image ../images/sample.jpg --text-to-hide HELLO
  ```

  - Input: `../images/sample.jpg`
  - Output: `../outputs/sample-encoded.png`

- **Decode**:

  ```bash
  python main.py decode --input-encoded ../outputs/sample-encoded.png
  ```

  - Input: `../outputs/sample-encoded.png`
  - Output: `../outputs/sample-encoded-decoded.png`

## Notes

- **Metadata**: Decoding relies on PNG metadata. Use PNG format for encoded images to preserve `stripe_period` and `stripe_type`.

- **Image Format**: Input images can be any format supported by OpenCV (e.g., JPG, PNG), but encoded/decoded images are PNGs.

- **Error Handling**: The program provides clear error messages for invalid inputs or missing metadata.

- **Customization**: Adjust parameters like `spacing-x`, `spacing-y`, or `letter-spacing` to control text appearance, but ensure values prevent text overlap (check decoded output for clarity).

- **Performance**: Encoding/decoding time depends on image size and chunk/strip settings. Smaller strip-width or chunk`-height` increases processing time.

## Limitations

- Decoding requires the encoded image to retain its metadata. Converting to non-metadata formats (e.g., JPEG) will prevent decoding unless defaults match.
- Small `stripe-period` values (e.g., `2`) or high `amplitude` (e.g., `0.3`) may make the hidden text faintly visible in the encoded image.
- Text legibility in the decoded image depends on font size, spacing, and image resolution.
