import csv
import re
import argparse

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
    parser = argparse.ArgumentParser(description='Process an SDE mix output file.')
    parser.add_argument('input_file', help='Path to the SDE mix output file')
    parser.add_argument('-o', '--output', default='mnemonics_counts.csv', help='Output CSV file name (default: mnemonics_counts.csv)')

    args = parser.parse_args()

    mnemonics = parse_sde_mix_out(args.input_file)
    write_to_csv(mnemonics, args.output)
    print(f"CSV file '{args.output}' has been created successfully.")

if __name__ == "__main__":
    main()

