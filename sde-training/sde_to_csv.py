import csv
import re

def parse_sde_mix_out(file_path):
    mnemonics = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Use regex to match lines with mnemonic and count
            match = re.match(r'^\s*([A-Za-z0-9_]+)\s+(\d+)', line)
            if match:
                mnemonic = match.group(1).lower()  # Convert mnemonic to lowercase
                count = int(match.group(2))
                if mnemonic in mnemonics:
                    mnemonics[mnemonic] += count
                else:
                    mnemonics[mnemonic] = count
    return mnemonics

def write_to_csv(mnemonics, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Mnemonic', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Sort mnemonics by count in descending order
        sorted_mnemonics = sorted(mnemonics.items(), key=lambda item: item[1], reverse=True)
        for mnemonic, count in sorted_mnemonics:
            writer.writerow({'Mnemonic': mnemonic, 'Count': count})

def main():
    input_file = 'sde-mix-out.txt'
    output_file = 'mnemonics_counts.csv'
    mnemonics = parse_sde_mix_out(input_file)
    write_to_csv(mnemonics, output_file)
    print(f"CSV file '{output_file}' has been created successfully.")

if __name__ == "__main__":
    main()

