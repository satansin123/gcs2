
file = open("cansat_2023_simp.txt","r")
simp1 = file.readlines()
simp=[]
for line in simp1:
        if line[0] !="#":
                simp.append(line.strip('\n'))
while("" in simp):
        simp.remove("")

simp = [sub.replace('$', '1062') for sub in simp]

print(simp)