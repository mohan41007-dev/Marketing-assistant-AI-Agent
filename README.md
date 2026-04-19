🤖 Agentic Marketing Operations Assistant
Internal Intelligence Platform for FE fundinfo
This is an Agentic AI Chatbot designed to streamline marketing operations by bridging the gap between internal brand strategy and external market trends. Unlike standard chatbots, this assistant uses Reasoning (ReAct logic) to decide whether to consult the internal Knowledge Vault or search the web via Google to provide the most accurate answer.

🌟 Key Features
Branded UI: Fully customized Streamlit interface using FE fundinfo brand guidelines (Persian Green & Mirage Navy).

Agentic Reasoning: Powered by GPT-4o and LangChain, the bot independently decides which tools to use based on the user's query.

Knowledge Vault (RAG): Upload and index PDFs, Word docs, and emails. The bot uses FAISS vector storage and Recursive Character Chunking for high-precision retrieval.

Live Market Intelligence: Integrated with SerpApi for real-time Google Search capabilities.

Memory-Aware: Maintains full conversation history to handle complex, multi-step marketing inquiries.

🛠️ Tech Stack
Framework: LangChain (Classic & Core 2026 modules)

LLM: OpenAI GPT-4o

Frontend: Streamlit (Custom CSS)

Vector Database: FAISS (Facebook AI Similarity Search)

Document Parsing: Unstructured.io

Search API: SerpApi

🚀 Getting Started
1. Prerequisites
Python 3.10+

OpenAI API Key

SerpApi Key

2. Installation
Clone the repository and install dependencies:

PowerShell
git clone https://github.com/your-username/mkchatbot.git
cd mkchatbot
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory and add your keys:

Plaintext
OPENAI_API_KEY=your_openai_key_here
SERPAPI_API_KEY=your_serpapi_key_here
4. Running the App
PowerShell
python -m streamlit run mbot.py
📂 Project Structure
mbot.py: The main application logic and UI.

.env: (Hidden) API credentials.

.gitignore: Prevents sensitive data and environment folders from being uploaded.

requirements.txt: List of all Python dependencies.

marketing_vault/: (Generated) Local vector database for uploaded documents.
