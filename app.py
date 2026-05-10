import streamlit as st

from document_reader import read_uploaded_file

from ai_functions import (
    generate_summary,
    extract_key_data,
    answer_question
)

from friction_tracker import (
    log_event,
    generate_report
)


st.set_page_config(
    page_title="AI Document Assistant",
    layout="centered"
)

st.title("AI Document Assistant")
st.write("Upload a document to summarize, extract key data, ask questions, and track UX friction.")


# =====================
# Session State
# =====================
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "key_data" not in st.session_state:
    st.session_state.key_data = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_name" not in st.session_state:
    st.session_state.file_name = ""

if "ux_events" not in st.session_state:
    st.session_state.ux_events = []


# =====================
# File Upload
# =====================
uploaded_file = st.file_uploader(
    "Upload your document",
    type=["txt", "pdf", "docx", "eml"]
)

if uploaded_file is not None:

    if uploaded_file.name != st.session_state.file_name:

        document_text = read_uploaded_file(uploaded_file)

        if document_text.strip() == "":
            st.warning("Cannot read this file.")

            log_event(
                st.session_state.ux_events,
                "error",
                "File Upload"
            )

        else:
            log_event(
                st.session_state.ux_events,
                "upload",
                "File Upload"
            )

            st.session_state.document_text = document_text
            st.session_state.file_name = uploaded_file.name
            st.session_state.messages = []
            st.session_state.summary = ""
            st.session_state.key_data = ""

            st.success("File uploaded successfully.")

            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_summary(document_text)

            with st.spinner("Extracting key data points..."):
                st.session_state.key_data = extract_key_data(document_text)


# =====================
# Display Document Results
# =====================
if st.session_state.document_text:
    with st.expander("Preview document"):
        st.write(st.session_state.document_text[:1500])

if st.session_state.summary:
    st.subheader("Document Summary")
    st.write(st.session_state.summary)

if st.session_state.key_data:
    st.subheader("Extracted Key Data Points")
    st.write(st.session_state.key_data)


# =====================
# Chat
# =====================
st.subheader("Ask Questions About the Document")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_question = st.chat_input("Ask something about the document...")

if user_question:

    log_event(
        st.session_state.ux_events,
        "question",
        "Chat Input"
    )

    if not st.session_state.document_text:
        st.warning("Please upload a document first.")

        log_event(
            st.session_state.ux_events,
            "error",
            "Chat Input"
        )

    else:
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Thinking..."):
            answer = answer_question(
                st.session_state.document_text,
                user_question
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)


# =====================
# UX Friction Diagnostic Report
# =====================
st.divider()

st.header("UX Friction Diagnostic Report")

report = generate_report(
    st.session_state.ux_events
)

st.subheader("Session Analysis")

st.write(
    f"Friction Index (FI): {report['friction_index']}"
)

st.write(
    f"Session Category: {report['session_category']}"
)

st.write(
    f"Total Interaction Events: {report['total_events']}"
)

st.subheader("Predicted Friction Hotspots")

if report["hotspots"]:

    for hotspot in report["hotspots"]:

        st.write(f"""
### {hotspot['area']}

- Friction Level: {hotspot['friction_level']}
- Interaction Count: {hotspot['interaction_count']}
""")

else:
    st.write("No hotspots detected.")