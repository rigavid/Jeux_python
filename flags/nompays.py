import os, pycountry as pc
import time

langue = "fr"

## TODO ## Fais prendre aussi en compte les keywords à afficher à l'écran

try:
    with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{langue}.txt", "r", encoding="utf8") as file: infos = eval(file.read().replace("\n", ""))
except: infos = {"title":"Flags of the world","flags":{},"buttons":[]}

def printe(*args):
    print(" "*100, "\r", *args, sep="", end="\r")
    time.sleep(0.05)

def set_flags_name(path, infos):
    printe(f"scan {path.split("/")[-1]}")
    for flag in os.listdir(path):
        if os.path.isdir(dir:=f"{path}/{flag}"):
            printe(f"cd {flag}")
            if set_flags_name(dir, infos): return True
            printe("cd ..")
        elif not (key:=flag[:-4:]) in infos["flags"].keys():
            try:
                try: nom = pc.countries.get(alpha_2=key).name
                except: nom = key
                if (val:="".join(i for i in input(f"\n{nom}: ") if i.lower() in " ,12345678909.abcdefghijklmnopqrstuvwxyz-\\()")) != "-":
                    if val != "":
                        infos["flags"][key] = val.replace("-","").split(",")
            except KeyboardInterrupt: return True
            except Exception as e: print(e)
    printe(f"end of {path.split("/")[-1]}")

loc_p = "/".join(i for i in __file__.split("/")[:-1:])
for path in [f"{loc_p}/drapeaux", f"{loc_p}/drapeauxAutres"]:
    if set_flags_name(path, infos): break

if not (oneline:=False):
    ind = list(infos["flags"].keys()); ind.sort()
    infos["flags"] = {k:infos["flags"][k] for k in ind}
    print(" "*100, end="\r")
    s = f"{"{"}\n\t'title': '{infos["title"]}',\n\t'flags': {"{"}\n\t\t{",\n\t\t".join(f"'{k}': \"{infos["flags"][k]}\"" for k in infos["flags"])}\n\t{"}"},\n\t'buttons': [\n\t\t{",\n\t\t".join(f"'{v}'" for v in infos["buttons"])}\n\t]\n{"}"}"
    with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{langue}.txt", "w", encoding="utf8") as file: file.write(s)
else:
    with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{langue}.txt", "w", encoding="utf8") as file:
        file.write(str(infos))