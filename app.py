import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


from chatbot import get_ai_response
from pdf_tools import extract_text_from_pdf
from data_tools import dataset_summary
from analyze_resume import analyze_resume

st.set_page_config(
    page_title="SmartAssist Pro",
    page_icon="🤖",
    layout="wide"
)

# --------------------------
# Custom CSS
# --------------------------
st.markdown("""
<style>

/* Background */

.stApp{
background: linear-gradient(
135deg,
#0f172a,
#1e293b,
#334155
);
}

/* Sidebar */

[data-testid="stSidebar"]{
background:#111827;
}

/* Glass Cards */

.glass{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(12px);
padding:20px;
border-radius:20px;
margin-bottom:15px;
border:1px solid rgba(255,255,255,0.1);
}

/* Hero */

.hero{
text-align:center;
padding:20px;
border-radius:20px;
background: rgba(255,255,255,0.05);
backdrop-filter: blur(10px);
margin-bottom:20px;
}

/* Text */

h1,h2,h3,p,label{
color:white !important;
}

</style>
""", unsafe_allow_html=True)

#------------------------------

# --------------------------
# Session State
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# Header
# --------------------------
st.title("🤖 SmartAssist Pro")
st.markdown("""
<div class='hero'>
<h1>🤖 SmartAssist Pro</h1>
<p>
AI Career Coach • Resume Analyzer • Data Dashboard
</p>
</div>
""", unsafe_allow_html=True)
st.caption("AI Career • Data • Resume Assistant")

# --------------------------
# Sidebar
# --------------------------
st.markdown("""
<div class='glass' style='color:white;'>
    <h3 style='color:white;'>🚀 Welcome to SmartAssist Pro</h3>

<ul style="color:white;">
<li style="color:white;">💬 AI Chat Assistant</li>
<li style="color:white;">📄 PDF Analysis</li>
<li style="color:white;">💼 Resume Review</li>
<li style="color:white;">📊 Data Dashboard</li>
<li style="color:white;">📈 Interactive Charts</li>
</ul>
""",unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigation",
    [
        "AI Chat",
        "PDF Analyzer",
        "Resume Analyzer",
        "Data Dashboard"
    ]
)

# ===================================================
# AI CHAT
# ===================================================

if menu == "AI Chat":

    st.subheader("💬 AI Assistant")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask anything..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Thinking..."):

            reply = get_ai_response(
                st.session_state.messages
            )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":reply
            }
        )

        with st.chat_message("assistant"):
            st.write(reply)

    # Download Chat

    chat_text = ""

    for msg in st.session_state.messages:

        chat_text += (
            f"{msg['role'].upper()} : "
            f"{msg['content']}\n\n"
        )

    st.download_button(
        "📥 Download Chat",
        chat_text,
        file_name="chat_history.txt"
    )

# ===================================================
# PDF ANALYZER
# ===================================================

elif menu == "PDF Analyzer":

    st.subheader("📄 PDF Analyzer")

    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if pdf:

        text = extract_text_from_pdf(pdf)

        stats = get_pdf_statistics(text)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Words",
            stats["Words"]
        )

        col2.metric(
            "Characters",
            stats["Characters"]
        )

        col3.metric(
            "Lines",
            stats["Lines"]
        )

        st.text_area(
            "Extracted Text",
            text,
            height=400
        )

# ===================================================
# RESUME ANALYZER
# ===================================================

elif menu == "Resume Analyzer":

    st.subheader("💼 Resume Analyzer")

    pdf = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if pdf:

        text = extract_text_from_pdf(pdf)

        report = analyze_resume(text)

        st.success("Resume Analysis Completed")

        st.text_area(
            "Analysis Report",
            report,
            height=350
        )

# ===================================================
# DATA DASHBOARD
# ===================================================

elif menu == "Data Dashboard":

    st.subheader("📊 Data Dashboard")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.dataframe(df.head())

        dataset_summary(df)

        st.subheader("🔥 Correlation Matrix")

        numeric_df = df.select_dtypes(
            include="number"
        )

        if len(numeric_df.columns) > 1:
            corr = numeric_df.corr()
            st.dataframe(corr)

        numeric_cols = (
            df.select_dtypes(
                include="number"
            ).columns
        )

        if len(numeric_cols) > 0:

            column = st.selectbox(
                "Select Column",
                numeric_cols
            )

            fig = px.histogram(
                df,
                x=column,
                title=f"Distribution of {column}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

#box plot  
            fig2 = px.box(
                df,
                y=column,
                title=f"Box Plot - {column}"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


# Scatter Plot
        if len(numeric_cols) >= 2:

            st.subheader("📉 Scatter Plot")
            x_col = st.selectbox(
                "X Axis",
                numeric_cols,
                key="x"
            )

            y_col = st.selectbox(
                "Y Axis",
                numeric_cols,
                key="y"
            )

            fig3 = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{x_col} vs {y_col}"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )
st.markdown("""
<hr>

<center>

Built with ❤️ using Streamlit

</center>
""", unsafe_allow_html=True)

            