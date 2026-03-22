class RAGBot:
    def __init__(self, llm, retriever, sentenceModel, prompt_logger):
        self.llm = llm
        self.sentenceModel = sentenceModel
        self.retriever = retriever
        self.prompt_logger = prompt_logger

    def answer_query(self, user_id: str, session_id: str, user_query: str):

        # 1. Convert query → embedding
        query_embedding = self.sentenceModel.encode([user_query])[0]

        # 2. Retrieve top chunks
        results = self.retriever.get_top_k_chunks(query_embedding, k=2)
        chunks = [chunk for chunk, _ in results]

        # 3. Build prompt
        context = "\n\n".join(chunks)
        prompt = f"""
You are an expert assistant for a custom t-shirt ecommerce platform.
Use the following context to answer the user's query.
If you don't know the answer, say so.

Context:
{context}

Query: {user_query}
Answer:
"""

        # 4. Generate response
        llm_response = self.llm.generate(prompt)

        # 5. Log
        self.prompt_logger.log_prompt({
            "user_id": user_id,
            "session_id": session_id,
            "user_query": user_query,
            "chunks": chunks,
            "llm_response": llm_response,
            "model_name": self.llm.model_name,
            "metadata": {"temperature": 0.7, "top_k": 2}
        })

        return llm_response