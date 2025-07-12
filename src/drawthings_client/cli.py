"""
drawthings command line interface
"""

import argparse
import json
import sys
from typing import List, Optional


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

    return parser


def cmd_config(args: argparse.Namespace) -> int:
    """設定値取得コマンドの実行"""
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


def main(argv: Optional[List[str]] = None) -> int:
    """メイン関数"""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "config":
            return cmd_config(args)
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
