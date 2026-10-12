from .database import DatabaseService


class Booking:
    def __init__(self, passport_number, departure_date, return_date,
                 passengers, destination, travel_class):
        self.passport_number = passport_number.strip()
        self.departure_date = departure_date
        self.return_date = return_date or None
        self.passengers = int(passengers)
        self.destination = destination.strip()
        self.travel_class = travel_class

    def save(self):
        query = """
            INSERT INTO Flight_Booking
                (Passport_Number, Depature_Date, Return_Date, Passangers,
                 Destination, Class)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return DatabaseService.execute_insert(
            query, (self.passport_number, self.departure_date, self.return_date,
                    self.passengers, self.destination, self.travel_class)
        )
