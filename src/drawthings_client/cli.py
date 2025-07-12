"""
drawthings command line interface
"""

import argparse
import json
import sys

from .lib.utils import save_image_and_config


def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        prog="drawthings",
        description="Draw Things app client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  drawthings config
  drawthings config model
  drawthings txt2img "a beautiful landscape"
  drawthings txt2img "a cat sitting on a table"
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.0.1")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # config サブコマンド
    config_parser = subparsers.add_parser(
        "config", help="Get configuration values from Draw Things app"
    )
    config_parser.add_argument(
        "key",
        nargs="?",
        help="Configuration key to retrieve (if not specified, shows all config)",
    )

    # txt2img サブコマンド
    txt2img_parser = subparsers.add_parser(
        "txt2img", help="Generate image from text using Draw Things app"
    )
    txt2img_parser.add_argument("prompt", help="Text prompt to generate image")

    return parser


def cmd_txt2img(args: argparse.Namespace) -> int:
    """txt2img コマンドの実行"""

    from drawthings_client.client import DrawThingsClient, Txt2ImgRequest

    try:
        client = DrawThingsClient()

        # Create txt2img request
        request = Txt2ImgRequest()
        request.prompt = args.prompt

        print(f"Generating image for prompt: {args.prompt}")
        print("Please wait...")

        # Generate image
        image, config = client.txt2img(request)

        # Save image with timestamp
        image_path, config_path = save_image_and_config(
            image, config, directory="output"
        )
        print(f"Image saved to: {image_path}")
        print(f"Config saved to: {config_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_config(args: argparse.Namespace) -> int:
    """
    Executes the config command to retrieve configuration values from the Draw Things app.
    """
    from drawthings_client.client import DrawThingsClient

    try:
        client = DrawThingsClient()
        config = client.get_config()

        if args.key:
            if args.key in config:
                value = config.get(args.key)
                print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
            else:
                print(f"Key '{args.key}' not found in configuration", file=sys.stderr)
                return 1
        else:
            # Display as JSON format
            print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "config":
            return cmd_config(args)
        elif args.command == "txt2img":
            return cmd_txt2img(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
