import pandas as pd
import itables
import ipywidgets as ipw
import os
from . import  DDIR

files = [("Health Care Quality Indicators", "HCQI.csv"), 
         ("Health Care Resources", "REAC.csv"), 
         ("Non-Medical Determinants of Health","LVNG.csv"), 
         ("Health Care Utilization", "PROC.csv")]

data = {f[0]: pd.read_csv(os.path.join(DDIR, f[1])) for f in files}

def getCountries(data):
    b = [d.loc[:, "Country"] for d in data.values()]
    
    tmp = list(set([bbb for bb in b for bbb in bb] ))
    tmp.sort()
    return tmp

em_table_out = ipw.Output()

@em_table_out.capture(clear_output=True)
def view_table(event):
    tmp = data[cat.value]
    itables.show(tmp[tmp.Country.isin(cs.value)])

cs = ipw.SelectMultiple(options=getCountries(data), value=['Australia'], description="Countries")
cat = ipw.Select(options=data.keys(), value = "Health Care Quality Indicators", description="Data Set")

cs.observe(view_table, names="value", type="change")
cat.observe(view_table, names="value", type="change")

def get_case_explorer():
    return ipw.VBox([ipw.HBox([cs, cat]), em_table_out], layout=ipw.Layout(width="100%"))
