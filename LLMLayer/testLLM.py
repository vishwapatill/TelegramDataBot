from OllamaLLM import OllamaLLM
ollama_llm = OllamaLLM(model_name="mistral", base_url="http://localhost:11434")
prompt = "Explain quantum computing in simple terms."
response = ollama_llm.generate(prompt)
print(response)

texts = ["Quantum computing is a type of computing."]
embeddings = ollama_llm.embed(texts)
print(embeddings[0][:5])  # Print first 5 dimensions


for chunk in ollama_llm.generate_stream(prompt):
    print(chunk, end="", flush=True)

