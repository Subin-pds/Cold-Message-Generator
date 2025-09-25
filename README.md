# Cold Message Generator 📧

A Python-based application that generates personalized cold emails using job descriptions and relevant portfolio links.

## Description

This project uses AI and natural language processing to:
1. Parse job descriptions from URLs
2. Extract key requirements and skills
3. Match them with relevant portfolio examples
4. Generate customized cold emails highlighting matching expertise

## Project Structure

```
.
├── App/
│   ├── Resources/
│   │   └── AI_Skills_JobLinks.csv    # Portfolio links database
│   ├── vector_store/                 # ChromaDB vector storage
│   ├── main.py                       # Streamlit web application
│   ├── chains.py                     # LangChain processing chains
│   ├── portfolio.py                  # Portfolio matching logic
│   └── utils.py                      # Utility functions
├── Storage/                          # Persistent storage
└── *.ipynb                          # Jupyter notebooks for development
```

## Features

- Web scraping of job descriptions
- Vector similarity search for matching portfolio items
- LLM-powered email generation
- Streamlit web interface
- ChromaDB for efficient similarity search
- Integration with Groq LLM API

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up environment variables in `App/.env`
4. Run the Streamlit app:
```bash
cd App
streamlit run main.py
```

## Usage

1. Enter a job description URL in the web interface
2. Click "Generate Cold Email"
3. The application will:
   - Extract job requirements
   - Find matching portfolio examples
   - Generate a personalized email

## Technologies

- Python
- Streamlit
- LangChain
- ChromaDB
- Groq LLM
- Sentence Transformers
- BeautifulSoup
- Pandas

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files.