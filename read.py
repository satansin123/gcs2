
file = open("cansat_2023_simp.txt","r")
simp1 = file.readlines()
simp=[]
for i in simp1:
    if i[0] !="#":
        simp.append(i.strip('\n'))
while("" in simp):
    simp.remove("")

simp = [sub.replace('$', '1062') for sub in simp]


print(simp)