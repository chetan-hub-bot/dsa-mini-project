"""Employee data model and ranking criteria definitions."""
from dataclasses import dataclass, asdict
from typing import Callable, Any, Dict


@dataclass
class Employee:
    """Represents an employee record in the organization."""
    emp_id: str
    name: str
    department: str
    salary: float
    experience_years: float
    performance_rating: float  # Scale: 1.0 - 5.0

    @property
    def composite_score(self) -> float:
        """
        Calculates an overall composite score (0 - 100) combining:
        - 50% Performance Rating (normalized against 5.0 max)
        - 30% Experience (normalized against 25 years max)
        - 20% Salary compensation tier (normalized against $200,000 max)
        """
        norm_perf = min(max(self.performance_rating / 5.0, 0.0), 1.0)
        norm_exp = min(max(self.experience_years / 25.0, 0.0), 1.0)
        norm_salary = min(max(self.salary / 200000.0, 0.0), 1.0)

        weighted = (norm_perf * 0.50) + (norm_exp * 0.30) + (norm_salary * 0.20)
        return round(weighted * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary, including computed composite score."""
        d = asdict(self)
        d["composite_score"] = self.composite_score
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        """Factory method to construct Employee from dictionary/CSV row."""
        return cls(
            emp_id=str(data["emp_id"]).strip(),
            name=str(data["name"]).strip(),
            department=str(data["department"]).strip(),
            salary=float(data["salary"]),
            experience_years=float(data["experience_years"]),
            performance_rating=float(data["performance_rating"]),
        )

    def __str__(self) -> str:
        return (
            f"[{self.emp_id}] {self.name:<18} | Dept: {self.department:<12} | "
            f"Salary: ${self.salary:>10,.2f} | Exp: {self.experience_years:>4.1f} yrs | "
            f"Rating: {self.performance_rating:>3.1f}/5.0 | Score: {self.composite_score:>5.1f}"
        )


# Available ranking criteria with corresponding key extractors and display names
CRITERIA_MAP: Dict[str, Dict[str, Any]] = {
    "performance": {
        "name": "Performance Rating",
        "key": lambda emp: emp.performance_rating,
        "format": lambda val: f"{val:.1f} / 5.0",
        "default_descending": True,
        "description": "Appraisal score based on annual deliverables and manager evaluation.",
    },
    "salary": {
        "name": "Salary ($)",
        "key": lambda emp: emp.salary,
        "format": lambda val: f"${val:,.2f}",
        "default_descending": True,
        "description": "Annual compensation package.",
    },
    "experience": {
        "name": "Experience (Years)",
        "key": lambda emp: emp.experience_years,
        "format": lambda val: f"{val:.1f} yrs",
        "default_descending": True,
        "description": "Total professional industry experience in years.",
    },
    "composite": {
        "name": "Composite Score (0-100)",
        "key": lambda emp: emp.composite_score,
        "format": lambda val: f"{val:.2f}",
        "default_descending": True,
        "description": "Weighted index: 50% Performance, 30% Experience, 20% Salary tier.",
    },
    "id": {
        "name": "Employee ID",
        "key": lambda emp: emp.emp_id,
        "format": lambda val: str(val),
        "default_descending": False,
        "description": "Organizational identifier.",
    },
}
