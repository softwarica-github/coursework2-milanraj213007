import codecs

input_file_path = input("Path to wordlist: ")
output_file_path = "Fixed-" + input_file_path

# Count the total number of lines in the input file
with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
    total_lines = sum(1 for line in f)
    f.close()

# Open the input and output files
with codecs.open(input_file_path, 'r', 'utf-8', errors='ignore') as input_file, \
     codecs.open(output_file_path, 'w', 'utf-8') as output_file:

    # Iterate over each line in the input file and write to the output file
    for i, line in enumerate(input_file, 1):
        # Check if the line contains any invalid UTF-8 characters
        try:
            line.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            # If the line contains non-valid UTF-8 characters, skip it
            continue

        # If the line is valid UTF-8, write it to the output file
        output_file.write(line)

        # Print the current line number and the total number of lines
        print(f"Currently fixing line: {i} / {total_lines}", end='\r', flush=True)
        
print(f"\nOutput to: {output_file_path}")