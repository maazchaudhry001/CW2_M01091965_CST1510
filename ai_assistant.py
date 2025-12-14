from typing import List, Dict
from openai import OpenAI


class AIAssistant:
    """Service class that manages interactions with the OpenAI Chat API."""

    def __init__(
        self,
        api_key: str,
        system_prompt: str = "You are a helpful assistant."
    ):
        self._client = OpenAI(api_key=api_key)
        self._system_prompt = system_prompt
        self._conversation: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

    def update_system_prompt(self, prompt: str) -> None:
        """Update the system prompt and reset the conversation history."""
        self._system_prompt = prompt
        self.reset_conversation()

    def send_message(
        self,
        message: str,
        model: str = "gpt-4o-mini"
    ) -> str:
        """Send a message to the AI model and return its response."""
        self._conversation.append(
            {"role": "user", "content": message}
        )

        response = self._client.chat.completions.create(
            model=model,
            messages=self._conversation,
        )

        reply = response.choices[0].message.content
        self._conversation.append(
            {"role": "assistant", "content": reply}
        )
        return reply

    def reset_conversation(self) -> None:
        """Clear conversation history while keeping the system prompt."""
        self._conversation = [
            {"role": "system", "content": self._system_prompt}
        ]
