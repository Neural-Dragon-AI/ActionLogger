import argparse
from action_logger import ActionLogger  # Assuming the ActionLogger class is defined in a file called action_logger.py

def main():
    parser = argparse.ArgumentParser(description="Capture screen, keyboard, and mouse actions.")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Capture duration in seconds. (default: 60)")
    parser.add_argument("-r", "--rate", type=int, default=10, help="Capture rate in frames per second. (default: 10)")
    parser.add_argument("-s", "--save_every", type=int, default=60, help="Save interval in seconds. (default: 60)")
    parser.add_argument("-o", "--output", type=str, default="output", help="Output folder for captured data. (default: output)")
    parser.add_argument("-f", "--resize_factor", type=float, default=3.16, help="Resize factor for screen captures. (default: 3.16)")

    args = parser.parse_args()

    action_logger = ActionLogger(
        capture_rate=args.rate,
        output_folder=args.output,
        resize_factor=args.resize_factor
    )

    try:
        action_logger.run(
            capture_duration=args.duration,
            save_every=args.save_every
        )
    except KeyboardInterrupt:
        print("Interrupted. Stopping the ActionLogger...")
        action_logger.stop()
        action_logger.save_mouse_positions(action_logger.mouse_positions)
        action_logger.save_keyboard_buffer()
        action_logger.save_screen_timestamps()
        print("Data saved. Exiting.")

if __name__ == "__main__":
    main()
