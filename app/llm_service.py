
import requests


def generate_answer(question, context):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:3b",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a public information assistant. "
                            "Answer using only the provided information. "
                            "Do not invent contact numbers, addresses, "
                            "opening hours, or services. "
                            "If the answer is missing, say so clearly."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: {question}\n\n"
                            f"Available information:\n{context}"
                        ),
                    },
                ],
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        return response.json()["message"]["content"]

    except requests.RequestException as error:
        print("Ollama connection error:", error)
        return (
            "Sorry, the local AI service is unavailable. "
            "Please ensure Ollama is running."
        )
