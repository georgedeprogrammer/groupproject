from .database import DatabaseService


class Messages:
    @staticmethod
    def subscribe(email):
        return DatabaseService.execute_insert(
            "INSERT INTO Newsletter_Subscribers (Email) VALUES (%s)",
            (email.strip(),),
        )

    @staticmethod
    def contact(name, email, message):
        return DatabaseService.execute_insert(
            """
            INSERT INTO Contact_Messages (Full_Name, Email, Message)
            VALUES (%s, %s, %s)
            """,
            (name.strip(), email.strip(), message.strip()),
        )
