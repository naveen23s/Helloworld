#2
import argparse

def non_numeric_string(value):
    if value.isdigit():
        raise argparse.ArgumentTypeError("Name must be a non-numeric string")
    return value

parser = argparse.ArgumentParser(description="Example with argparse")
parser.add_argument("name", type=non_numeric_string,help="Your name")
parser.add_argument("age", type=int, help="Your age")

args = parser.parse_args()

print(f"Hello {args.name}, you are {args.age} years old!")

