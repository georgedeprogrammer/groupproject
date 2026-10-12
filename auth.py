from .database import DatabaseService


class UserAccount:
    """User login accounts; intentionally separate from customer_details."""

    @staticmethod
    def create(username, email, password, role="customer", id_number=None):
        query = """
            INSERT INTO user_logins (ID_Number, Username, Email, Password, User_Role)
            VALUES (%s, %s, %s, %s, %s)
        """
        return DatabaseService.execute_insert(
            query, (id_number, username.strip(), email.strip(), password, role)
        )

    @staticmethod
    def authenticate(username_or_email, password):
        user = DatabaseService.fetch_one(
            """
            SELECT Login_ID, ID_Number, Username, Email, Password, User_Role
            FROM user_logins
            WHERE Username = %s OR Email = %s
            LIMIT 1
            """,
            (username_or_email.strip(), username_or_email.strip()),
        )
        if user and user["Password"] == password:
            return user
        return None
