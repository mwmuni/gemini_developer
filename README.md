# Gemini Agent

This repository contains a Python implementation of a Gemini Agent for interacting with the Gemini API. This agent is designed to be used with Google's Gemini Pro model and allows for interactive conversations, code execution, and file operations.

## Files

- `ask_gemini.py`: This module provides a Python interface for interacting with the Gemini Pro model through Google Vertex AI. It handles authentication, request construction, response parsing, and maintains chat history.
- `gemini_agent.py`: This module implements the Gemini Agent that uses the `ask_gemini.py` module to communicate with the Gemini Pro model. It allows users to send queries, execute code (bash and Python), and receive responses in an interactive loop.

## Features

- **Interactive Conversations:** Engage in natural language conversations with the Gemini Pro model.
- **Code Execution:** Execute bash and Python code snippets provided by the model.
- **File Operations:** Perform basic file operations based on the model's instructions.
- **Contextual Understanding:** The agent maintains chat history, allowing the model to understand and respond to queries within the context of the conversation.

## Installation

1. Install Python 3.7 or higher.
2. Install the required packages: vertexai, json

```bash
pip install -r requirements.txt
```

3. Set up Google Cloud Platform project and enable Vertex AI API.
4. Authenticate your Google Cloud account.

## Usage

1. Run the `gemini_agent.py` script:

```bash
python gemini_agent.py
```

2. Start interacting with the agent by typing your queries in the console.
3. Agent outputs with blocks of type `bash` and `python` are captured and exectuted or saved.

## Examples

**Interactive Conversation:**

```
You: What is the capital of France?
Agent: Paris
```

**Code Execution:**

```
You: Create a Python script that prints "Hello, world!"
```
Agent:
```
      ```python
      # hello.py
      print("Hello, world!")
      ```
```

This will create a python file called `hello.py`

Agent:
```
      ```bash
      hatch run python hello.py
      ```
```

**File Operations:**

```
You: Create a new directory named "documents"
```
Agent:
```
      ```bash
      mkdir documents
      ```
```


## Notes

- The agent is designed to work with Google's Gemini Pro model and requires a valid API key and Google Cloud Platform project.
- Ensure that your Google Cloud account has the necessary permissions to access Vertex AI API.
- The agent's capabilities are limited to the functionalities provided by the Gemini Pro model and the code within the scripts.

## License

This project is licensed under the MIT License.
