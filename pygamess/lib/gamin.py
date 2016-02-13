class gamin:
    def __init__(self,inname):
	self.inname=inname
    
    def Basis(self):
	f=open(self.inname,"r")
	label="Basis"
	stringbasis=0
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		stringbasis=istrp[len(label)+1:]
	f.close()
	basis=stringbasis.split("/")
	return basis

    def CalculationMode(self):
	f=open(self.inname,"r")
	label="CalculationMode"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def Theory(self):
	f=open(self.inname,"r")
	label="Theory"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
   
    def Shell(self):
	f=open(self.inname,"r")
	label="Shell"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close() 
    
    def Coordinates(self):
	f=open(self.inname,"r")
	startlabel="%Coordinates"
	endlabel="%"
	linestart=0
	lineend=0
	atoms=[]
	fread=f.readlines()
	for i in range(len(fread)):
	    istrp=fread[i].strip()
	    if istrp[0:len(startlabel)]==startlabel:
		linestart=i
	    if istrp[0:len(endlabel)]==endlabel:
		lineend=i
	
	for i in range(linestart+1,lineend):
	    if(fread[i].strip()!=""):
		atoms.append(fread[i].strip())
	f.close()
	return atoms
    
    def MoleculeCharge(self):
	f=open(self.inname,"r")
	label="MoleculeCharge"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def Multiplicity(self):
	f=open(self.inname,"r")
	label="Multiplicity"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def MaxSCFiter(self):
	f=open(self.inname,"r")
	label="MaxSCFiter"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def DirectSCF(self):
	f=open(self.inname,"r")
	label="DirectSCF"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def Units(self):
	f=open(self.inname,"r")
	label="Units"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()

    def XCFunctional(self):
	f=open(self.inname,"r")
	label="XCFunctional"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def DiffSP(self):
	f=open(self.inname,"r")
	label="DiffSP"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def DiffS(self):
	f=open(self.inname,"r")
	label="DiffS"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def NDFunc(self):
	f=open(self.inname,"r")
	label="NDFunc"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def NPFunc(self):
	f=open(self.inname,"r")
	label="NPFunc"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def NFFunc(self):
	f=open(self.inname,"r")
	label="NFFunc"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def HessMethod(self):
	f=open(self.inname,"r")
	label="HessMethod"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def VibAnal(self):
	f=open(self.inname,"r")
	label="VibAnal"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def OptStepSize(self):
	f=open(self.inname,"r")
	label="OptStepSize"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def NOptStep(self):
	f=open(self.inname,"r")
	label="NOptStep"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
    
    def NumericalGrad(self):
	f=open(self.inname,"r")
	label="NumericalGrad"
	for i in f.readlines():
	    istrp=i.strip()
	    if istrp[0:len(label)]==label:
		return istrp[len(label)+1:]
	f.close()
