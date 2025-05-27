import uuid
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


def collect_user_preferences():
    """Collect user preferences interactively"""
    print("🤖 Personal AI Assistant Setup")
    print("Let's get to know you better! Please answer a few questions:\n")

    name = input("What's your name? ").strip()
    if not name:
        name = "User"

    print(f"\nNice to meet you, {name}! 👋\n")

    print("Tell me about your interests and preferences:")

    hobbies = input("What are your favorite hobbies or activities? ").strip()
    food = input("What's your favorite type of food? ").strip()
    entertainment = input("What's your favorite TV show, movie, or book? ").strip()
    other = input("Anything else you'd like me to remember about you? ").strip()

    preferences_parts = []
    if hobbies:
        preferences_parts.append(f"Hobbies/Activities: {hobbies}")
    if food:
        preferences_parts.append(f"Favorite food: {food}")
    if entertainment:
        preferences_parts.append(f"Favorite entertainment: {entertainment}")
    if other:
        preferences_parts.append(f"Other: {other}")

    preferences = "\n".join(preferences_parts) if preferences_parts else "No specific preferences provided."

    return name, preferences


def main():
    print("=" * 50)
    print("🤖 Personal AI Assistant Terminal Chat")
    print("=" * 50)

    # Collect user preferences first
    user_name, user_preferences = collect_user_preferences()

    print(f"\n✅ Great! I'll remember your preferences, {user_name}.")
    print("Now let's start chatting! Type 'quit' or 'exit' to stop.\n")

    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": user_name,
        "user_preferences": user_preferences,
    }

    APP_NAME = "Personal AI Assistant"
    USER_ID = user_name.lower().replace(" ", "_")
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
                print(f"\r🤖 AI Assistant: {agent_response}")
            else:
                print("\r🤖 AI Assistant: Sorry, I couldn't process that message.")

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
