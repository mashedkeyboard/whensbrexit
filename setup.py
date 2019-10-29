import fileinput, os, re, shutil, json
from datetime import datetime

print("Build script started")

print("Cleaning old directories")

try:
    shutil.rmtree('public')
except OSError:
    pass

shutil.copytree("static","public")

print("Building main page")

with open("static/api.json", 'r') as apijson:
    api = json.load(apijson)
    ld = datetime.fromisoformat(api['scheduledDateOfLeaving'])
    with fileinput.FileInput("public/index.html", inplace=True) as file:
        for line in file:
            for match in re.findall(r'<!% (.*?) %>', line):
                sub = match.split(".")
                replacement = None

                if sub[0] == "scheduledDateOfLeaving":
                    replacement = ld.strftime("%B %d, %Y at %H:%M")
                elif sub[0] == "extensionStatus":
                    curExt = api["extension"][0]
                    if curExt["formalised"] != True:
                        replacement = "Extension "

                        if curExt["accepted"]:
                            replacement += "accepted, awaiting formalisation,"
                        elif curExt["offered"]:
                            replacement += "offered, awaiting acceptance,"
                        else:
                            replacement += "requested"

                        if curExt["extendDate"]:
                            replacement += " for " + datetime.fromisoformat(curExt["extendDate"]).strftime("%B %d, %Y")
                    else:
                        replacement = "No additional extension currently requested."

                if replacement:
                    line = line.replace('<!% ' + match + ' %>', replacement)
            print(line,end='')
    
print("Build complete")
