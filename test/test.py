#!/usr/bin/env python3
"""Test script that makes requests to all models with both API formats."""

import argparse
import sys

from request_chat_completion_api import make_request as make_chat_request
from request_message_api import make_request as make_message_request

# Global array of (model_name, message, system_prompt) triplets
TEST_CASES = [
    ("claude-opus-4-5",    "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the claude-opus-4-5 model. Your answer are as short as possible."),
    ("claude-sonnet-4-5",  "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the claude-sonnet-4-5 model. Your answer are as short as possible."),
    ("claude-haiku-4-5",   "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the claude-haiku-4-5 model. Your answer are as short as possible."),
    ("gpt-5.1-codex",      "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the gpt-5.1-codex model. Your answer are as short as possible."),
    ("gpt-5.1-codex-mini", "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the gpt-5.1-codex-mini model. Your answer are as short as possible."),
    ("cld-o45",            "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the cld-o45 model. Your answer are as short as possible."),
    ("cld-s45",            "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the cld-s45 model. Your answer are as short as possible."),
    ("cld-h45",            "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the cld-h45 model. Your answer are as short as possible."),
    ("g51-cdx",            "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the g51-cdx model. Your answer are as short as possible."),
    ("g51-cdx-mini",       "Hello, what model do you test? which api format?", "You are AI Chat made to test llm-proxy-logger project for the g51-cdx-mini model. Your answer are as short as possible."),
]


def main():
    parser = argparse.ArgumentParser(description="Test all models with both API formats")
    parser.add_argument("--url", type=str, required=True, help="Base URL (e.g., http://localhost:4000)")
    parser.add_argument("--provider-key", action="store_true", help="Use provider-specific API keys (ANTHROPIC_API_KEY for Message API, OPENAI_API_KEY for Chat Completion API)")
    
    args = parser.parse_args()
    
    results = []
    
    # Test each model with both API formats
    for model_name, message, system_prompt in TEST_CASES:
        # Test with Anthropic Message API format
        print(f"Testing {model_name} (Message API)...", end=" ", flush=True)
        try:
            response = make_message_request(args.url, model_name, message, args.provider_key, system_prompt + "You respond to the Message API format.")
            print("✓")
            results.append((model_name, "Message API", True, response[:50] if len(response) > 50 else response))
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append((model_name, "Message API", False, str(e)))
        
        # Test with OpenAI Chat Completion API format
        print(f"Testing {model_name} (Chat Completion API)...", end=" ", flush=True)
        try:
            response = make_chat_request(args.url, model_name, message, args.provider_key, system_prompt + "You respond to the Chat Completion API format.")
            print("✓")
            results.append((model_name, "Chat Completion API", True, response[:50] if len(response) > 50 else response))
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append((model_name, "Chat Completion API", False, str(e)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    for model_name, api_format, success, result in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} {model_name} ({api_format})")
        if not success:
            print(f"  Error: {result}")
    
    # Exit with error code if any tests failed
    failed_count = sum(1 for _, _, success, _ in results if not success)
    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

