N=5
M=2
config_initiala= (3,3,0,0,0)
config_finala = (0,0,3,3,1)

def calc_euristica(info):
    distanta= (info[0] + info[1])/ (M-1)
    return distanta

#verific daca o configuratie formata din canibali-misionari e valida
def is_valid(can,mis):
    if (can>=0):
        if (mis ==0):
            return True
        elif (mis-can >=0):
            return True
    return False



class Nod:
    def __init__(self,info):
        self.info = info;
        self.h = calc_euristica(info)

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self,capat, varf):
        self.capat=capat
        self.varf=varf
        self.cost=1

class Problema:
    def __init__(self):
        self.noduri=[Nod(config_initiala)]
        self.arce=[]
        self.nod_start=self.noduri[0]
        self.nod_scop=config_finala

    def cauta_nod_nume(self,info):
        for nod in self.noduri:
            if nod.info == info:
                    return nod
            return None


class NodParcurgere:
    problema=None
    def __init__(self,nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf
        self.parinte = parinte
        self.g = g
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def contine_in_drum(self, nod):
        nod_c =self
        while nod_c.parinte is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    def drum_arbore(self):
        nod_c=self
        drum=[nod_c]
        while nod_c.parinte is not None:
            drum=[nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def test_scop(self):
        if self.nod_graf.h:
            return False
        return True
        #return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"

    def expandeaza(self):
        l_succesori=[]
        info=self.nod_graf.info
        mal=info[4]
        #luam toate posibilitatile de misionari si canibali
        for m in range(min(info[mal*2+1],M) + 1):
            if m==0:
                nr_can_max=M
            else:
                nr_can_max= min(M-m, m, info[mal*2])
            for c in range (nr_can_max + 1):
                if m ==0 and c==0:
                    continue
                if m+c>M:
                    continue
                nou_mal=1-mal
                succ=[0,0,0,0,0]
                succ[4]=nou_mal
                succ[nou_mal*2]=info[nou_mal*2]+c
                succ[nou_mal*2+1]=info[nou_mal*2+1]+m
                succ[mal*2]=info[mal*2]-c
                succ[mal*2+1]=info[mal*2+1]-m

                if is_valid(succ[0],succ[1]) and is_valid(succ[2],succ[3]):
                    t1=tuple(succ)
                    succesor=problema.cauta_nod_nume(t1)
                    if not succesor:
                        nod_nou=Nod(t1)
                        problema.noduri.append(nod_nou)
                        succesor=nod_nou
                    cost=1
                    l_succesori.append((succesor,cost))
        #print(l_succesori)
        return l_succesori



def str_info_noduri(l):
    sir = "["
    for x in l:
        sir += str(x) + "  "
    sir += "]"
    return sir

def afis_succesori_cost(l):
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)
    return sir

def in_lista(l, nod):
	"""
		lista "l" contine obiecte de tip NodParcurgere
		"nod" este de tip Nod
	"""
	for i in range(len(l)):
		if l[i].nod_graf.info == nod.info:
			return l[i]
	return None

def a_star():
	"""
		Functia care implementeaza algoritmul A-star
	"""
	### TO DO ... DONE

	rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
	open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
	closed = []  # closed va contine elemente de tip NodParcurgere

	while len(open) > 0 :

		print("Afisam open: " + str_info_noduri(open)) 	# afisam lista open
		nod_curent = open.pop(0)	# scoatem primul element din lista open
		closed.append(nod_curent)	# si il adaugam la finalul listei closed

		#testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
		if nod_curent.test_scop():
			break

		l_succesori = nod_curent.expandeaza()# contine tupluri de tip (Nod, numar)
		for (nod_succesor, cost_succesor) in l_succesori:
			# "nod_curent" este tatal, "nod_succesor" este fiul curent

			# daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
			if (not nod_curent.contine_in_drum(nod_succesor)):

				# calculez valorile g si f pentru "nod_succesor" (fiul)
				g_succesor = nod_curent.g + cost_succesor # g-ul tatalui + cost muchie(tata, fiu)
				f_succesor = g_succesor + nod_succesor.h # g-ul fiului + h-ul fiului

				#verific daca "nod_succesor" se afla in closed
				# (si il si sterg, returnand nodul sters in nod_parcg_vechi
				nod_parcg_vechi = in_lista(closed, nod_succesor)

				if nod_parcg_vechi is not None:	# "nod_succesor" e in closed
					# daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
					# 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
					# atunci actualizez parintele, g si f
					# si apoi voi adauga "nod_nou" in lista open
					if (f_succesor < nod_parcg_vechi.f):
						closed.remove(nod_parcg_vechi)	# scot nodul din lista closed
						nod_parcg_vechi.parinte = nod_curent # actualizez parintele
						nod_parcg_vechi.g = g_succesor	# actualizez g
						nod_parcg_vechi.f = f_succesor	# actualizez f
						nod_nou = nod_parcg_vechi	# setez "nod_nou", care va fi adaugat apoi in open

				else :
					# daca nu e in closed, verific daca "nod_succesor" se afla in open
					nod_parcg_vechi = in_lista(open, nod_succesor)

					if nod_parcg_vechi is not None:	# "nod_succesor" e in open
						# daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
						# 	   f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
						# atunci scot nodul din lista open
						# 		(pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
						# actualizez parintele, g si f
						# si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
						if (f_succesor < nod_parcg_vechi.f):
							open.remove(nod_parcg_vechi)
							nod_parcg_vechi.parinte = nod_curent
							nod_parcg_vechi.g = g_succesor
							nod_parcg_vechi.f = f_succesor
							nod_nou = nod_parcg_vechi

					else: # cand "nod_succesor" nu e nici in closed, nici in open
						nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor)
						# se calculeaza f automat in constructor

				if nod_nou:
					# inserare in lista sortata crescator dupa f
					# (si pentru f-uri egale descrescator dupa g)
					i=0
					while i < len(open):
						if open[i].f < nod_nou.f:
							i += 1
						else:
							while i < len(open) and open[i].f == nod_nou.f and open[i].g > nod_nou.g:
								i += 1
							break

					open.insert(i, nod_nou)


	print("\n------------------ Concluzie -----------------------")
	if len(open) == 0:
		print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
	else:
		print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()

