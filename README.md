# ZIP-Password-Cracker
A simple Python script to crack ZIP Passwords using fcrackzip.  

The script uses a mixed method of both dictionary and bruteforce attacking, as such it requires a wordlist file. But I will provide one in the repo.

### Usage
```cmd
usage: PyZIP-Crack.py [-h] -z ZIPFILE -l WORDLIST [-m MIN_LENGTH] [-x MAX_LENGTH]
PyZIP-Crack.py: error: the following arguments are required: -z/--zipfile, -l/--wordlist
```

#### Example Usage

```cmd
python PyZIP-Crack.py -z example.zip -l rockyou.txt
```
if the `-m` / `x` fields are left empty they are set to a default of `1` and `8`, meaning it starts at a length of 1 character passwords, and builds its way up to 8. You can change those fileds with the `-m` and `-x` arguments like so.

```cmd
python PyZIP-Crack.py -z example.zip -l rockyou.txt -m 2 -x 5
```
That would run the script with a minimum length of 2 and a maximum length of 5
