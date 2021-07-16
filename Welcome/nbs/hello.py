import ipywidgets as ipw
import subprocess
subprocess.run(["python3", "-m", "pip", "install", "google-translate.py"])
from google_translate_py import Translator

def f1(b):
    nm = name.value
    m = f"Hello, {nm}! Welcome to the Digital Transformation of Health, July 2021."
    try:
        tran = Translator()
        rslt = tran.translate(m, "", lc.value)
        msg.value = rslt
    except Exception as error:
        print(error)
        msg.value = f"Hello, {nm}! I'm sorry that the selected translation failed. Please try again."

name = ipw.Text(value='', placeholder="Type your name")
msg = ipw.Label(value="")
sub = ipw.Button(description="Submit")
sub.on_click(f1)
lc = ipw.Dropdown()

def create_welcome(languages=None):
    if languages == None:
        languages = [("English","en"), ("Spanish","es"), ("Chinese","zh"), 
                     ("Korean","ko"), ("Hindi","hi"), ("Persian","fa"), ("Arabic","ar")]
    lc.options = languages
    lc.description = "Choose a language"
    b = ipw.VBox([name, lc, sub, msg])
    return b
