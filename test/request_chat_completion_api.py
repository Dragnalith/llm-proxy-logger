#!/usr/bin/env python3
"""Minimal script to make requests to OpenAI Chat Completion API."""

import argparse
import json
import os
import sys

import requests


def make_request(url: str, model: str, message: str, use_provider_key: bool = False, system: str = "You are AI Chat made to test llm-proxy-logger project. Your answer are as short as possible") -> str:
    """
    Make a request to OpenAI Chat Completion API.
    
    Args:
        url: Base URL (e.g., http://localhost:4000)
        model: Model slug
        message: User message
        use_provider_key: If True, use OPENAI_API_KEY; otherwise use LITELLM_MASTER_KEY
        system: System prompt (default: "You are AI Chat made to test llm-proxy-logger project. Your answer are as short as possible")
    
    Returns:
        Response text from the API
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If API key is not found
    """
    if use_provider_key:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Set OPENAI_API_KEY")
    else:
        api_key = os.environ.get("LITELLM_MASTER_KEY")
        if not api_key:
            raise ValueError("API key not found. Set LITELLM_MASTER_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json"
    }
    
    # Build full URL by appending endpoint
    base_url = url.rstrip("/")
    full_url = f"{base_url}/v1/chat/completions"
    
    payload = {
        "model": model,
        "max_tokens": 64,
        "temperature": 1,
        "messages": [
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    response = requests.post(full_url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    
    # Extract text from OpenAI response
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        return json.dumps(result, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Make request to OpenAI Chat Completion API")
    parser.add_argument("--model", type=str, required=True, help="Model slug")
    parser.add_argument("--url", type=str, required=True, help="Base URL (e.g., http://localhost:4000)")
    parser.add_argument("--provider-key", action="store_true", help="Use OPENAI_API_KEY instead of LITELLM_MASTER_KEY")
    parser.add_argument("--system", type=str, default="You are AI Chat made to test llm-proxy-logger project. Your answer are as short as possible", help="System prompt")
    parser.add_argument("message", type=str, help="User message")
    
    args = parser.parse_args()
    
    try:
        result = make_request(args.url, args.model, args.message, args.provider_key, args.system)
        print(result)
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

