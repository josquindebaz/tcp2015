import csv,re

auteurs  = []
liens = []
with open('THATCamp FR - Base.csv', 'rb') as csvfile:
	b =  csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in b:
		if len(row) > 5:	
			a = re.split(';',row[5])
			if  a != ["Auteurs"]:
				a = map(lambda x : re.sub("\s*$","",x), a)
				a = map(lambda x : re.sub("^\s*","",x), a)
				for c in a:
					if c not in auteurs:
						auteurs.append(c)
				if len(a) > 1:
					a = map(lambda x : auteurs.index(x),a)
					liens.append(a)

				
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

