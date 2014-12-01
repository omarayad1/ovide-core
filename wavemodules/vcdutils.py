import re

def listSigs():
	pass

def parseVCD(file, opt):
	only_sigs = 1 if 'only_sigs' in opt.keys() else 0
	if 'siglist' in opt.keys():
		usigs = {x: 1 for x in opt['siglist']}
		all_sigs = 0
	else:
		all_sigs = 1
	use_stdout = 1 if 'use_stdout' in opt.keys() else 0
	fh = open(file,'r').readlines()
	heir = []
	i = 0
	while i < len(fh):
		line = fh[i]
		if re.search(r"\$enddefinitions \b",line,flags=re.X):
			num_sigs = len(data.keys())
			if only_sigs:
				break
		elif re.search(r"\$timescale \b",line,flags=re.X):
			statement = line
			if not re.search(r"\$end \b",line,flags=re.X):
				ll = line
				j=i
				while not re.search(r"\$end \b", ll, flags=re.X):
					j+=1
					ll = fh[j]
					statement += (' ' + ll)
			mult = calcMult(statement,opt)
		elif re.search(r"\$scope \b",line,flags=re.X):
			heir.append(line.split()[2])
		elif re.search(r"\$upscope \b",line,flags=re.X):
			heir.pop()
		elif re.search(r"\$var \b",line,flags=re.X):
			type,size,code,name = line.split(' ',4)[1::]
			name = name.replace('$end','').strip()
			path = '.'.join(heir)
			full_name = path + name
		i++
def calcMult(statement, opt):
	pass

def getTimescale():
	pass

def getEndtime():
	pass