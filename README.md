
# RAG Based Log Analyzer

A Streamlit web application for analyzing log files using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs). The app leverages MongoDB Atlas for vector storage and semantic search, and integrates with Ollama for LLM-powered responses.

## Features
- Upload and analyze log files (CSV format)
- Semantic search over logs using vector embeddings
- Natural language question answering about your logs
- Interactive Streamlit UI

## Architecture Overview

```
Log Files (CSV) → Data Loader (load/data_pipeline.py, load.sh) → MongoDB Atlas (Vector Store)
                                                        ↑
Streamlit UI (main.py) → Log Analyzer (analyzer/log_analyzer.py) → Retriever (analyzer/retriever.py) → Ollama LLM
```

## Folder Structure

```
log-analyzer/
├── main.py                  # Streamlit app entry point
├── analyzer/
│   ├── __init__.py
│   ├── log_analyzer.py      # Business logic
│   └── retriever.py         # Vector DB and LLM integration
├── load/
│   ├── data_pipeline.py     # Data loading scripts
│   └── load.sh              # Data loading shell script
├── store/
│   ├── backup/              # Example log CSVs
│   └── logs/                # Example log CSVs
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Set the following environment variables (e.g., in your shell or a `.env` file):

- `MONGODB_URL` — MongoDB Atlas connection string
- `MONGODB_DBNAME` — MongoDB database name

Example:
```bash
export MONGODB_URL="mongodb+srv://<user>:<password>@cluster.mongodb.net"
export MONGODB_DBNAME="logdb"
```

### 3. Load Log Data

Place your log CSV files in `store/backup/` or `store/logs/`.

Run the data pipeline to ingest and vectorize logs:

```bash
cd load
bash load.sh
```

### 4. Start Ollama LLM Server

```bash
ollama pull llama2
ollama run llama2
```

Make sure Ollama is running and accessible at `http://localhost:11434`.

### 5. Run the Streamlit App

From the project root:

```bash
streamlit run main.py
```

## Usage
- Enter your question about the logs in the text area.
- Click **Analyze** to get a semantic, LLM-powered answer based on your log data.

## Troubleshooting
- Ensure MongoDB Atlas and Ollama are running and accessible.
- Check that environment variables are set correctly.
- If you see import errors, run the app from the project root directory.

## License
MIT License

---

**Enjoy analyzing your logs with AI!**
