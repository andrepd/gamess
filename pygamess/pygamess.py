import sys
import os
sys.path.append('./lib')
sys.path.append('./data')
from gamin import gamin
from basis_list import basis_list

if(len(sys.argv)!=3):
    print "Usage: python "+sys.argv[0]+" infile.pygam outfile.inp"
    sys.exit()

test=gamin(sys.argv[1])

#DFT
functional={}
functionaldata=open("./data/xcfunctionals.data","r")
functionalread=functionaldata.readlines()
for i in range(len(functionalread)):
    if "#" not in functionalread[i] and functionalread[i]!='\n':
	ispl=functionalread[i].strip().split("\t")
	functional.update({ispl[0]:ispl[1]})
#--------------------------------------

#SCFTYP
shell={"rhf":"SCFTYP=RHF ",
        "rohf":"SCFTYP=ROHF ",
	"uhf":"SCFTYP=UHF "
}
#--------------------

#RUNTYP
calcmode={"gs":"RUNTYP=ENERGY ",
          "go":"RUNTYP=OPTIMIZE ",
          "hessian":"RUNTYP=HESSIAN "
}
#-------------------

#CC
theory={"mp2":"MPLEVL=2 ",
    "dft":"DFTTYP=",
    "lccd":"CCTYP=LCCD ",
    "ccsd":"CCTYP=CCSD ",
    "ccd":"CCTYP=CCD ",
    "ccsdt":"CCTYP=CCSD(T) " 
}
#----------------------------

#Units
Units={"bohr":"BOHR",
}
#-------------------

#SCF
if test.DirectSCF():
    if test.DirectSCF()=="yes":
	scf=" $SCF DIRSCF=.TRUE. $END\n"
    elif test.DirectSCF()=="no":
	pass
    else:
	sys.exit("Choose yes or no for Direct SCF!")

#Mult Basis
basislist=[]
for i in range(len(test.Basis())):
    basis=" $BASIS "
    place=0
    if "#" in test.Basis()[i]:
	place=test.Basis()[i].find("#")
    
    if test.Basis()[i][:place] in basis_list and place!=0:
	basis+=basis_list[test.Basis()[i][:place]]
    elif test.Basis()[i] in basis_list and place==0:
	basis+=basis_list[test.Basis()[i]]
    else:
	sys.exit("That basis set does not exist in the database!")
    
    if "#" in test.Basis()[i]:
	if test.Basis()[i].count("+")==1:
	    basis+="DIFFSP=.TRUE. "
	if test.Basis()[i].count("+")==2:
	    basis+="DIFFS=.TRUE. "

	if "p" in test.Basis()[i]:
	    basis+="NPFUNC="+test.Basis()[i][test.Basis()[i].find("p")-1]+" "
	if "d" in test.Basis()[i]:
	    basis+="NDFUNC="+test.Basis()[i][test.Basis()[i].find("d")-1]+" "
	if "f" in test.Basis()[i]:
	    basis+="NFFUNC="+test.Basis()[i][test.Basis()[i].find("f")-1]+" "

    basis+="$END\n"
    basislist.append(basis)
#------------------------------

#$CONTRL
control=" $CONTRL "

if test.Shell() in shell:
    control+=shell[test.Shell()]
else:
    sys.exit("Choose either rhf, rohf or uhf!")

if test.CalculationMode() in calcmode:
    control+=calcmode[test.CalculationMode()]
else:
    sys.exit("That calculation mode does not exist!")

if test.MoleculeCharge():
    control+="ICHARG="+test.MoleculeCharge()+" "

if test.Multiplicity():
    control+="MULT="+test.Multiplicity()+" "

if test.MaxSCFiter():
    if test.MaxSCFiter()=="30":
	pass
    else:
	control+="MAXIT="+test.MaxSCFiter()+" "

if test.Units():
    if test.Units()=="angstrom":
	pass
    if test.Units()=="bohr":
	control+="UNITS="+test.Units()+" "
if test.NumericalGrad():
    if test.NumericalGrad()=="yes":
	control+="NUMGRD=.TRUE. "
    elif test.NumericalGrad()=="no":
	pass
    
if test.Theory():
    if test.Theory()=="dft":
	control+=theory[test.Theory()]
	if test.XCFunctional():
	    control+=functional[test.XCFunctional()]+" "
	else:
	    sys.exit("To use DFT you have to choose a XC functional!")
    
    elif test.Theory() in theory:
	control+=theory[test.Theory()]+" "
    else:
	sys.exit("Choose a valid theory level (mp2,ccd,dft...)!")

controllist=[]
controlclean=control
for i in range(len(test.Basis())):
    control=controlclean
    if "cc_" in test.Basis()[i]:
	control+="ISPHER=1 "
    control+="$END\n"
    controllist.append(control)
#---------------------------------------

#HESSIAN
if test.CalculationMode()=="hessian":
    hessian=" $FORCE "
    if test.HessMethod():
	if test.HessMethod()=="analytic":
	    hessian+="METHOD=ANALYTIC "
	elif test.HessMethod()=="numeric":
	    hessian+="METHOD=SEMINUM "
	else:
	    sys.exit("Choose either analytic or numeric method!")
    
    if test.VibAnal():
	if test.VibAnal()=="yes":
	    hessian+="VIBANL=.TRUE. "
	elif test.HessMethod()=="no":
	    hessian+="VIBANL=.FALSE. "
	else:
	    sys.exit("Choose yes or no for vibrational analysis!")
    hessian+="$END\n"
#----------------------------------------

#Optimization
if test.CalculationMode()=="go":
    statopt=" $STATPT "
    if test.NOptStep():
	if type(int(test.NOptStep())) is int:
	    statopt+="NSTEP="+test.NOptStep()+" "
	else:
	    sys.exit("Choose a number of steps!")
    
    if test.OptStepSize():
	if test.OptStepSize():
	    if type(float(test.OptStepSize())) is float:
		statopt+="OPTTOL="+test.OptStepSize()+" "
	    else:
		sys.exit("Choose a number of steps!")
    statopt+="$END\n"


#$DATA
data=" $DATA\ncomment\nC1\n"
for i in test.Coordinates():
    data+=i
    data+="\n"
data+=" $END\n"
#---------------------------    
for i in range(len(test.Basis())):
    f=open(sys.argv[2]+"_"+test.Basis()[i]+".inp","w")
    f.write(basislist[i])
    f.write(controllist[i])
    f.write(" $SYSTEM TIMLIM=525600 MEMORY=524288000 MEMDDI=125 $END\n")
    if test.DirectSCF():
	f.write(scf)
    if test.CalculationMode()=="hessian":
	f.write(hessian)
    if test.NOptStep() or test.OptStepSize():
	f.write(statopt)
    f.write(data)
    f.close()

for i in range(len(test.Basis())):
    os.system("python gamessrun.py "+sys.argv[2]+"_"+test.Basis()[i]+".inp")
for i in range(len(test.Basis())):
    os.system("python read.py "+sys.argv[2]+"_"+test.Basis()[i]\
	    +".log energy cc geometry > "+sys.argv[2]+"_"+test.Basis()[i]+".res")
os.system("rm *.inp")
