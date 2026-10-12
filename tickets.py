from .database import DatabaseService


class Tickets:
    @staticmethod
    def find_by_passport_and_number(passport_number, ticket_number):
        return DatabaseService.fetch_one(
            """
            SELECT TicketID, Ticket_Number, Passport_Number, Flight_Date, Amount
            FROM Tickets
            WHERE Passport_Number = %s AND Ticket_Number = %s
            LIMIT 1
            """,
            (passport_number.strip(), ticket_number.strip()),
        )
