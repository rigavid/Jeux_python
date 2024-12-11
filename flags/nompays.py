import os, pycountry as pc

langue = "fr"

## TODO ## Fais aussi prendre en compte les keywords à afficher à l'écran

try:
    with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{langue}.txt", "r", encoding="utf8") as file: infos = eval(file.read().replace("\n", ""))
except: infos = {"title":"Flags of the world","flags":{},"buttons":[]}

end = False
for d in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/"):
    if not (key:=d[:-4:]) in [i for i in infos["flags"]]:
        try:
            try: nom = pc.countries.get(alpha_2=key).name
            except: print(f"Le pays '{key}' n'est pas reconnu "); continue
            if (val:="".join(i for i in input(f"{nom}: ") if i.lower() in " ,abcdefghijklmnopqrstuvwxyz-\\")) != "-":
                if val != "":
                    infos["flags"][key] = val.replace("-","").split(",")
        except KeyboardInterrupt: end=True; break
        except Exception as e: print(e)

if not end:
    for d in os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeauxUS/")+os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeauxAutres/"):
        if not (key:=d[:-4:]) in [i for i in infos["flags"]]:
            try:
                if (val:="".join(i for i in input(f"{key}: ") if i.lower() in " ,abcdefghijklmnopqrstuvwxyz-\\")) != "-":
                    if val != "":
                        infos["flags"][key] = val.replace("-","").split(",")
            except KeyboardInterrupt: break
            except Exception as e: print(e)

ind = list(infos["flags"].keys()); ind.sort()
infos["flags"] = {k:infos["flags"][k] for k in ind}
print(" "*100, end="\r")
s = f"{"{"}\n\t'title': '{infos["title"]}',\n\t'flags': {"{"}\n\t\t{",\n\t\t".join(f"'{k}': \"{infos["flags"][k]}\"" for k in infos["flags"])}\n\t{"}"},\n\t'buttons': [\n\t\t{",\n\t\t".join(f"'{v}'" for v in infos["buttons"])}\n\t]\n{"}"}"
with open("/".join(i for i in __file__.split("/")[:-1:])+f"/langues/{langue}.txt", "w", encoding="utf8") as file: file.write(s)