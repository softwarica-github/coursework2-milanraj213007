import argparse
import itertools
import zipfile

def extract_zip(zip_file, max_length):
    # Loop through all possible password combinations
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=[]{}|/?<>,."
    
    for length in range(1, max_length+1):
        for password in itertools.product(charset, repeat=length):
            password = ''.join(password)
            print('Trying password:', password)

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
    parser.add_argument('-z', type=str, help='The path to the ZIP file.')
    parser.add_argument('-m', type=int, default=10, help='The maximum length of the password to try.')
    args = parser.parse_args()

    # Open the ZIP file
    zip_file = zipfile.ZipFile(args.z)

    # Extract the ZIP file using a brute-force attack
    password = extract_zip(zip_file, args.m)

    if password is None:
        print('Password not found.')
    else:
        print('Password found:', password)
