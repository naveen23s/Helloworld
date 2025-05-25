#2
import argparse

parser = argparse.ArgumentParser(description="Example with argparse")
parser.add_argument("name", help="Your name")
parser.add_argument("age", type=int, help="Your age")

args = parser.parse_args()

print(f"Hello {args.name}, you are {args.age} years old!")