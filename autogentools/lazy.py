'''
def name_thing(par1, par2, parn):

becomes

@APP.route("name/thing", method = ["POST"])
def name_thing():
    server.name_thing(request.form["par1"], request.form["par2"], request.form["par3"])
'''


f = open("./functions.txt", "r")
w = open("./win.txt", "w")
for line in f:
    start = 4
    end = line.find("_")

    name1 = line[start:end]
    start = end + 1
    end = line.find("(", start+1)
    name2 = line[start:end]
    
    args = []
    start = end+1
    end = line.find(",", start+1)
    while end != -1:
        args.append(f'request.form["{line[start:end].strip()}"]')
        start = end+1
        end = line.find(",", start+1)
    end = line.find(")", start+1)
    args.append(f'request.form["{line[start:end].strip()}"]')
    w.write(f'@APP.route("{name1}/{name2}", match = ["POST"])\n')
    w.write(f'def {name1}_{name2}():\n')
    w.write(f'\treturn server.{name1}_{name2}({", ".join(args)})\n')
    w.write('\n')




