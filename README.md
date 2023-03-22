# ZIP-Password-Cracker
A simple Python script to crack ZIP Passwords

The script uses a mask attack which encompasses both bruteforce and dictionary attacks. While a wordlist is optional, if one is not provided it will default to the bruteforce method which can take a lot longer. You can find an extensive wordlist [here](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)

### Usage
```
usage: PyCrack-ZIP.py [-h] [-zip ZIP] [-min MIN] [-max MAX] [-wordlist WORDLIST]

Extract a ZIP file using a brute-force attack.

optional arguments:
  -h, --help          show this help message and exit
  -zip ZIP            The path to the ZIP file.
  -min MIN            The starting length of the password to try.
  -max MAX            The maximum length of the password to try.
  -wordlist WORDLIST  The path to a file containing a list of possible passwords.
```

#### Example Usage

```
python PyZIP-Crack.py -zip Example2.zip -wordlist rockyou.txt
```
if the `-min` / `-max` fields are left empty they are set to a default of `1` and `8`, meaning it starts at a length of 1 character passwords, and builds its way up to 8. You can change those fileds with the `-min` and `-max` arguments like so.

```
python PyZIP-Crack.py -zip Example2.zip -min 2 -max 5 -wordlist rockyou.txt
```
That would run the script with a minimum length of 2 and a maximum length of 5
