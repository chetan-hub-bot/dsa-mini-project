"""Utilities to load, export, and generate employee datasets for testing and benchmarks."""
import csv
import os
import random
from typing import List
from core.employee import Employee

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_CSV_PATH = os.path.join(DATA_DIR, "sample_employees.csv")

FIRST_NAMES = [
    "Aarav", "Aditi", "Aditya", "Akash", "Ananya", "Arjun", "Deepak", "Dev",
    "Divya", "Gaurav", "Ishaan", "Ishita", "Kabir", "Karan", "Kavita", "Manish",
    "Meera", "Neha", "Pooja", "Pranav", "Priya", "Rahul", "Rajesh", "Rhea",
    "Rohan", "Rohit", "Sanya", "Siddharth", "Sneha", "Tanvi", "Varun", "Vikram"
]

LAST_NAMES = [
    "Sharma", "Patel", "Verma", "Iyer", "Singh", "Gupta", "Reddy", "Malhotra",
    "Roy", "Joshi", "Kapoor", "Desai", "Nair", "Sen", "Mehta", "Kulkarni",
    "Mukherjee", "Chopra", "Singhania", "Bansal", "Khanna", "Sundaram", "Bhatt", "Menon"
]

DEPARTMENTS = ["Engineering", "Data Science", "Product", "Marketing", "Sales", "HR", "Finance"]


def load_sample_employees(csv_path: str = SAMPLE_CSV_PATH) -> List[Employee]:
    """Load employee records from a CSV file."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Employee data file not found at: {csv_path}")

    employees = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(Employee.from_dict(row))
    return employees


def save_employees_to_csv(employees: List[Employee], target_path: str) -> None:
    """Save an employee list to a CSV file."""
    if not employees:
        return

    fieldnames = ["emp_id", "name", "department", "salary", "experience_years", "performance_rating"]
    with open(target_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow({
                "emp_id": emp.emp_id,
                "name": emp.name,
                "department": emp.department,
                "salary": emp.salary,
                "experience_years": emp.experience_years,
                "performance_rating": emp.performance_rating,
            })


def generate_synthetic_employees(count: int, seed: int = 42) -> List[Employee]:
    """Generate a reproducible synthetic list of N employees for benchmarking."""
    rng = random.Random(seed)
    records = []

    for i in range(1, count + 1):
        emp_id = f"SYN{i:05d}"
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        department = rng.choice(DEPARTMENTS)
        # Experience: 0.5 to 20.0 years
        exp = round(rng.uniform(0.5, 20.0), 1)
        # Salary roughly correlated with experience + base + variance
        base_salary = 50000 + (exp * 7000) + rng.uniform(-10000, 25000)
        salary = round(max(40000.0, min(base_salary, 220000.0)), 2)
        # Performance rating: 2.0 to 5.0 with normal-ish distribution
        rating = round(min(5.0, max(2.0, rng.gauss(4.0, 0.6))), 1)

        records.append(Employee(
            emp_id=emp_id,
            name=name,
            department=department,
            salary=salary,
            experience_years=exp,
            performance_rating=rating,
        ))

    return records


if __name__ == "__main__":
    sample = load_sample_employees()
    print(f"Loaded {len(sample)} sample employees.")
    for emp in sample[:3]:
        print(emp)
