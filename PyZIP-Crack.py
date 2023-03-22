import itertools, argparse, zipfile, chardet, signal, sys, threading

# Define a global variable to signal the password cracking loop to stop
stop_event = threading.Event()

# Define a signal handler to catch the SIGINT signal
def signal_handler(sig, frame):
    global stop_event
    print('\nExited')
    stop_event.set()
    sys.exit()

def extract_zip(zip_file, start_length, max_length, wordlist):
    # Loop through all possible password combinations
    charset = "abcdefghijklmnopqrstuvwxyz"
    
    if wordlist:
        # Detect the encoding of the wordlist file
        with open(wordlist, 'rb') as f:
            passwords = f.read().splitlines()
            
        # Filter the passwords list to only include passwords within the desired length range
        passwords = [password for password in passwords if start_length <= len(password) <= max_length]
    else:
        # Generate all possible password combinations
        passwords = (''.join(password) for length in range(start_length, max_length+1) for password in itertools.product(charset, repeat=length))

    for password in passwords:
        ''' Set comments according to which print method you'd like '''
        if stop_event.is_set():
            return None
            
        try:
            password = password.decode('utf-8')
        except:
            password = password
        
        print("\rTrying password: {:<{}}".format(password[:max_length], max_length), end="", flush=True)

        # Attempt to extract the ZIP file with the current password
        try:
            zip_file.extractall(pwd=password.encode())
            return password
        except:
            pass

    # If no password was found, return None
    return None

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract a ZIP file using a brute-force attack.')
    parser.add_argument('-zip', type=str, help='The path to the ZIP file.')
    parser.add_argument('-min', type=int, default=1, help='The starting length of the password to try.')
    parser.add_argument('-max', type=int, default=8, help='The maximum length of the password to try.')
    parser.add_argument('-wordlist', type=str, help='The path to a file containing a list of possible passwords.')
    args = parser.parse_args()   
    
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Open the ZIP file
    try:
        zip_file = zipfile.ZipFile(args.zip)
    except Exception as e:
        parser.print_help()
        sys.exit()

    # Extract the ZIP file using a brute-force attack
    password = extract_zip(zip_file, args.min, args.max, args.wordlist)

    if password is None:
        print('\nPassword not found.')
    else:
        print('\nPassword found:', password)
