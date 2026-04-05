import argparse
import json
import sys

from statscrypt.repl import start_repl_interactive, start_repl_json


def send_json_message(type: str, payload: any):
    """Sends a structured JSON message to stdout for IPC."""
    message = json.dumps({"type": type, "payload": payload})
    sys.stdout.write(message + "\n")
    sys.stdout.flush()


def main():
    """
    Main entry point for the statscrypt command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="statscrypt: A Stata-like interpreter in Python."
    )
    parser.add_argument(
        "--json", action="store_true", help="Run in JSON mode for IPC with a GUI."
    )

    args = parser.parse_args()

    if args.json:
        start_repl_json(send_json_message)
    else:
        start_repl_interactive()


if __name__ == "__main__":
    main()
