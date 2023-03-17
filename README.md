
# ActionLogger

ActionLogger is a lightweight Python script that captures screen, keyboard presses, and mouse positions at a specified frame rate. The captured data is saved in an output folder.

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:
pip install -r requirements.txt

perl
Copy code

## Usage

To run the ActionLogger, use the provided `run_action_logger.py` script with optional command-line arguments:

python run_action_logger.py -d <duration> -r <rate> -s <save_every> -o <output_folder> -f <resize_factor>



- `-d <duration>`: Capture duration in seconds (default: 60)
- `-r <rate>`: Capture rate in frames per second (default: 10)
- `-s <save_every>`: Save interval in seconds (default: 60)
- `-o <output_folder>`: Output folder for captured data (default: output)
- `-f <resize_factor>`: Resize factor for screen captures (default: 3.16)

For example, to run the action logger for 120 seconds at 10 FPS, saving data every 60 seconds to the "output" folder, and resizing screen captures by a factor of 3.16:

python run_action_logger.py -d 120 -r 10 -s 60 -o "output" -f 3.16

markdown
Copy code

Press `Ctrl+C` to stop the ActionLogger and save the remaining data.

## Output

The captured data is saved in the specified output folder in the following format:

- `mouse_positions.json`: A JSON file containing the captured mouse positions
- `keyboard_buffer.json`: A JSON file containing the captured keyboard presses
- `screen_timestamps.json`: A JSON file containing the timestamps of captured screen images
- `screen_<timestamp>.png`: A series of PNG images containing the captured screen images, resized by the specified resize factor
You can create a README.md file in your project folder and paste this content into it. Make sure to adjust the content as needed to fit your specific implementation or requirements.