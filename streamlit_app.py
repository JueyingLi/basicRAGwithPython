from __future__ import annotations

import streamlit as st

from gemini_llm import DEFAULT_GEMINI_MODEL
from rag_service import DOCUMENT_PATH, EMBEDDING_MODEL_NAME, run_rag

st.set_page_config(page_title="Basic RAG Viewer", layout="wide")

st.title("Basic RAG Viewer")
st.caption("Ask a question, inspect the best match, and review the top similar chunks.")

with st.sidebar:
    st.header("Settings")
    document_path = st.text_input("Document path", value=DOCUMENT_PATH)
    embedding_model_name = st.text_input("Embedding model", value=EMBEDDING_MODEL_NAME)
    llm_model_name = st.text_input("LLM model", value=DEFAULT_GEMINI_MODEL)
    use_llm = st.checkbox("Use Gemini for final answer", value=True)
    n_results = st.slider("Top N similar results", min_value=1, max_value=10, value=5)
    rerank_top_k = st.slider("Top K reranked results", min_value=1, max_value=10, value=3)

query = st.text_area("Question", height=120, placeholder="Type your question here...")
submit = st.button("Run RAG", type="primary")

if submit:
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running retrieval and reranking..."):
            response = run_rag(
                query=query,
                n_results=n_results,
                rerank_top_k=rerank_top_k,
                document_path=document_path,
                embedding_model_name=embedding_model_name,
                llm_model_name=llm_model_name,
                use_llm=use_llm,
            )

        st.subheader("Question")
        st.write(response["query"])

        st.subheader("LLM Status")
        st.write(response["llm_status"])

        st.subheader("Final Result")
        st.write(response["final_result"] or "No result found.")

        st.subheader("Top Retrieval Result")
        st.write(response["retrieval_result"] or "No reranked result found.")

        st.subheader("Reranked Results")
        for index, item in enumerate(response["reranked_results"], start=1):
            st.markdown(f"**Rank {index}**")
            st.write(item)

        st.subheader(f"Top {len(response['similar_results'])} Similar Results")
        for item in response["similar_results"]:
            with st.expander(f"Rank {item['rank']} | Distance: {item['distance']}", expanded=False):
                st.write(item["document"])
