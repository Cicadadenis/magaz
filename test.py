def rm():
    add_tex = open("tex.txt", "r").readlines()
    ff = []
    for x in add_tex:
        ff.append(x.split("\n")[0])
    print(ff)


    x = input("Введи id для удаления:   ")
    ff.remove(x)
    with open("tex.txt", "w") as r:
        for x in ff:
            r.write(f"{x}\n")
rm()