class Person:
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.id = None

    def print_person(self, id):
        print(f"#{id} : {self.firstname} {self.lastname}")