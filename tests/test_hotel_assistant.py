# file: tests/test_hotel_assistant.py
import unittest
from hotel_assistant import HotelAssistant, build_instructions, SimpleAgent


class HotelAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        # Use SimpleAgent for predictable testing
        self.assistant = HotelAssistant(agent_cls=SimpleAgent)

    def test_available_rooms_paradise(self) -> None:
        resp = self.assistant.query("How many rooms are available?", hotel_name="Hotel Paradise")
        self.assertIn("140", resp)
        self.assertIn("rooms available for public", resp)

    def test_owner_bluesky(self) -> None:
        resp = self.assistant.query("Who is the owner?", hotel_name="Hotel BlueSky")
        self.assertIn("Mr. John Doe", resp)

    def test_default_hotel_used_when_not_specified(self) -> None:
        resp = self.assistant.query("How many rooms are available?")
        self.assertIn("180", resp)

    def test_invalid_hotel_name(self) -> None:
        resp = self.assistant.query("Who is the owner?", hotel_name="Nonexistent Hotel")
        self.assertIn("not in the database", resp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
