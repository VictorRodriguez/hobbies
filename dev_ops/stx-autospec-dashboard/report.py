"""Print HTML report."""
import csv
import os
from jinja2 import Environment, FileSystemLoader

def print_html_doc(dictionary_data):
    """Generate the html index."""
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').
          render(data=dictionary_data),
          file=open("index.html", "w"))

def main():

    outfile = '/tmp/output.csv'
    data = {}

    with open(outfile, mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            data[rows[0]] = {'autospec_status':rows[1]}

    print_html_doc(data)
    print(data)

if __name__ == '__main__':
    main()
