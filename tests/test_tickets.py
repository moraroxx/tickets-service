
import unittest

from tickets import TicketService


class TestTicketService(unittest.TestCase):

    def setUp(self):
        self.service = TicketService()

    def test_ticket_is_created(self):
        ticket = self.service.create_ticket("Ошибка входа")
        self.assertEqual(ticket["title"], "Ошибка входа")

    def test_default_priority_is_medium(self):
        ticket = self.service.create_ticket("Ошибка входа")
        self.assertEqual(ticket["priority"], "medium")

    def test_valid_low_priority(self):
        ticket = self.service.create_ticket("Заявка", "low")
        self.assertEqual(ticket["priority"], "low")

    def test_valid_high_priority(self):
        ticket = self.service.create_ticket("Заявка", "high")
        self.assertEqual(ticket["priority"], "high")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create_ticket("Заявка", "urgent")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create_ticket("   ")

    def test_title_is_trimmed(self):
        ticket = self.service.create_ticket("  Заявка  ")
        self.assertEqual(ticket["title"], "Заявка")

    def test_ticket_can_be_found_by_id(self):
        ticket = self.service.create_ticket("Заявка")
        found = self.service.get_ticket(ticket["id"])
        self.assertEqual(found, ticket)

    def test_missing_ticket_returns_none(self):
        self.assertIsNone(self.service.get_ticket(999))

    def test_ticket_ids_increment(self):
        first = self.service.create_ticket("Первая")
        second = self.service.create_ticket("Вторая")
        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)


if __name__ == "__main__":
    unittest.main()
