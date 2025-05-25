import argparse

def calc_inc(x: int):
    y = x + 1
    return y

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Example with argparse")
  parser.add_argument("number", type=int, help="Your input")

  args = parser.parse_args()
  x1= calc_inc(args.number)
  print("New number = ",x1) 