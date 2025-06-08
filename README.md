# ChatDB - Natural Language PostgreSQL Interface

A powerful chatbot application that allows you to interact with PostgreSQL databases using natural language queries. Built with LangChain, Groq Llama, and Streamlit for an intuitive web-based experience.

## 🚀 Features

- 🌐 **Modern Web Interface**: Clean, responsive Streamlit-based UI
- 💬 **Natural Language Queries**: Ask questions in plain English
- 📊 **Database Schema Viewer**: Explore your database structure
- 🔄 **Real-time Connection Status**: Live connection monitoring
- 🗑️ **Chat History Management**: Clear and manage conversation history
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🤖 **AI-Powered**: Leverages Groq's Llama model for intelligent responses
- 🔒 **Secure**: Environment-based configuration for credentials

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database (local or remote)
- Groq API key ([Get one here](https://console.groq.com/))

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/anmolpansara/ChatWithDB.git
cd ChatDB
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project root with the following variables:
```env
# Database Configuration
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Usage

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Getting Started
1. Launch the application
2. Click "Connect to Database" in the sidebar
3. Once connected, start asking questions about your database
4. View database schema in the sidebar for reference

## 💡 Example Queries

Try these natural language questions with your database:

**Data Exploration:**
- "How many records are in the users table?"
- "What tables are available in the database?"
- "Show me the structure of the orders table"

**Analytics:**
- "What are the top 5 products by sales?"
- "Show me the latest orders from this week"
- "What's the average age of users?"
- "How many orders were placed last month?"

**Business Intelligence:**
- "Which customers have spent the most money?"
- "What's the total revenue by product category?"
- "Show me users who haven't placed any orders"

## 🔧 Configuration

### Database Connection
The application supports PostgreSQL databases. Update your `.env` file with:
- Local database: Use `localhost` as DB_HOST
- Remote database: Use your server's IP or domain name
- Cloud database: Use the provided connection details from your cloud provider

### Groq API Setup
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file as `GROQ_API_KEY`

## 📁 Project Structure

```
ChatDB/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md          # Project documentation
└── .gitignore         # Git ignore file (recommended)
```

## 🔍 Troubleshooting

**Connection Issues:**
- Verify your PostgreSQL server is running
- Check database credentials in `.env` file
- Ensure the database is accessible from your network

**API Errors:**
- Verify your Groq API key is valid
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**Query Errors:**
- Try simpler, more specific questions
- Check that the referenced tables/columns exist
- Review the database schema in the sidebar
