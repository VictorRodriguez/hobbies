import csv

# Define the specific string to look for
specific_string = "END_STATIC_STATS"

# Input file name and output CSV file name
input_file_name = "sde-mix-out.txt"
output_csv_name = "sde-mix-out.csv"


# Open the input file for reading and the output CSV file for writing
with open(input_file_name, "r") as input_file, open(
    output_csv_name, "w", newline=""
) as output_csv:

    # Initialize a list to store the lines
    lines_to_write = []

    # Create a CSV writer object
    csv_writer = csv.writer(output_csv, delimiter=",")

    # Flag to indicate if specific_string has been found
    found_specific_string = False

    # Iterate through each line in the input file
    for line in input_file:
        # Check if the specific string is in the line
        if specific_string in line:
            found_specific_string = True
            continue  # Skip this line and start processing from the next line
        # Check if the line starts with '#' or '*'
        if line.startswith("*"):
            continue  # Skip this line
        if line.startswith("#"):
            continue  # Skip this line
        # If the specific string has been found, split the line by spaces and write it to the CSV
        if found_specific_string:
            line = line.strip()  # Remove leading/trailing whitespace
            line_parts = line.split()  # Split the line by spaces
            if len(line_parts) >= 2:
                line_parts[0] = line_parts[0].lower()
                line_parts[1] = int(line_parts[1])
                lines_to_write.append(line_parts)

    # Sort the lines by the second column (index 1)
    sorted_lines = sorted(lines_to_write, key=lambda x: x[1], reverse=True)

    # Create a CSV writer object with a space delimiter
    csv_writer = csv.writer(output_csv, delimiter=",")

    # Write the header
    csv_writer.writerow(["mnemonic", "Count"])

    # Write the sorted lines to the CSV file
    csv_writer.writerows(sorted_lines)

print(f"CSV file '{output_csv_name}' has been created.")
