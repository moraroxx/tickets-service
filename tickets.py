
VALID_PRIORITIES = {"low", "medium", "high"}


class TicketService:
    def __init__(self):
        self.tickets = []
        self.next_id = 1

    def create_ticket(self, title, priority="medium", description=""):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название заявки не может быть пустым")

        if priority not in VALID_PRIORITIES:
            raise ValueError("Недопустимый приоритет заявки")

        ticket = {
            "id": self.next_id,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "status": "open"
        }

        self.tickets.append(ticket)
        self.next_id += 1

        return ticket

    def get_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket["id"] == ticket_id:
                return ticket

        return None

    def get_all_tickets(self):
        return self.tickets.copy()
