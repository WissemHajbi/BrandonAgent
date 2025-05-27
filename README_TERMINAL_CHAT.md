# 🤖 Brandon Bot Terminal Chat

A simple terminal-based chatbot that maintains conversation state and remembers user preferences. Built with Google's Agent Development Kit (ADK) and Gemini AI.

## 🚀 Features

- **Stateful Conversations**: Remembers your preferences across the chat session
- **Terminal Interface**: Simple command-line chat experience
- **Auto-Retry Logic**: Handles API overload with automatic retries
- **Graceful Error Handling**: User-friendly error messages
- **Easy Exit**: Type `quit`, `exit`, or `q` to stop

## 📋 Prerequisites

- Python 3.8 or higher
- Google AI API key (Gemini)

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install google-adk python-dotenv
```

### 2. Environment Setup

Create a `.env` file in the `5-sessions-and-state` directory:

```env
# .env file
GOOGLE_API_KEY=your_google_api_key_here
```

**How to get your Google API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" 
4. Create a new API key
5. Copy the key and paste it in your `.env` file

### 3. Project Structure

```
5-sessions-and-state/
├── terminal_chat.py              # Main terminal chat application
├── basic_stateful_session.py     # Original example
├── question_answering_agent/     # Agent configuration
│   ├── __init__.py
│   └── agent.py                  # Agent definition
├── .env                          # Your API keys (create this)
└── README_TERMINAL_CHAT.md       # This file
```

## 🏃‍♂️ Running the Chat

1. **Navigate to the directory:**
   ```bash
   cd 5-sessions-and-state
   ```

2. **Run the terminal chat:**
   ```bash
   python terminal_chat.py
   ```

3. **Start chatting:**
   ```
   🤖 Brandon Bot Terminal Chat
   Type your messages and press Enter. Type 'quit' or 'exit' to stop.

   ✅ Session created: a45ad5e9...

   You: What are my favorite activities?
   🤖 Thinking...
   🤖 Brandon Bot: Based on your preferences, you enjoy playing Pickleball, Disc Golf, and Tennis!

   You: quit
   👋 Goodbye!
   ```

## 🎯 What the Bot Knows

The bot comes pre-configured with Brandon's preferences:
- **Name**: Brandon Hancock
- **Sports**: Pickleball, Disc Golf, Tennis
- **Favorite Food**: Mexican
- **Favorite TV Show**: Game of Thrones
- **Special Interest**: Loves YouTube likes and subscriptions

## 🔧 Customization

To customize the bot for yourself, edit the `initial_state` in `terminal_chat.py`:

```python
initial_state = {
    "user_name": "Your Name",
    "user_preferences": """
        Your hobbies and interests here.
        Your favorite food.
        Your favorite shows/movies.
        Any other preferences.
    """,
}
```

## 🚨 Troubleshooting

### "Model Overloaded" Error
- **What it means**: Google's servers are busy
- **Solution**: The bot automatically retries with delays
- **If it persists**: Wait a few minutes and try again

### "Authentication Error"
- **Check**: Your `GOOGLE_API_KEY` in the `.env` file
- **Verify**: The API key is valid and active

### Import Errors
- **Install dependencies**: `pip install google-adk python-dotenv`
- **Check Python version**: Must be 3.8+

## 🎓 Learning Points

This project demonstrates:
- **Stateful AI Conversations**: How to maintain context across messages
- **Error Handling**: Graceful handling of API failures
- **Retry Logic**: Automatic retry with exponential backoff
- **Terminal UI**: Simple command-line interface design
- **Environment Configuration**: Secure API key management

## 📝 Next Steps

Want to extend this project? Try:
- Adding more complex state management
- Implementing conversation history
- Adding file upload capabilities
- Creating a web interface
- Adding voice input/output

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with different agent configurations
- Add new features
- Improve error handling
- Share your modifications

---

**Happy Chatting! 🎉**
