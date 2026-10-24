"""Main entry point for Task 35 - Employee Ranking System.

Usage:
  python main.py          # Launches the Desktop GUI application
  python main.py --cli    # Launches interactive Terminal CLI demonstration
  python main.py --help   # Displays usage information
"""
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Task 35: Employee Ranking System using Data Structures and Algorithms."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run interactive command-line interface instead of GUI"
    )
    args = parser.parse_args()

    if args.cli:
        from cli.menu import run_cli_menu
        run_cli_menu()
    else:
        try:
            import tkinter as tk
            from ui.app import EmployeeRankingApp

            root = tk.Tk()
            app = EmployeeRankingApp(root)
            root.mainloop()
        except Exception as e:
            print(f"[Notice] Failed to start GUI ({e}). Falling back to CLI mode...")
            from cli.menu import run_cli_menu
            run_cli_menu()


if __name__ == "__main__":
    main()
