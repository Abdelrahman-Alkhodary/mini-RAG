# mini-rag

This is a minimal implementation for the RAG application for question answering

## Requirements

- Python 3.8 or later

## Installation

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Setup the environements variables
```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file such as `OPENAI_API_KEY` value.


## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```