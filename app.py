import streamlit as st
import os
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom prompt template for formatted database responses
SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct query to run, then look at the results of the query and return the answer.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.

IMPORTANT FORMATTING RULES:
1. Always format your final answer in a clear, readable way
2. Use bullet points or numbered lists when showing multiple items
3. Include column headers when showing tabular data
4. Round decimal numbers to 2 decimal places
5. Format dates in a readable format (YYYY-MM-DD)
6. If showing counts or statistics, include the actual numbers
7. Provide context for your answers (e.g., "Based on the data in the users table...")

Only use the following tools. Only use the information returned by the tools to construct your final answer.
Do not make up any information that is not found in the database.
Your response should be accurate and helpful to the user.

If the question does not seem related to the database, just return "I can only help with questions about the database."
"""

SQL_SUFFIX = """Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query. Then I should query the schema of the most relevant tables.
{agent_scratchpad}"""

def setup_database():
    """Setup PostgreSQL database connection"""
    db_user = os.getenv("DB_USER", "username")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "dbname")
    
    connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        db = SQLDatabase.from_uri(connection_string)
        return db, None
    except Exception as e:
        return None, str(e)

def setup_agent(db):
    """Setup LangChain agent with SQL toolkit"""
    try:
        llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        agent_executor = initialize_agent(
            tools=toolkit.get_tools(),
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent_executor, None
    except Exception as e:
        return None, str(e)

def query_database(agent, query):
    """Query the database using the agent"""
    try:
        response = agent.run(query)
        return response, None
    except Exception as e:
        error_msg = str(e)
        if "Could not parse LLM output" in error_msg:
            return "Sorry, I encountered a parsing error. Please try rephrasing your question or ask something simpler.", None
        elif "Agent stopped due to iteration limit" in error_msg:
            return "The query is taking longer than expected. Please try asking a simpler question or be more specific.", None
        elif "Agent stopped due to time limit" in error_msg:
            return "The query timed out. Please try asking a simpler question or be more specific.", None
        return None, error_msg

# Configure Streamlit page
st.set_page_config(
    page_title="PostgreSQL Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "db" not in st.session_state:
    st.session_state.db = None
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = False

def connect_to_database():
    """Connect to database and initialize agent"""
    with st.spinner("Connecting to database..."):
        db, db_error = setup_database()
        if db_error:
            st.error(f"Database connection failed: {db_error}")
            return False
        
        agent, agent_error = setup_agent(db)
        if agent_error:
            st.error(f"Agent initialization failed: {agent_error}")
            return False
        
        st.session_state.db = db
        st.session_state.agent = agent
        st.session_state.connected = True
        st.success("✅ Connected successfully!")
        return True

# Main UI
st.title("🤖 PostgreSQL Chatbot")
st.markdown("Ask questions about your PostgreSQL database in natural language!")

# Sidebar for connection status and settings
with st.sidebar:
    st.header("🔧 Connection")
    
    if not st.session_state.connected:
        st.warning("Not connected to database")
        if st.button("Connect to Database", type="primary"):
            connect_to_database()
    else:
        st.success("✅ Connected to database")
        if st.button("Disconnect"):
            st.session_state.db = None
            st.session_state.agent = None
            st.session_state.connected = False
            st.session_state.messages = []
            st.rerun()
    
    st.header("📊 Database Info")
    if st.session_state.connected and st.session_state.db:
        try:
            table_info = st.session_state.db.get_table_info()
            st.text_area("Tables Schema", table_info, height=200)
        except Exception as e:
            st.error(f"Error getting table info: {e}")
    
    st.header("🔑 Environment")
    st.info("Make sure your .env file contains:\n- DB_USER\n- DB_PASSWORD\n- DB_HOST\n- DB_PORT\n- DB_NAME\n- GROQ_API_KEY")

# Chat interface
if st.session_state.connected:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your database..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, error = query_database(st.session_state.agent, prompt)
                
                if error:
                    st.error(f"Error: {error}")
                    response = "Sorry, I encountered an error while processing your request."
                
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

else:
    st.info("👆 Please connect to your database using the sidebar to start chatting!")
    
    # Example queries
    st.header("💡 Example Questions")
    st.markdown("""
    Once connected, you can ask questions like:
    - "How many records are in the users table?"
    - "What are the top 5 products by sales?"
    - "Show me the latest orders from this week"
    - "What's the average age of users?"
    - "List all tables in the database"
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Groq Llama")
