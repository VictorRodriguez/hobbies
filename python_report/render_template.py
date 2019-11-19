import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.txt"
template = templateEnv.get_template(TEMPLATE_FILE)

d = {}
d["interest_rate"] = 2
d["df"] = {'A' : '1','B': '2', 'C':'3', 'D':'4'}
outputText = template.render(dict_item=d['df'],\
    interest_rate=d['interest_rate'])
html_file = open('report.html', 'w')
html_file.write(outputText)
html_file.close()
