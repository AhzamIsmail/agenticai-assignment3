# file: main.py
"""
Interactive demo for HotelAssistant using SimpleAgent.
"""

from hotel_assistant import HotelAssistant, SimpleAgent

def main():
    assistant = HotelAssistant(agent_cls=SimpleAgent)

    print("=== Hotel Assistant ===")
    while True:
        hotel_name = input("Enter hotel name (or 'quit' to exit): ").strip()
        if hotel_name.lower() == "quit":
            break

        question = input("Your question: ").strip()
        if not question:
            print("Please enter a question.")
            continue

        response = assistant.query(question, hotel_name=hotel_name)
        print("Assistant:", response)
        print("-" * 40)


if __name__ == "__main__":
    main()
