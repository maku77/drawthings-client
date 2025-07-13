"""
drawthings command line interface
"""

import argparse
import json
import sys

from drawthings_client.client import DrawThingsClient, Txt2ImgParams

from .lib.file_utils import FilePathGenerator


def create_parser() -> argparse.ArgumentParser:
    """
    Create command line argument parser for Draw Things CLI
    """
    from . import __version__

    parser = argparse.ArgumentParser(
        prog="drawthings",
        description="Draw Things app client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  drawthings config
  drawthings config model
  drawthings txt2img "a beautiful landscape"
  drawthings txt2img "a cat sitting on a table" -d ~/images
  drawthings txt2img "sunset over mountains" --dir ./output
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand for getting configuration
    config_parser = subparsers.add_parser(
        "config", help="Get configuration values from Draw Things app"
    )
    config_parser.add_argument(
        "key",
        nargs="?",
        help="Configuration key to retrieve (if not specified, shows all config)",
    )

    # Subcommand for generating images from text
    txt2img_parser = subparsers.add_parser(
        "txt2img", help="Generate image from text using Draw Things app"
    )
    txt2img_parser.add_argument("prompt", help="Text prompt to generate image")
    txt2img_parser.add_argument(
        "-d", "--dir",
        default="output",
        help="Output directory for generated images (default: output)"
    )

    return parser


def cmd_txt2img(args: argparse.Namespace) -> int:
    """
    Executes the txt2img command to generate images from text using the Draw Things app."""

    try:
        client = DrawThingsClient()

        # Create txt2img request
        request = Txt2ImgParams(prompt=args.prompt)

        print(f"Generating image with parameters: {request.to_json()}")
        print("Please wait...")

        path_gen = FilePathGenerator(args.dir)
        image_count = 0
        for image, config in client.txt2img(request):
            image_count += 1

            image_path = path_gen.create_image_path(image_count)
            image.save(image_path)
            print(f"Image saved to: {image_path}")

            config_path = path_gen.create_config_path(image_count)
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False, sort_keys=True)
            print(f"Configuration saved to: {config_path}")

        if image_count == 0:
            print("No images were generated")
            return 1

        print(f"\nGenerated {image_count} image(s)")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_config(args: argparse.Namespace) -> int:
    """
    Executes the config command to retrieve configuration values from the Draw Things app.
    """

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
