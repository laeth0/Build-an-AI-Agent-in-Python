from functions.run_python import run_python_file


def main():
    print("Result for main.py without args:")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Result for main.py with calculator args:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Result for tests.py:")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Result for ../main.py:")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Result for nonexistent.py:")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Result for lorem.txt:")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()