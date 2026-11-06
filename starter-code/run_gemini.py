"""Chat with Gemini in the terminal, or pass a prompt for one response."""

import argparse
import os

from template import GEMINI_MODEL, call_gemini, streaming_chatbot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="Câu hỏi một lần; bỏ trống để mở chatbot.")
    parser.add_argument("--model", default=GEMINI_MODEL, help="Model cho chế độ một câu hỏi.")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Giới hạn token cho chế độ một câu hỏi.")
    args = parser.parse_args()

    if not os.getenv("GEMINI_API_KEY"):
        parser.exit(1, "Chưa có GEMINI_API_KEY. Hãy thêm key vào file .env ở thư mục gốc.\n")

    if args.prompt is None:
        if args.model != GEMINI_MODEL or args.max_tokens != 1024:
            parser.error("--model và --max-tokens chỉ dùng khi truyền một câu hỏi.")
        print("=== Chatbot Gemini ===")
        print("Nhập tin nhắn rồi nhấn Enter. Gõ /clear để xóa lịch sử; exit hoặc quit để thoát.")
        try:
            streaming_chatbot()
        except KeyboardInterrupt:
            print()
        print("Tạm biệt!")
        return

    text, latency, usage = call_gemini(
        args.prompt, model=args.model, max_tokens=args.max_tokens
    )
    print(text)
    print(f"\nLatency: {latency:.2f}s")
    print(f"Tokens: {usage['input_tokens']} in / {usage['output_tokens']} out")


if __name__ == "__main__":
    main()
