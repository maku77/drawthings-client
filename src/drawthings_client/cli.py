"""
drawthings command line interface
"""

import argparse
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
    if args.key:
        print(f"Getting configuration value for: {args.key}")
        # TODO: 実際のDraw Things APIから指定された設定値を取得
        print("⚠️  Draw Things API integration not yet implemented")
        return 0

    # キーが指定されていない場合は全設定を表示
    print("Current Draw Things configuration:")
    # TODO: 実際のDraw Things APIから全設定を取得
    sample_config = {
        "model": "stable-diffusion-xl",
        "width": 1024,
        "height": 1024,
        "steps": 20,
        "guidance_scale": 7.5,
        "sampler": "DPM++ 2M",
        "scheduler": "Karras",
        "seed": -1,
        "batch_size": 1,
        "safety_checker": True,
    }

    for key, value in sample_config.items():
        print(f"  {key}: {value}")

    print("\n⚠️  Draw Things API integration not yet implemented")
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
