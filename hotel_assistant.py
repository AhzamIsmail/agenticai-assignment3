# file: hotel_assistant.py
"""
Core HotelAssistant logic using SimpleAgent (no shim, no external deps).
"""

from __future__ import annotations
import logging
from typing import Optional
from config import HOTELS, MODEL, guardrail_input_function

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- SimpleAgent Implementation ---------------------------------------------------
class SimpleAgent:
    def __init__(self, name: str, instructions: str = "", model: Optional[str] = None,
                 input_guardrails=None, output_guardrails=None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.input_guardrails = input_guardrails or []
        self.output_guardrails = output_guardrails or []

    def query(self, user_input: str) -> str:
        user_q = user_input.lower()

        # Guardrail check
        for guardrail in self.input_guardrails:
            if not guardrail(user_input):
                return "⚠️ Invalid input."

        # Check which hotel this agent is handling
        lines = self.instructions.splitlines()
        hotel_name = None
        for line in lines:
            if line.strip().startswith("- Hotel name:"):
                hotel_name = line.split(":", 1)[1].strip()
        hotel_data = HOTELS.get(hotel_name)

        if not hotel_data:
            return "❌ Hotel not found in database."

        available = hotel_data["total_rooms"] - hotel_data["reserved_rooms"]

        # Responses
        if "room" in user_q or "available" in user_q or "how many" in user_q:
            return f"There are {available} rooms available for public at {hotel_name}."

        if "owner" in user_q:
            return f"The owner of {hotel_name} is {hotel_data['owner']}."

        return f"🤖 {self.name}: Sorry, I didn't understand your question."


# --- build_instructions -----------------------------------------------------------
def build_instructions(hotel_name: str) -> str:
    if hotel_name not in HOTELS:
        return "You are a helpful hotel customer care assistant. The requested hotel is not in the database."
    data = HOTELS[hotel_name]
    available = data["total_rooms"] - data["reserved_rooms"]
    return (
        f"You are a helpful hotel customer care assistant.\n"
        f"- Hotel name: {hotel_name}\n"
        f"- Owner: {data['owner']}\n"
        f"- Total rooms: {data['total_rooms']}\n"
        f"- Reserved for special guests: {data['reserved_rooms']}\n"
        f"- Available rooms for public: {available}\n"
    )


# --- HotelAssistant wrapper -------------------------------------------------------
class HotelAssistant:
    """Wrapper that composes an `Agent` implementation; accepts agent_cls for testing/injection."""

    def __init__(self, agent_cls: type = SimpleAgent) -> None:
        self._agent = agent_cls(
            name="Hotel Customer Care",
            instructions="You are a helpful hotel assistant.",
            model=MODEL,
            input_guardrails=[guardrail_input_function],
            output_guardrails=[],
        )

    def query(self, user_input: str, hotel_name: Optional[str] = None) -> str:
        target_hotel = hotel_name or list(HOTELS.keys())[0]
        instructions = build_instructions(target_hotel)
        self._agent.instructions = instructions
        return self._agent.query(user_input)


# singleton instance for quick use
hotel_assistant = HotelAssistant()

# convenience exports
__all__ = ["HotelAssistant", "hotel_assistant", "build_instructions", "SimpleAgent"]
