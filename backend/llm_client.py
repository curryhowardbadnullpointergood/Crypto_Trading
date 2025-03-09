# src/llm_client_simple.py  # Renamed file to indicate simplicity

import aiohttp
import logging
import json  # Still need json for payload
from typing import Dict, List, Any  # Keep necessary types

# Basic logger setup - for errors, can be further simplified if needed
logging.basicConfig(level=logging.ERROR) # Simpler logging level
logger = logging.getLogger(__name__)

class SimpleChatClient: # Renamed class for simplicity
    """
    A basic client for interacting with a chat-based LLM API (like GaiaNet).
    Simplified for easy use in a hackathon project.
    """

    API_URL = "https://0xe7d21e1bd35163c0bcdc6d5ea8c23f3c277f2d17.us.gaianet.network/v1/chat/completions" # Direct URL, simpler

    def __init__(self):
        """Initializes the SimpleChatClient."""
        self._session = None # Use underscore to indicate "internal"
        self.default_system_prompt = ( # Renamed to prompt for simplicity
            "Act as a crypto trading expert. Provide concise, actionable advice based on market analysis."
        )

    async def _get_session(self): # Simplified session management, internal method
        """Manages the aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"} # Minimal headers
            )
        return self._session

    async def close_session(self): # Method to close session if needed
        """Closes the aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def get_response( # Renamed from chat_completion to get_response, more generic
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500, # Reduced default max_tokens for simplicity
        temperature: float = 0.7,
    ) -> Optional[Dict[str, Any]]: # Optional return type for error handling
        """
        Sends a request to the LLM API and returns the response.
        Simplified error handling and request process.
        """
        session = await self._get_session() # Get or create session
        api_endpoint = self.API_URL # Use class constant directly

        # Ensure system message - simpler check
        has_system_message = False
        for msg in messages:
            if msg.get('role') == 'system':
                has_system_message = True
                break
        if not has_system_message:
            messages.insert(0, {"role": "system", "content": self.default_system_prompt})


        payload = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model": "Meta-Llama-3-8B-Instruct-Q5_K_M", # Model name kept
        }

        try:
            async with session.post(api_endpoint, json=payload) as response:
                if response.status == 200:
                    return await response.json() # Return JSON directly
                else:
                    error_text = await response.text()
                    logger.error(f"LLM API Error {response.status}: {error_text}") # Simpler error log
                    return None # Indicate failure with None

        except aiohttp.ClientError as e:
            logger.error(f"Network error during API request: {e}") # Simpler network error log
            return None # Indicate failure with None
        except Exception as e:
            logger.exception("Unexpected error during LLM API call:") # More general exception logging
            return None # Indicate failure with None


# Example usage (optional, for demonstration in this file)
async def main():
    client = SimpleChatClient()
    try:
        user_message = "Analyze the current market for Solana and BONK. Give trading advice."
        messages = [{"role": "user", "content": user_message}]
        response_data = await client.get_response(messages)

        if response_data:
            if response_data.get('choices'):
                ai_response = response_data['choices'][0]['message']['content']
                print("AI Response:\n", ai_response)
            else:
                print("No 'choices' in API response.")
        else:
            print("Failed to get a response from the LLM API.")

    finally:
        await client.close_session() # Ensure session is closed

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())