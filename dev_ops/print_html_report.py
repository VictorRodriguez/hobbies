"""Print HTML report."""
import json
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
   
    data = {}
    pkg = 'helloworld'
    data[pkg] = []

    data[pkg].append({
        'clr_status': "Ok",
        'build_status': "Ok",
        'qa_status': "Ok",
        'last_commit': "1234asda1 <vrodri3>"
        })

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    with open('data.json') as json_file:
        data_json = json.load(json_file)
        print_html_doc(data_json)


if __name__ == '__main__':
    main()
