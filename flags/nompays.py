import os, pycountry as pc
with open("/".join(i for i in __file__.split("/")[:-1:])+"/langues/fr.txt", "r", encoding="utf8") as file:
    infos = eval(file.read().replace("\n", ""))

lst = os.listdir("/".join(i for i in __file__.split("/")[:-1:])+"/drapeaux/")
lst.sort()
for d in lst:
    if not (key:=d[:-4:]) in [i for i in infos["flags"]]:
        try:
            try:
                nom = pc.countries.get(alpha_2=key).name
            except:
                print(f"Le pays '{key}' n'est pas reconnu ")
                continue
            val = "".join(i for i in input(f"{nom}: ") if i.lower() in ",abcdefghijklmnopqrstuvwxyz-")
            if val != "-":
                infos["flags"][key] = set(list(val.replace("-","").split(",")))
        except KeyboardInterrupt: break
        except Exception as e:
            print(e)

print(" "*100, end="\r")

s = f"{"{"}\n\t'title': '{infos["title"]}',\n\t'flags': {"{"}\n\t\t{",\n\t\t".join(f"'{k}': \"{infos["flags"][k]}\"" for k in infos["flags"])}\n\t{"}"},\n\t'buttons': [\n\t\t{",\n\t\t".join(f"'{v}'" for v in infos["buttons"])}\n\t]\n{"}"}"

with open("/".join(i for i in __file__.split("/")[:-1:])+"/langues/fr.txt", "w", encoding="utf8") as file:
    file.write(s)