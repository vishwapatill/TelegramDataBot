import ollama
from LLMStruct import BaseLLM
from typing import List, Dict, Any, Optional
class OllamaLLM(BaseLLM):
    """Ollama LLM provider using the official Ollama Python SDK."""

    def __init__(
        self,
        model_name: str = "llama2",
        base_url: str = "http://localhost:11434",
        **kwargs
    ):
        """
        Initialize the Ollama LLM provider.

        Args:
            model_name: Name of the Ollama model (e.g., "llama2", "mistral").
            base_url: Base URL of the Ollama server.
            **kwargs: Additional arguments for the Ollama client.
        """
        self.model_name = model_name
        self.base_url = base_url
        # Set the base URL for the Ollama client
        ollama.Client(host=base_url)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """
        Generate a response from the Ollama model.

        Args:
            prompt: User prompt.
            system_prompt: Optional system prompt for context.
            stream: If True, streams the response (not implemented here for simplicity).
            **kwargs: Additional generation parameters (e.g., temperature, top_p).

        Returns:
            Generated response as a string.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                stream=stream,
                **kwargs
            )
            return response["message"]["content"]
        except ollama.ResponseError as e:
            raise RuntimeError(f"Ollama generation error: {e}")

    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Note: The official Ollama SDK does not yet support embeddings,
        so we fall back to the REST API using `requests`.

        Args:
            texts: List of texts to embed.
            **kwargs: Additional embedding parameters.

        Returns:
            List of embeddings (each as a list of floats).
        """
        import requests
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model_name, "prompt": texts[0]},  # Ollama embeds one text at a time
                **kwargs
            )
            response.raise_for_status()
            return [response.json()["embedding"]]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama embedding error: {e}")

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        Generate a streaming response from the Ollama model.

        Args:
            prompt: User prompt.
            system_prompt: Optional system prompt for context.
            **kwargs: Additional generation parameters.

        Yields:
            Generated response chunks as strings.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                stream=True,
                **kwargs
            )
            for chunk in response:
                yield chunk["message"]["content"]
        except ollama.ResponseError as e:
            raise RuntimeError(f"Ollama streaming error: {e}")
