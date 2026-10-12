class Employee:
    def __init__(self, FullName, ID_Number, Contact, Nationality, Email_Address, Date_Of_Birth, Role, Employee_ID, Salary, Hourly_Rate, Status):
        self.name = FullName
        self.id_number = ID_Number
        self.contact = Contact
        self.nationality = Nationality
        self.email = Email_Address
        self.date_of_birth = Date_Of_Birth
        self.role = Role
        self.employee_id = Employee_ID
        self.salary = Salary
        self.hourly_rate = Hourly_Rate
        self.status = Status

    def Employee(self):
        print(f"Employee Name: {self.name}")
        print(f"ID Number: {self.id_number}")
        print(f"Contact: {self.contact}")
        print(f"Nationality: {self.nationality}")
        print(f"Email: {self.email}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Role: {self.role}")
        print(f"Employee ID: {self.employee_id}")

    def Employee_Status(self):
        print(f"Employee {self.name} is currently {self.status}.")
        print(f"Salary: {self.salary}")
        print(f"Hourly Rate: {self.hourly_rate}")
        