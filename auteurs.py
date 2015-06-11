import csv,re

class FromCSV(object):
	"""recup data from csv file"""
	def __init__(self,f ='THATCamp FR - Base.csv' ):
		with open(f, 'rb') as csvfile:
			"""from a comma-separated export of google spreadsheet"""
			buf =  csv.reader(csvfile, delimiter=',', quotechar='"')
			self.rows = []
			for row in buf:
				self.rows.append(row)

			self.colums = self.rows[0]
			self.rows.pop(0)

	def N_Col(self,val):
		"""index of a column value"""
		if val in self.colums:
			return self.colums.index(val)
		else:
			return False


def nettoie(txt):
	"""supprime les blancs en debut et fin de string"""
	txt = re.sub("\s*$","",txt)
	txt = re.sub("^\s*","",txt)
	return txt

recup = FromCSV()

auteurs  = []
liens = []
institutions = {}
nb_atelier = {}

for row in recup.rows:
	if len(row) > 5:	
		inst = re.split(';',row[11]) #recup institutions 
		authors = re.split(';',row[5])	#recup authors
		authors = map(nettoie, authors)
		for author in authors:
			if author not in auteurs:
				auteurs.append(author) #add a new author
			"""find institution"""
			if len(inst) == 1 and len(authors) == 1 and inst[0] != "":
				institutions[author] = inst[0] 
			elif len(inst) == len(authors) and len(inst) > 1 :
				 institutions[ author ] = inst[authors.index(author)] 
			"""compte nb ateliers par auteurs"""
			if author in nb_atelier:
				nb_atelier[ author] += 1
			else :
				nb_atelier[ author] = 1
					
		if len(authors) > 1: #links
			authors = map(lambda x : auteurs.index(x),authors)
			liens.append(authors)

				
""".net generation for pajek"""
F = open("auteurs.net",'w')
txt = "*Vertices   %s\n" % len(auteurs)
for aut in auteurs:
	txt += '%d "%s"\n' % (auteurs.index(aut)+1,aut)

txt += "*Edges\n" 
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

""".paj generation for pajek"""
txt = "*Network auteurs.net\n" + txt
txt += "\n*Partition institution\n*Vertices %d\n" % len(auteurs)

institutions_liste =  institutions.values()
for aut in auteurs:
	if aut in institutions:
		txt += "%d\n" %  (institutions_liste.index(institutions[aut]))
	else :
		txt += "0\n" 

txt += "\n*Vector nb of workshop\n*Vertices %d\n" % len(auteurs)
for aut in auteurs:
	txt += "%d\n" % nb_atelier[aut]

F = open("test.paj",'w')
F.write(txt)
F.close()


