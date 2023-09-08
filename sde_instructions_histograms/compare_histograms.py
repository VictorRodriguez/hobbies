import sys

# Function to read a file and store mnemonics and counts in a dictionary
def read_file(filename):
    mnemonic_count_dict = {}
    with open(filename, 'r') as file:
        # Skip the header line
        next(file)
        for line in file:
            mnemonic, count = line.strip().split(',')
            mnemonic_count_dict[mnemonic] = float(count)
    return mnemonic_count_dict

# Function to find common mnemonics and calculate the ratio of difference
def find_common_mnemonics(file1_dict, file2_dict):
    common_mnemonics = set(file1_dict.keys()) & set(file2_dict.keys())
    for mnemonic in common_mnemonics:
        count1 = file1_dict[mnemonic]
        count2 = file2_dict[mnemonic]

        if count1 == 0 and count2 == 0:
            print(f"Mnemonic: {mnemonic}, Counts in both files are zero.")
        elif count2 == 0:
            print(f"Mnemonic: {mnemonic}, Count in {sys.argv[2]} is zero.")
        else:
            ratio = count1 / count2
            if count1 > count2:
                print(f"Mnemonic: {mnemonic}, Count in {sys.argv[1]} is {ratio:.2f} times more than in {sys.argv[2]}")
            elif count1 < count2:
                print(f"Mnemonic: {mnemonic}, Count in {sys.argv[2]} is {1/ratio:.2f} times more than in {sys.argv[1]}")
            else:
                print(f"Mnemonic: {mnemonic}, Counts in both files are equal")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py file1.txt file2.txt")
    else:
        file1_path = sys.argv[1]
        file2_path = sys.argv[2]

        file1_dict = read_file(file1_path)
        file2_dict = read_file(file2_path)

        find_common_mnemonics(file1_dict, file2_dict)

