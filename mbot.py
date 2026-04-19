import streamlit as st
import os
from dotenv import load_dotenv

# --- MODERN 2026 IMPORTS ---
from langchain_classic.agents import AgentExecutor, create_openai_functions_agent
from langchain_classic import hub 
from langchain_core.tools import Tool
from langchain_core.messages import AIMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_unstructured import UnstructuredLoader # Modern 2026 Loader
from langchain_community.utilities import SerpAPIWrapper

# Load API Keys
load_dotenv()

# --- FE FUNDINFO BRANDING & VISIBILITY FIX ---
def apply_branding():
    st.markdown("""
        <style>
        /* Global Background */
        .stApp {
            background-color: #F4F7F9;
            font-family: 'Inter', sans-serif;
        }
        
        /* Sidebar: Mirage Navy Background */
        [data-testid="stSidebar"] {
            background-color: #19252F !important;
        }

        /* CRITICAL FIX: Make Sidebar Text White & Visible */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }

        /* Persian Green Primary Buttons */
        div.stButton > button:first-child {
            background-color: #00A499;
            color: white;
            border-radius: 4px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #685BC8; /* Transitions to Brand Purple */
            color: white;
            border: none;
        }

        /* Chat Message Bubbles */
        .stChatMessage {
            background-color: white;
            border: 1px solid #E1E8ED;
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        /* Main Header Accent */
        h1 {
            color: #19252F;
            border-left: 5px solid #00A499;
            padding-left: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="FE fundinfo | AI Assistant", layout="wide", page_icon="📈")
apply_branding()

# --- 1. DATA INGESTION (Optimized for Efficiency) ---
@st.cache_resource
def process_marketing_files(uploaded_files):
    all_docs = []
    # Using Recursive Splitter ensures the AI gets meaningful context chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    
    for uploaded_file in uploaded_files:
        temp_path = f"./temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Modern Loader: Handles multiple formats with high precision
        loader = UnstructuredLoader(file_path=temp_path, mode="elements")
        raw_elements = loader.load()
        
        chunks = text_splitter.split_documents(raw_elements)
        all_docs.extend(chunks)
        os.remove(temp_path) 
    
    vector_db = FAISS.from_documents(all_docs, OpenAIEmbeddings())
    return vector_db.as_retriever(search_kwargs={"k": 5})

# --- 2. SIDEBAR HUB ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00A499;'>FE fundinfo</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("📂 Knowledge Vault")
    uploaded_files = st.file_uploader("Upload Marketing Docs (PDF, Word, Email)", accept_multiple_files=True)
    if st.button("Index Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                st.session_state.retriever = process_marketing_files(uploaded_files)
                st.success("Vault Updated!")
        else:
            st.warning("Please upload files.")

# --- 3. AGENT TOOLS ---
search = SerpAPIWrapper()

def internal_doc_search(query: str):
    if "retriever" not in st.session_state:
        return "Internal vault is empty. Please upload documents."
    docs = st.session_state.retriever.invoke(query)
    return "\n\n".join([f"Source: {d.metadata.get('filename')}\nContent: {d.page_content}" for d in docs])

tools = [
    Tool(name="Internal_Knowledge", func=internal_doc_search, 
         description="Use for internal fund data, strategy, and brand documents."),
    Tool(name="Google_Search", func=search.run, 
         description="Use for external market trends and real-time news.")
]

# --- 4. REASONING ENGINE (FE Specialist Persona) ---
llm = ChatOpenAI(model="gpt-4o", temperature=0) 
prompt = hub.pull("hwchase17/openai-functions-agent")

# Injecting FE fundinfo Persona for better responses
prompt.messages[0].prompt.template = """You are the FE fundinfo Marketing Operations Agent. 
Prioritize Internal_Knowledge for company facts. Use Google_Search for market trends.
Be professional, accurate, and concise."""

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 5. CHAT UI ---
st.title("🤖 Agentic Marketing Assistant")
st.markdown("*Precision Intelligence for Fund Information*")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

if user_input := st.chat_input("Ex: Compare our Q4 strategy to current trends..."):
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        try:
            response = agent_executor.invoke({"input": user_input, "chat_history": st.session_state.chat_history})
            answer = response["output"]
            st.markdown(answer)
            st.session_state.chat_history.append(AIMessage(content=answer))
        except Exception as e:
            st.error(f"Reasoning Error: {str(e)}")
            st.write(internal_doc_search(user_input))