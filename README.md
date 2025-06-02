# 💸 Personal UPI Usage and Financial Analyzer using LLMs

A smart, AI-powered personal finance assistant that extracts and analyzes UPI transaction statements from popular apps like Paytm, GPay, and PhonePe, offering personalized insights and budgeting suggestions — all through a clean and interactive **Streamlit** dashboard.

---

## 🚀 Project Overview

This project leverages **PDF parsing**, **data analysis**, and **Large Language Models (LLMs)** to help users better understand and manage their digital payments and financial habits. It simplifies UPI transaction histories and delivers actionable insights such as:

- Spending patterns  
- Category-wise expenses  
- Unnecessary transactions  
- Personalized saving tips  

---

## 🧠 Skills You’ll Gain

- 📄 PDF Data Extraction and Parsing  
- 🧹 Data Cleaning and Structuring using Pandas  
- 🤖 LLM Integration using OpenAI (via API)  
- 📊 Financial Data Analysis and Pattern Recognition  
- 🌐 Deployment using **Streamlit**  
- 💡 Prompt Engineering for Recommendation Systems  

---

## 🏦 Domain

**FinTech / Personal Finance Automation**

---

## 🧩 Problem Statement

Build an AI-powered application that:
- Extracts and structures UPI transaction data from various PDF formats (Paytm, PhonePe, GPay, etc.)
- Analyzes financial behavior (e.g., total monthly expenses, frequent merchants)
- Detects wasteful spending
- Provides personalized financial advice and savings strategies

---

## 💼 Business Use Cases

- **Personal Finance Management**: Empower users to track their digital spending habits  
- **Spending Habit Detection**: Spot frequent categories and merchants  
- **Budgeting Assistant**: Generate smart saving suggestions  
- **Unified View**: Combine UPI data from multiple platforms into one report  

---

## ⚙️ Project Workflow

### 1. 🗂️ Dataset Preparation
- **Input**: UPI transaction PDFs from apps like Paytm, PhonePe, and GPay  
- **Output**: Cleaned and structured CSV or JSON files with fields:
  - Date, Time, Amount, Receiver, Description, Category

### 2. 🔍 Text Parsing & Preprocessing
- Tools Used: `PyMuPDF`, `pdfplumber`  
- Normalize and format raw text into usable tabular data using `pandas`

### 3. 📈 Data Analysis
- Identify:
  - Monthly and weekly spending trends  
  - Category-wise summaries  
  - Top merchants and transaction categories  
  - Potentially wasteful transactions  

### 4. 🧠 LLM-based Recommendations
- Using **OpenAI GPT model** for:
  - Budgeting tips  
  - Expense reduction advice  
  - Financial health summaries  

### 5. 📊 Deployment
- **Streamlit-based web app**  
- Simple, responsive UI with insights, charts, and LLM-powered advice  
- Can be deployed on platforms like Streamlit Community Cloud  
