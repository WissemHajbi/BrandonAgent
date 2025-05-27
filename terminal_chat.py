import uuid
import sys
import io
import time

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()


def send_message_with_retry(runner, user_id, session_id, message, max_retries=3):
    """Send message with automatic retry for 503 errors"""
    for attempt in range(max_retries):
        try:
            agent_response = ""
            for event in runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=message,
            ):
                if (event.content and
                    event.content.parts and
                    hasattr(event.content.parts[0], 'text') and
                    event.content.parts[0].text):
                    agent_response = event.content.parts[0].text.strip()
            return agent_response

        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  
                    print(f"⏳ Model busy, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "ERROR_503"
            else:
                return f"ERROR: {error_msg}"

    return "ERROR_MAX_RETRIES"


def main():
    print("🤖 Brandon Bot Terminal Chat")
    print("Type your messages and press Enter. Type 'quit' or 'exit' to stop.\n")

    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Brandon Hancock",
        "user_preferences": """
            I like to play Pickleball, Disc Golf, and Tennis.
            My favorite food is Mexican.
            My favorite TV show is Game of Thrones.
            Loves it when people like and subscribe to his YouTube channel.
        """,
    }

    APP_NAME = "Brandon Bot"
    USER_ID = "brandon_hancock"
    SESSION_ID = str(uuid.uuid4())
    session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )

    print(f"✅ Session created: {SESSION_ID[:8]}...\n")

    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            new_message = types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )

            print("🤖 Thinking...")
            agent_response = send_message_with_retry(runner, USER_ID, SESSION_ID, new_message)

            if agent_response.startswith("ERROR_503"):
                print("\r⏳ The AI model is currently overloaded. Please try again later.")
            elif agent_response.startswith("ERROR:"):
                print(f"\r❌ {agent_response}")
            elif agent_response:
                print(f"\r🤖 Brandon Bot: {agent_response}")
            else:
                print("\r🤖 Brandon Bot: Sorry, I couldn't process that message.")

            print()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                print("⏳ The AI model is currently busy. Please try again in a moment.")
            else:
                print(f"❌ Error: {error_msg}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
