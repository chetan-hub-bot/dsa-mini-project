"""Data management and generation package."""
from .generator import load_sample_employees, generate_synthetic_employees, save_employees_to_csv

__all__ = ["load_sample_employees", "generate_synthetic_employees", "save_employees_to_csv"]
