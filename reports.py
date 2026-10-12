from .database import DatabaseService


class Reports:
    def __init__(self, full_name, id_number, issue):
        self.full_name = full_name.strip()
        self.id_number = int(id_number) if str(id_number).strip() else None
        self.issue = issue.strip()

    def save(self):
        return DatabaseService.execute_insert(
            """
            INSERT INTO Reports (Full_Name, ID_Numbber, Issue)
            VALUES (%s, %s, %s)
            """,
            (self.full_name, self.id_number, self.issue),
        )
