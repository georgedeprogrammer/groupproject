from .database import DatabaseService


class OnlineCheckIn:
    def __init__(self, passport_number, full_name, ticket_number, checked_as):
        self.passport_number = passport_number.strip()
        self.full_name = full_name.strip()
        self.ticket_number = ticket_number.strip()
        self.checked_as = checked_as

    def save(self):
        return DatabaseService.execute_insert(
            """
            INSERT INTO Online_CheckIn
                (Passport_Number, Full_Name, Ticket_Number, Checked_As)
            VALUES (%s, %s, %s, %s)
            """,
            (self.passport_number, self.full_name, self.ticket_number, self.checked_as),
        )
