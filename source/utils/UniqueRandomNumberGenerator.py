import random


class UniqueRandomNumberGenerator:
    def __init__(self):
        self.generated_numbers = set()

    def generate_unique_number(self, length = 10):
        if length <= 0:
            raise ValueError("Length must be a positive integer")
        

        min_value = 10 ** (length - 1)
        max_value = (10 ** length) - 1

        while True:
            
            
            new_number = random.randint(min_value, max_value)
            
            from person.models import Person
            
            if new_number not in self.generated_numbers and not Person.objects.filter(phone_number=new_number).exists():
                self.generated_numbers.add(new_number)
                return new_number