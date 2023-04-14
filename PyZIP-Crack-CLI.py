import itertools
import argparse
import zipfile
import chardet
import signal
import sys
import threading

# Define a global variable to signal the password cracking loop to stop
stop_event = threading.Event()

# Define a signal handler to catch the SIGINT signal
def signal_handler(sig, frame):
    global stop_event
    print('\nExited')
    stop_event.set()
    sys.exit()

def extract_zip(zip_file, start_length, max_length, charset, wordlist=None):
    # filler to prevent print artifacting
    filler = " " * (max_length // 2) # use // to prevent float values
    
    # Loop through all possible password combinations
    if wordlist:
        with open(wordlist, 'r', errors='ignore') as f:
            passwords = f.read().splitlines()
        
        # Filter the passwords list to only include passwords within the desired length range
        passwords = [password for password in passwords if start_length <= len(password) <= max_length]

        # Print a message indicating that the dict attack is starting
        print("Starting dictionary attack...")

        # Use the wordlist until it is exhausted, then switch to the brute-force attack
        for i, password in enumerate(passwords, start=1):
            if stop_event.is_set():
                return None

            progress = f"Trying password from wordlist: {password} (on: {i} out of: {len(passwords)}){filler}"
            print("\r" + progress, end="", flush=True)

            try:
                zip_file.extractall(pwd=password.encode())
                print('\n\nPassword found:', password)
                print('Total attempts:', i)   # Print the total number of attempts made
                return password
            except Exception:
                pass
        
        print('\nWordlist exhausted, switching to brute-force attack...')

    # Generate all possible password combinations
    passwords = (''.join(password) for length in range(start_length, max_length+1) for password in     itertools.product(charset, repeat=length))

    # Print a message indicating that the brute-force attack is starting
    print("\nStarting brute-force attack...")

    for i, password in enumerate(passwords, start=1):
        if len(password) > max_length:
            break
        
        if stop_event.is_set():
            return None
        
        progress = f"Trying password: {password} (on iteration: {i} of cycle: {len(password)})"
        print("\r" + progress, end="", flush=True)

        # Attempt to extract the ZIP file with the current password
        try:
            zip_file.extractall(pwd=password.encode())
            print('\n\nPassword found:', password)
            print('Total attempts:', i)   # Print the total number of attempts made
            return password
        except Exception:
            global count
            count = i
            pass

    # If no password was found, print the total number of attempts made and return None
    print('\n\nPassword not found.')
    print('Total attempts:', count)
    return None


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract a ZIP file using a brute-force attack.')
    parser.add_argument('-zip', type=str, required=True, help='The path to the ZIP file.')
    parser.add_argument('-min', type=int, default=1, help='The starting length of the password to try.')
    parser.add_argument('-max', type=int, default=8, help='The maximum length of the password to try.')
    parser.add_argument('-wordlist', type=str, help='The path to a file containing a list of possible passwords.')
    parser.add_argument('-charset', type=str, default='abcdefghijklmnopqrstuvwxyz', help='The character set to use for the brute-force attack.')
    args = parser.parse_args()

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Open the ZIP file
    try:
        zip_file = zipfile.ZipFile(args.zip)
    except Exception as e:
        parser.error('Failed to open ZIP file: ' + str(e))

    # Extract the ZIP file using a brute-force attack
    password = extract_zip(zip_file, args.min, args.max, args.charset, args.wordlist)
