# LLM Chat CLI

## Prerequisites
* Python 3.11+
* OpenRouter API Key

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   
   .venv\Scripts\activate
   
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory:
   ```bash
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
   ```
## Usage
Run the application
  ```bash
  python -m src.main
  ```
## Testing
Run unit tests
  ```bash
pytest
```
