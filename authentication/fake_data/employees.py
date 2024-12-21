from faker import Faker
import json

fake = Faker()

employees = []

for i in range(300):
    employees.append({
        "model": "authentication.employee", 
        "pk": i + 1,
        "fields": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "gender": fake.random_element(elements=('Male', 'Female')),
            "age": fake.random_int(min=18, max=65),
            "salary": round(fake.random_number(digits=5, fix_len=True) * 1.0, 2)
        }
    })

with open("authentication/fixtures/0003_employee.json", "w") as f:
    json.dump(employees, f, indent=4)

print(f"Created {len(employees)} employees")
