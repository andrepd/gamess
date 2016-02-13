import sys

res=tuple(open(sys.argv[1],"r"))
start=0
end=0
for i in range(len(res)):
    if "EQUILIBRIUM GEOMETRY LOCATED" in res[i]:
	start=i
    if "MOLECULAR ORBITALS" in res[i]:
	end=i
for i in range(start,end):
    print res[i].strip()
