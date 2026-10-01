"""Command-line entry point for quick local smoke tests."""

from __future__ import annotations

import argparse
import json

from .controller import SmartHomeController


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart-home natural-language control simulator")
    parser.add_argument("text", nargs="+", help="Chinese natural-language command")
    parser.add_argument("--confirm", action="store_true", help="confirm high-risk actions")
    parser.add_argument("--llm", action="store_true", help="enable optional LLM fallback from env")
    args = parser.parse_args()
    controller = SmartHomeController(enable_llm_from_env=args.llm)
    decision = controller.process(" ".join(args.text), confirmed=args.confirm)
    print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
