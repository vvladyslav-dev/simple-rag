import streamlit as st
import tempfile
from core.usecases.collection_exists import CollectionExistsUseCaseRequest
from core.usecases.index_documents import IndexPDFUseCaseRequest
from core.usecases.retrieve import RetrieveUseCaseRequest
from core.usecases.generate import GenerateUseCaseRequest
from infrastructure.document_loaders.pdf_loader import PDFDocumentLoader
from mediatr import Mediator

def handle_pdf_upload(uploaded_file):
    exists = Mediator.send(CollectionExistsUseCaseRequest(collection_name=uploaded_file.name)).exists
    if exists:
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    loader = PDFDocumentLoader(tmp_path)
    response = Mediator.send(IndexPDFUseCaseRequest(loader=loader, collection_name=uploaded_file.name))

    if response.success:
        st.success("Document indexed successfully!")
    else:
        st.error("Failed to index document!")

def handle_generate_response(selected_collection, input_text):
    if not selected_collection:
        st.error("Please select or upload a collection first.")
        return

    with st.spinner("Generating response..."):
        try:
            retrieve_response = Mediator.send(RetrieveUseCaseRequest(question=input_text, collection_name=selected_collection))
            generate_response_obj = Mediator.send(
                GenerateUseCaseRequest(question=input_text, context=retrieve_response.context)
            )
            st.success("Response:")
            st.write(generate_response_obj.answer)
        except Exception as e:
            st.error(f"Failed to generate response: {e}")
