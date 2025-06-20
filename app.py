import streamlit as st
from backend.document_parser import parse_document
from backend.embedder import prepare_document_index
from backend.retriever import retrieve_relevant_chunks
from backend.responder import format_prompt, generate_answer
from utils.helpers import clean_text

st.set_page_config(page_title="LawBridge AI", layout="wide")
st.title("⚖️ LawBridge AI")
st.markdown("Upload a legal document (PDF or DOCX), ask questions in plain English, and get tailored answers based on your role.")

uploaded_file = st.file_uploader("📄 Upload your legal document", type=["pdf", "docx"])
user_role = st.selectbox("👤 Select your role", ["Tenant", "Lawyer", "Client"])
query = st.text_input("🔍 Ask a legal question")

if st.button("Submit"):
    if not uploaded_file:
        st.warning("Please upload a document.")
    elif not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing your document and query..."):
            try:
                # Step 1: Extract and clean document text
                raw_text = parse_document(uploaded_file)
                cleaned_text = clean_text(raw_text)

                # Step 2: Chunk + Embed + Index
                index, chunks = prepare_document_index(cleaned_text)

                # Step 3: Retrieve most relevant clauses
                top_chunks = retrieve_relevant_chunks(query, index, chunks, top_k=2)
                combined_clause = "\n".join(top_chunks)

                # Step 4: Format prompt and get response
                prompt = format_prompt(combined_clause, query, user_role)
                answer = generate_answer(prompt)

                # Step 5: Show result
                st.success("✅ Answer:")
                st.write(answer)

                with st.expander("📜 Relevant Clause(s) Used"):
                    st.write(combined_clause)

                with st.expander("🧾 Prompt Sent to Model"):
                    st.code(prompt)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
