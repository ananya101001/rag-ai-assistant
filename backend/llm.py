# backend/llm.py
import ollama
from config import LLM_MODEL

def generate_rag_response(question, retrieval_results):
    # Safety check
    if not retrieval_results:
        return "Error: No results to process.", []

    context_text = ""
    sources = set()
    
    if retrieval_results['documents'] and retrieval_results['documents'][0]:
        for i, doc in enumerate(retrieval_results['documents'][0]):
            context_text += f"--- Snippet {i+1} ---\n{doc}\n\n"
            if retrieval_results['metadatas'][0][i]:
                sources.add(retrieval_results['metadatas'][0][i]['source'])
    
    prompt = f"""
    You are a Secure AI Audit Assistant. Answer strictly based on the context.
    
    Context:
    {context_text}
    
    Question: 
    {question}
    """

    try:
        stream = ollama.chat(
            model=LLM_MODEL, 
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        return stream, list(sources)
    except Exception as e:
        return f"Error: {str(e)}", []