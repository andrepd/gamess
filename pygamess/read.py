import sys

res=tuple(open(sys.argv[1],"r"))
lines=[]

if "geometry" in sys.argv:
    for i in range(len(res)):
	if "EQUILIBRIUM GEOMETRY LOCATED" in res[i]:
	    j=i
	    while "MOLECULAR ORBITALS" not in res[j]:
		lines.append(res[j])
		j+=1
	    break

if "energy" in sys.argv:
    for i in range(len(res)):
	if "ENERGY COMPONENTS" in res[i]:
	    j=i
	    while "MULLIKEN AND LOWDIN POPULATION ANALYSES" not in res[j]:
		lines.append(res[j])
		j+=1
	    break
if "cc" in sys.argv:
    for i in range(len(res)):
	if "SUMMARY OF RESULTS" in res[i]:
	    j=i
	    while "THE FOLLOWING METHOD AND ENERGY" not in res[j]:
		lines.append(res[j])
		j+=1
	    break


for i in lines:
    print i,
