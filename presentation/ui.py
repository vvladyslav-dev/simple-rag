import streamlit as st
from presentation.actions import handle_generate_response, handle_pdf_upload
from core.usecases.get_collections_list import GetCollectionsListUseCaseRequest
from mediatr import Mediator

def run_app():
    st.title("🦜🔗 RAG App")

    collections_response = Mediator.send(GetCollectionsListUseCaseRequest()).collections
    collection_names = [
        getattr(c, "name", "") for c in getattr(collections_response, "collections", []) if getattr(c, "name", "")
    ]

    selected_collection = st.selectbox(
        "Select collection to query",
        options=collection_names if collection_names else ["<no collections>"],
    )
    if selected_collection == "<no collections>":
        selected_collection = None

    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
    if uploaded_file:
        handle_pdf_upload(uploaded_file)

    with st.form("my_form"):
        input_text = st.text_area("Enter text:", "What are the three key pieces of advice for learning how to code?")
        submitted = st.form_submit_button("Submit")

    if submitted:
        handle_generate_response(selected_collection, input_text)
