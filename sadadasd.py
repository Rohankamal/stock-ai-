class InvalidAgeError(Exception):
    def __init__(self, message="Age must be between 0 and 120"):
        self.message = message
        super().__init__(self.message)

try:
    age = int(input("Enter your age: "))
    if age < 0 or age > 120:
        raise InvalidAgeError(f"Invalid age: {age}. Age must be between 0 and 120")
    else:
        print(f"Age {age} is valid.")
except InvalidAgeError as ex:
    print(ex)



