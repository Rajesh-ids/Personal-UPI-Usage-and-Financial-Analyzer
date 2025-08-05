import os
import time
import random
import textwrap
import streamlit as st
import PyPDF2
import google.generativeai as genai


# Set up Google Gemini API Key
GEMINI_API_KEY = "Enter Your API key"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI setup
st.set_page_config(page_title="AI Personal Finance Assistant", page_icon="🤖", layout="wide")


# Add background image CSS
background_url = "https://cdn.prod.website-files.com/5eb185b0c64d8e1e73a9eec8/64e62bd9e412c90c2bc7eb05_website-image%20(3).png"
page_bg_img = f"""
<style>
.stApp {{
    position: relative;
    background-image: url("{background_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Add a semi-transparent overlay */
.stApp::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.8);  /* black with 40% opacity */
    z-index: 0;
}}

.stApp > * {{
    position: relative;
    z-index: 1;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Main title
st.markdown('''
<style>
@keyframes glow {
    0% { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000; }
    20% { text-shadow: 0 0 10px #ff8c00, 0 0 20px #ff8c00, 0 0 30px #ff8c00; }
    40% { text-shadow: 0 0 10px #ffd700, 0 0 20px #ffd700, 0 0 30px #ffd700; }
    60% { text-shadow: 0 0 10px #32cd32, 0 0 20px #32cd32, 0 0 30px #32cd32; }
    80% { text-shadow: 0 0 10px #1e90ff, 0 0 20px #1e90ff, 0 0 30px #1e90ff; }
    100% { text-shadow: 0 0 10px #8a2be2, 0 0 20px #8a2be2, 0 0 30px #8a2be2; }
}

@keyframes slideIn {
    0% { transform: translateY(-50px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

.animated-header {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    margin: 20px 0;
    animation: slideIn 1s ease-out;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

.animated-header .text-part {
    background: linear-gradient(45deg, #ff0000, #ff8c00, #ffd700, #32cd32, #1e90ff, #8a2be2);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: glow 3s ease-in-out infinite, gradientShift 4s ease infinite;
    -webkit-text-stroke: 1px black;
    text-stroke: 1px black;
}

.animated-header .emoji {
    color: initial;
    -webkit-text-fill-color: initial;
    background: none;
    text-shadow: none;
    filter: none;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>

<h1 class="animated-header">
<span class="emoji">🤖</span> 
<span class="text-part">AI-Powered Personal Finance Assistant</span> 
<span class="emoji">💡</span>
</h1>
''', unsafe_allow_html=True)

#Sub Title 
st.markdown('<p style="text-align:center; color:yellow;">Upload your UPI Transaction History PDF for smart financial insights</p>', unsafe_allow_html=True)

# Upload PDF
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"], help="Only PDF files are supported")

# Info button
col1, col2 = st.columns([0.05, 0.95])

with col1:
    if "show_info" not in st.session_state:
        st.session_state.show_info = False

    if st.button("ℹ️", help="Click to toggle usage instructions"):
        st.session_state.show_info = not st.session_state.show_info

with col2:
    if st.session_state.show_info:
        st.markdown("""
        ### 📘 How to Use This Tool
        - 📂 **Upload** your UPI Transaction History PDF file.
        - 🧠 **AI** will analyze your transactions automatically.
        - 📊 You'll receive a detailed financial report including:
          - 💸 Income & Expenses  
          - 💰 Savings Percentage  
          - 📂 Category-Wise Spending  
          - 💡 Smart Budgeting Advice  
        """)

# Function to extract text from PDF
def extract_text_from_pdf(file_path: str) -> str | None:
    """Extracts text from a PDF file using PyPDF2."""
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"❌ PDF Extraction Error: {e}")
        return None

# Function to build the prompt for Gemini with emojis and user advice
def build_financial_prompt(transaction_text: str) -> str:
    """Generates a formatted prompt for Gemini based on transaction data, including emojis and advice."""
    return textwrap.dedent(f"""
        Analyze the following Paytm transaction history and generate detailed financial insights and personalized advice:

        {transaction_text}

        Present the analysis in the following structured format with relevant emojis and a final section offering financial advice:

        **📊 Financial Insights for [User Name]**

        **💰 Overall Monthly Income & Expenses:**
        - Month: [Month]
        - Income: ₹[Amount]
        - Expenses: ₹[Amount]

        **🛑 Unnecessary Expenses Analysis:**
        - Expense Category: [Category Name]
        - Amount: ₹[Amount]
        - Recommendation: [Suggestion]

        **💵 Savings Percentage Calculation:**
        - Savings Percentage: [Percentage] %

        **📈 Expense Trend Analysis:**
        - Notable Trends: [Trend Details]

        **🔧 Cost Control Recommendations:**
        - Suggestion: [Detailed Suggestion]

        **📂 Category-Wise Spending Breakdown:**
        - Category: [Category Name] - ₹[Amount]

        **💡 Personalized Financial Advice:**
        - Offer clear and actionable advice to the user on how to better manage their money based on the insights above. Include tips for saving more, avoiding unnecessary spending, or optimizing budget categories.

        Set the subheading font size to 4 and the body text size to 3. Highlight the subheadings in #00e600 color code.
    
    """)

# Function to call Gemini API with retry logic
def generate_insights_with_retry(prompt: str, model_name: str = "gemini-1.5-flash", max_retries: int = 3, delay_range=(2, 5)) -> str | None:
    """Uses Gemini API to generate insights with retry logic."""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            st.warning(f"Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(*delay_range))
            else:
                st.error("🚫 Analysis failed after several attempts.")
                return None

# Main Logic
if uploaded_file:
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded!")

    with st.spinner("📖 Extracting text..."):
        raw_text = extract_text_from_pdf(temp_path)

    if raw_text:
        prompt = build_financial_prompt(raw_text)

        with st.spinner("🧠 Gemini is analyzing your financial data..."):
            insights = generate_insights_with_retry(prompt)

        if insights:
            st.subheader("📈 Financial Analysis Report")
            st.markdown(insights, unsafe_allow_html=True)
            st.snow()
        else:
            st.error("⚠️ Unable to generate insights. Please try again later.")
    else:
        st.error("📄 Could not extract text from this PDF. Make sure it's not a scanned image.")

    os.remove(temp_path)
