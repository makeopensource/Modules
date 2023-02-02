from flask import Flask, render_template, request, make_response, send_file
from jinja2.exceptions import TemplateNotFound
import toml
import json

from plugins import MarkdownExtension


def read_toml(filename):
    with open(filename, "r") as f:
        return toml.loads(f.read())

def add_unlocked(response, module, old_unlocked = None):
    unlocked = old_unlocked or json.loads(
        request.cookies.get("unlocked", "[]")
    )
    print(f"Add unlocked: {unlocked}")
    if module not in unlocked:
        unlocked.append(module)

    print(unlocked)
    response.set_cookie("unlocked", json.dumps(unlocked))
    return unlocked
    
def get_unlocked():
    return [0] + json.loads(
        request.cookies.get("unlocked", "[]")
    )


app = Flask(__name__)
app.jinja_env.add_extension(MarkdownExtension)

config = read_toml("config.toml")
module_map = {x["url"]: x for x in config["module"]}


@app.route("/")
def hello_world():
    response = render_template("index.html", config=config, unlocked=get_unlocked())
    return response


@app.route("/module/<module_url>")
def module_view(module_url):
    module = module_map[module_url]
    module_id = module["id"]
    module_name = module["name"]

    if module_id != 0 and module_id not in get_unlocked():
        return f"Module \"{module_name}\" not unlocked"

    try:
        response = make_response(render_template(f"{module_url}.html", complete=module_id in get_unlocked()))
   
    except TemplateNotFound:
        response = make_response(f"Module \"{module_name}\" not yet implemented")

    unlocked = add_unlocked(response, module_id)

    for next_module_id in module.get("next", []):
        add_unlocked(response, next_module_id, unlocked)

    return response

 
@app.route("/file/<filename>")
def file_view(filename):
    return send_file(f"file/{filename}", as_attachment=True)


