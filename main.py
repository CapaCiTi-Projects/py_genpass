from argparse import ArgumentParser
import pyperclip
import random
import string
import sys
import time

def print_animated(text, multiline=False, delay=0.05, base=None):
	if multiline:
		if base is not None:
			for line in text:
				print(base * len(line))
			print("\r"*len(text), end="")

		for line in text:
			for char in line:
				system.stdout.write(char)
				sys.stdout.flush()

				time.sleep(delay)
	else:
		if base is not None:
			print(base * len(text), end="\r")

		for char in text:
			sys.stdout.write(char)
			sys.stdout.flush()

			time.sleep(delay)
	sys.stdout.write("\n")

def get_random_password(chars, length=12):
	random.shuffle(chars)
	res = ""

	for _ in range(length):
		idx = random.randrange(len(chars))
		res += chars[idx]

	return res

def setup_argparser():
	parser = ArgumentParser(description="Generate a random password based on supplied values.")

	parser.add_argument("-l", "--length", type=int, help="The length of the outputted password.", default=12)
	parser.add_argument("-uc", "--exclude-uppercase", action="store_true", help="Exclude uppercase letters in the password.")
	parser.add_argument("-lc", "--exclude-lowercase", action="store_true", help="Exclude lowercase letters in the password.")
	parser.add_argument("-d", "--exclude-digits", action="store_true", help="Exclude digits in the password.")
	parser.add_argument("-s", "--exclude-special", action="store_true", help="Exclude special characters in the password.")
	parser.add_argument("-c", "--count", type=int, help="The number of passwords to generate.", default=1)
	parser.add_argument("--no-anim", action="store_true", help="Use to disable text animations in output.")

	return parser.parse_args()

def print_intro(speed=50):
	speed = 1 / speed
	print("Hello and welcome to this simple Python Password Generator")
	print("You can call me GenPass, and I'll do my utmost to give you a great experience today.")
	print("")

def get_start_int(val, default=-1):
	"""Function to see if the supplied val is an integer or starts with an integer, if so return that integer, otherwise return default."""
	match = re.search("^\d+", val)
	return int(match.group()) if match is not None else default

def get_yes_no_bool(val, default=False):
	val = val.lower()
	if val in ["yes", "y", "1", "true", "t"]:
		return True
	elif val in ["no", "n", "0", "false", "f"]:
		return False
	else:
		return default

def main():
	args = setup_argparser()
	print_intro()

	valid_chars = ""

	if not args.exclude_uppercase:
		valid_chars += string.ascii_uppercase
	if not args.exclude_lowercase:
		valid_chars += string.ascii_lowercase
	if not args.exclude_digits:
		valid_chars += string.digits
	if not args.exclude_special:
		valid_chars += string.punctuation
	valid_chars = list(valid_chars)

	passwords = []

	for num in range(args.count):
		pword = get_random_password(valid_chars, length=args.length)
		passwords.append(pword)
		text = str(num+1).rjust(len(str(args.count)), " ") + ". " + pword

		if args.no_anim:
			print(text)
		else:
			print_animated(text, base=".")

	print("")
	should_clipboard =get_yes_no_bool(input("Should I save a password to the clipboard? [Yes|no] "))

	if should_clipboard:
		if args.count > 1:
			save_idx = get_start_int(input(f"Then enter the number of that password and I'll do it... [1-{args.count}]"))

			if 0 < save_idx <= args.count:
				pyperclip.copy(passwords[save_idx])
				print("Copy successful. :)")
			else:
				print("Copy failed because the wrong value was entered. Sorry. :(")
		else:
			pyperclip.copy(passwords[0])
			print("Copy successful. :)")
	print("Have a great further.")


if __name__ == "__main__":
	# Run the program logic.
	main()
