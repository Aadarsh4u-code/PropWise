from rag import generate_answer, process_urls
import streamlit as st

# Set the page configuration and title
st.set_page_config(page_title="PropWise", page_icon="🏡")
st.title("🏙️PropWise AI Assistant", anchor=False)
st.caption("_'Turning Real Estate Data into Smart Decisions.'_")
st.divider()



st.sidebar.header("About PropWise")
st.sidebar.markdown(
    """
    **PropWise** is an AI-powered RAG-based real estate research tool that extracts insights from trusted sources like **CNBC**, **CBRE Ireland**, and **realtor.com**, enabling analysts to make informed decisions with accurate and relevant information on properties, market trends, and investment opportunities.
    """
)
st.sidebar.divider()

url1 = st.sidebar.text_input("URL 1", placeholder="Enter first URL")
url2 = st.sidebar.text_input("URL 2", placeholder="Enter second URL")
url3 = st.sidebar.text_input("URL 3", placeholder="Enter third URL")


# Placeholder for status messages
status_placeholder = st.empty()

# Placeholder for question input
query_placeholder = st.empty()

process_url_button = st.sidebar.button("Process URLs", type="primary")


if process_url_button:
    urls = [url for url in (url1, url2, url3) if url != '']
    if len(urls) == 0:
        status_placeholder.text("You must provide at least one valid URL.")
    else:
        for status in process_urls(urls):
            status_placeholder.text(status)

query = query_placeholder.text_input("Question")
if query:
    try:
        answer, sources = generate_answer(query)
        st.header("Answer:")
        st.write(answer)

        if sources:
            st.subheader("Sources:")
            for source in sources:
                st.write(source)
    except RuntimeError as e:
        status_placeholder.text("You must process urls first")