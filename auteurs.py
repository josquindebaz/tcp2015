import csv,re


auteurs  = []
liens = []
institutions = {}
with open('THATCamp FR - Base.csv', 'rb') as csvfile:
	b =  csv.reader(csvfile, delimiter=',', quotechar='"')
	compt = 0
	for row in b:
		compt += 1
		if compt == 1:
			colonnes = row
		else :
			if len(row) > 5:	
				a = re.split(';',row[5])
				inst = re.split(';',row[11])
				a = map(lambda x : re.sub("\s*$","",x), a)
				a = map(lambda x : re.sub("^\s*","",x), a)
				for c in a:
					if c not in auteurs:
						auteurs.append(c)
						if len(inst) == 1 and len(a) == 1 and inst[0] != "":
							institutions[c] = inst[0]	
						elif len(inst) == len(a) and len(inst) > 1 :
							for cpt in range(len(a)):
								institutions[ a[cpt] ] = inst[cpt]
					
				if len(a) > 1:
					a = map(lambda x : auteurs.index(x),a)
					liens.append(a)

print institutions
				
F = open("auteurs.net",'w')
txt = "*Vertices   %s\n" % len(auteurs)
for aut in auteurs:
	txt += '%d "%s"\n' % (auteurs.index(aut)+1,aut)

txt += "*Arcs\n" 
for l in liens:
	if len(l) == 2:
		txt += "%d %d 1\n" %(l[0]+1,l[1]+1)
	else :
		while l:
			f = l.pop(0)
			for i in range(len(l)):
				txt += "%d %d 1\n" %(f+1,l[i]+1)
			
		

txt = txt.decode('utf-8').encode('latin-1')

F.write(txt)
F.close()

