import sys
import asyncio
from src.config import Config
from src.client import OpenRouterClient
from src.services import ChatService
import itertools

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

            # print("Thinking... ", end="\r")

            loader_task = asyncio.create_task(show_loader())

            try:
                response = await service.ask(user_input)
            finally:
                loader_task.cancel()
                try:
                    await loader_task
                except asyncio.CancelledError:
                    pass


            print(f"\rBot: {response}")
            print_separator()

        except KeyboardInterrupt:
            print("\nBye bye!")
            break

        except Exception as e:
            print(f"Error: {e}")
            print_separator()

def print_separator():
    print("-" * 50)

async def show_loader(text: str = ""):
    """
    Async function for showing loader text
    """
    spinner = itertools.cycle(['|', '/', '-', '\\'])

    try:
        while True:
            sys.stdout.write(f"\r{text}{next(spinner)}")
            sys.stdout.flush()
            await asyncio.sleep(0.3)
    except asyncio.CancelledError:
        sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")
        sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())