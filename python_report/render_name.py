import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "name.txt"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(name='Mark')
print(outputText)
