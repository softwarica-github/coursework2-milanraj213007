import argparse
import subprocess
import sys

# Default values
zipfile = ""
wordlist = ""
min_length = 1
max_length = 8

# Usage function
def usage():
    print(f"Usage: {sys.argv[0]} [-z <zipfile>] [-l <wordlist>] [-m <min_length>] [-x <max_length>]")
    print("    -z <zipfile>: Zip file to crack (required)")
    print("    -l <wordlist>: Password wordlist file (required)")
    print("    -m <min_length>: Minimum password length (default: 1)")
    print("    -x <max_length>: Maximum password length (default: 8)")
    sys.exit(1)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zipfile", required=True, help="Zip file to crack")
parser.add_argument("-l", "--wordlist", required=True, help="Password wordlist file")
parser.add_argument("-m", "--min_length", type=int, default=min_length, help="Minimum password length (default: 2)")
parser.add_argument("-x", "--max_length", type=int, default=max_length, help="Maximum password length (default: 6)")
args = parser.parse_args()

zipfile = args.zipfile
wordlist = args.wordlist
min_length = args.min_length
max_length = args.max_length

# Check if fcrackzip is installed
try:
    subprocess.run(["fcrackzip", "--help"], stdout=subprocess.PIPE, check=True)
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Error: fcrackzip is not installed. Please install it before running this script.")
    sys.exit(1)

# Function to handle password found event
def password_found(password):
    print(f"\nPASSWORD FOUND!!!!: pw == {password}")
    sys.exit(0)

# Loop over password lengths
for length in range(min_length, max_length+1):
    print(f"Trying passwords of length {length}")
    # Run fcrackzip with the current length and wordlist
    # Redirect stderr to stdout and pipe to grep to check if password is found
    result = subprocess.run(["fcrackzip", "-u", "-p", wordlist, "-l", str(length), zipfile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if "PASSWORD FOUND" in result.stdout:
        password = result.stdout.split()[-1]
        password_found(password)
