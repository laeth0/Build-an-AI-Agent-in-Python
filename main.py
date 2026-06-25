import os
import argparse
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


def generate_content(client, messages):
    for attempt in range(5):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    temperature=0,
                ),
            )
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and attempt < 4:
                time.sleep(45)
                continue
            raise


def main():
    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Please add it to your .env file.")

    client = genai.Client(api_key=api_key)

    messages: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    response = generate_content(client, messages)

    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata found in Gemini response.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()