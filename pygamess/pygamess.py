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
    if test.Basis()[i] in basis_list:
	basis+=basis_list[test.Basis()[i]]
    else:
	sys.exit("That basis set does not exist in the database!")
        
    if test.DiffSP():
	if test.DiffSP()=="yes":
	    basis+="DIFFSP=.TRUE. "
	elif test.DiffSP()=="no":
	    pass
	else:
	    sys.exit("Choose yes or no for diffuse SP shells!")
    
    if test.DiffS():
	if test.DiffS()=="yes":
	    basis+="DIFFS=.TRUE. "
	elif test.DiffS()=="no":
	    pass
	else:
	    sys.exit("Choose yes or no for diffuse S shells!")
    
    if test.NPFunc():
	if test.NPFunc() in ["1","2","3"]:
	    basis+="NPFUNC="+test.NPFunc()+" "
	else:
	    sys.exit("Choose beetween 1,2,3 P functions!")
    
    if test.NDFunc():
	if test.NDFunc() in ["1","2","3"]:
	    basis+="NDFUNC="+test.NDFunc()+" "
	else:
	    sys.exit("Choose beetween 1,2,3 D functions!")
    
    if test.NFFunc():
	if test.NFFunc() in ["1","2","3"]:
	    basis+="NFFUNC="+test.NFFunc()+" "
	else:
	    sys.exit("Choose beetween 1,2,3 F functions!")
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
    control+="ICHARGE="+test.MoleculeCharge()+" "

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
os.system("./scripts/makefolder.sh " + sys.argv[2])
for i in range(len(test.Basis())):
    f=open(sys.argv[2]+"_"+test.Basis()[i]+".inp","w")
    f.write(basislist[i])
    f.write(controllist[i])
    if test.DirectSCF():
	f.write(scf)
    if test.CalculationMode()=="hessian":
	f.write(hessian)
    if test.NOptStep() or test.OptStepSize():
	f.write(statopt)
    f.write(data)
    os.system("mv "+sys.argv[2]+"_"+test.Basis()[i]+".inp "+sys.argv[2])
    f.close()

os.system("cd "+sys.argv[2])
os.system("../scripts/gamessrun.sh")
os.system("../scripts/makefolder.sh res")
os.system("mv *.log res")
