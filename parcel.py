from decimal import Decimal
from .database import DatabaseService


class Parcel:
    def __init__(self, sender_name, recipient_name, description, weight, destination):
        self.sender_name = sender_name.strip()
        self.recipient_name = recipient_name.strip()
        self.description = description.strip()
        self.weight = Decimal(str(weight))
        self.destination = destination.strip()

    def save(self):
        query = """
            INSERT INTO Parcel_Sending
                (Sender_Name, Recipient_Name, Parcel_Description, Weight, Destination)
            VALUES (%s, %s, %s, %s, %s)
        """
        return DatabaseService.execute_insert(
            query, (self.sender_name, self.recipient_name, self.description,
                    self.weight, self.destination)
        )
