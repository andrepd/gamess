import os
import sys

name=sys.argv[1]
point=name.find(".")
namecrop=name[:point]
comm="rungms "+namecrop+".inp | tee "+namecrop+".log"
os.system(comm)
os.system("rm *.dat")
os.system("rm *.F*")
