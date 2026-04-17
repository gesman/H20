#!/usr/bin/env python3
"""Format Claude Code stream-json output for human-readable terminal use."""

import json
import sys


class Colors:
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    CALM_YELLOW = "\033[38;5;186m"
    DIM_YELLOW = "\033[2;33m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def write(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def handle_stream_event(data: dict) -> None:
    event = data.get("event", {})
    event_type = event.get("type", "")

    if event_type == "message_start":
        model = event.get("message", {}).get("model", "claude")
        write(f"\n{Colors.CYAN}[assistant {model}]:{Colors.RESET} ")
        return

    if event_type == "content_block_start":
        block = event.get("content_block", {})
        block_type = block.get("type", "")
        if block_type == "tool_use":
            name = block.get("name", "")
            tool_id = block.get("id", "")
            write(
                f"\n{Colors.YELLOW}[tool call]{Colors.RESET} "
                f"{name} (id={tool_id})\n"
                f"    {Colors.DIM_YELLOW}[tool input]{Colors.RESET} "
            )
        elif block_type == "thinking":
            write(f"\n{Colors.DIM}[thinking]{Colors.RESET}\n")
        return

    if event_type == "content_block_delta":
        delta = event.get("delta", {})
        delta_type = delta.get("type", "")
        if delta_type == "text_delta":
            write(f"{Colors.CALM_YELLOW}{delta.get('text', '')}{Colors.RESET}")
        elif delta_type == "thinking_delta":
            write(f"{Colors.DIM}{delta.get('thinking', '')}{Colors.RESET}")
        elif delta_type == "input_json_delta":
            write(delta.get("partial_json", ""))
        return

    if event_type == "content_block_stop":
        write("\n")
        return

    if event_type == "error":
        error = event.get("error", {})
        msg = error.get("message") or error.get("type") or "unknown error"
        write(f"\n{Colors.RED}[error]{Colors.RESET} {msg}\n")


def handle_result(data: dict) -> None:
    cost = data.get("total_cost_usd", 0)
    usage = data.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    turns = data.get("num_turns", 0)
    write(
        f"\n\n{Colors.BOLD}[done]{Colors.RESET} "
        f"cost=${cost:.4f} input_tokens={input_tokens} "
        f"output_tokens={output_tokens} turns={turns}\n"
    )


def main() -> None:
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_type = data.get("type", "")
        if msg_type == "stream_event":
            handle_stream_event(data)
        elif msg_type == "result":
            handle_result(data)


if __name__ == "__main__":
    main()
