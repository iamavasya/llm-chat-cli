import sys
import asyncio
from src.config import Config
from src.client import OpenRouterClient
from src.services import ChatService

def print_separator():
    print("-" * 50)

async def main():
    print_separator()
    print("Welcome to Python LLM CLI Chat // Made by iamavasya (Rostyslav Mukha)")
    print("Initializing...")

    try:
        config = Config.load()
    except ValueError as e:
        print(f"Config error: {e}")
        return
    client = OpenRouterClient(api_key=config.api_key, model=config.model)
    service = ChatService(client=client)

    print(f"Ready! Model: {config.model}")
    print("Type 'bye' to exit.")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["bye", "exit", "quit"]:
                print("Bye bye!")
                break

            print("Thinking... ", end="\r")
            response = await service.ask(user_input)
            print(f"\rBot: {response}")
            print_separator()

        except KeyboardInterrupt:
            print("\nBye bye!")
            break

        except Exception as e:
            print(f"Error: {e}")
            print_separator()

if __name__ == "__main__":
    asyncio.run(main())