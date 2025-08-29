# PropWise - “Turning Real Estate Data into Smart Decisions.”

## 📖 Overview
The **PropWise (Real Estate Research Assistant)** is an end-to-end **Retrieval-Augmented Generation (RAG) application** designed to help real estate analysts extract insights quickly from online news sources such as **CNBC, CBRE Ireland, realtor.com, and other real estate media platforms**.  

Instead of manually reading through multiple articles, analysts can input URLs of relevant news sources along with their query, and the system will return precise answers with **citations to original sources**. This saves time, ensures credibility, and improves the decision-making process.


## 🚀 Problem Statement
Real estate analysts often spend **hours combing through long news articles** to extract relevant information.  
The challenge is not just finding articles, but **deriving context-specific insights quickly** and verifying them with sources.  

The **Real Estate Research Assistant** solves this by:
- Accepting article URLs as input.  
- Analyzing and retrieving relevant sections.  
- Using an LLM to generate concise answers.  
- Providing **source citations** for trust and transparency.  


## 🎯 Purpose
The main purpose of this tool is to:
- **Respond to user queries** based on the content of real estate news articles.  
- **Provide verified answers with citations** to ensure credibility.  
- Enable analysts to make **faster, data-backed decisions** in the real estate market.  

## ⚙️ Features
- 📥 Input multiple news article URLs.  
- ❓ Ask custom domain-specific questions.  
- 🤖 RAG-powered answer generation.  
- 📌 Citations with links to original sources.  
- 💻 User-friendly interface for analysts and researchers.  

## 🛠️ Tech Stack
- **Backend**: Python, LangChain  
- **LLM**:  Groq (llama-3.3-70b-versatile) (via Hugging Face API)  
- **Embedding Model**: Sentence Transformers (sentence-transformers/all-MiniLM-L6-v2) 
- **Database (Vector Store)**: Chroma DB  
- **Frontend**: Streamlit (interactive interface)  
- **Scraping & Parsing**: PlaywrightURLLoader 
- **Deployment**: Docker + Streamlit Cloud  

## 📊 Workflow
1. **User Input**: Analyst provides one or more article URLs + a query.  
2. **Data Extraction**: Articles are scraped and cleaned.  
3. **Embedding & Retrieval**: Relevant chunks are stored/retrieved from a vector database.  
4. **RAG Pipeline**: Query + retrieved content passed to the LLM.  
5. **Response Generation**: The model generates an answer.  
6. **Citation Linking**: Citations are included with each answer.  


## 🖥️ Example Usage
```python
Input:
- URL: "https://irishrealestate.news/over-1000-dublin-homes-on-way-in-odevaney-gardens-redevelopment/
- Question: "How many new homes are planned for the O’Devaney Gardens redevelopment?"

Output:
"Over 1000 new homes are planned for the O'Devaney Gardens redevelopment in Dublin. Specifically, Phase 1 will deliver 379 A-rated social, affordable, and cost rental homes."
[Source: irishrealestate.news]"
```

## Installation

```
# Clone repo
git clone https://github.com/Aadarsh4u-code/PropWise
cd PropWise

# Create virtual environment
python10.3 -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows

# Install requirements
pip install -r requirements.txt
```

## Running the App
```streamlit run app.py```

## 🧪 Future Enhancements

1. Add multi-source aggregation (compare across multiple news sites).
1. Build trend analysis dashboard for visual insights.
1. Support speech-to-text queries for faster interactions.
1. Integrate with financial data APIs for richer context.
