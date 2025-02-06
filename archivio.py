import ast

class Studente:

    def __init__(self, cognome, nome, matricola):
        #controllo dei tipi e dei valori dei parametri iniziali
        if type(cognome) != str or type(nome) != str:
            raise TypeError(f'Il parametro nome/cognome deve essere una stringa')
        if type(matricola) != int:
            raise TypeError(f'Il parametro matricola deve essere un numero intero')
        if matricola <= 0:
            raise ValueError("Il parametro matricola deve essere un numero positivo")

        self.cognome = cognome
        self.nome = nome
        self.matricola = matricola
        self.listaesami = []

    #metodi di accesso per ottenere gli attributi dell'istanza della classe

    def get_cognome(self):
        return self.cognome

    def get_nome(self):
        return self.nome

    def get_matricola(self):
        return self.matricola

    def get_listaesami(self):
        return self.listaesami


    #metodi di modifica per impostare nuovi valori agli attributi dell'istanza della classe

    def set_cognome(self, cognome):
        if type(cognome) != str:
            raise TypeError("Il parametro nome deve essere una stringa")
        self.cognome = cognome

    def set_nome(self, nome):
        if type(nome) != str:
            raise TypeError("Il parametro nome deve essere una stringa")
        else:
            self.nome = nome

    def set_matricola(self, matricola):
        if type(matricola) != int:
            raise TypeError("Il parametro matricola deve essere un intero")
        self.matricola = matricola

    def set_listaesami(self, listaesami):
        if listaesami == []:
            self.listaesami = []
        else:
            for i in listaesami:
                if type(i[0]) != str or type(i[1]) != int:
                    raise TypeError("La tupla di listaesami deve essere una stringa")
                elif i[1] < 18 or i[1] >= 33:
                    raise ValueError("Il numero intero deve essere maggiore o uguale di 18 e minore di 33")
                else:
                    self.listaesami = listaesami

    def get_voto(self, codice):
        for i in range(len(self.listaesami)):
            if self.listaesami[i][0] == codice:
                return self.listaesami[i][1]

    def __str__(self):
        if self.listaesami == []:
            return f'{self.nome} {self.cognome} mat: {self.matricola} esami: no'
        else:
            return f'{self.nome} {self.cognome} mat: {self.matricola} esami: {self.listaesami}'

    def __eq__(self, altroStudente):
        return self.cognome == altroStudente.cognome and self.nome == altroStudente.nome and self.matricola == altroStudente.matricola

    def registra_esame(self, codice, voto):
        if type(codice) != str or type(voto) != int or (voto < 18 or voto >= 33):
            return False
        for tupla in self.listaesami:
            #verifica se l'esame con lo stesso codice è già presente nella lista
            if tupla[0] == codice:
                return False
        else:
            self.listaesami.append((codice, voto))
            return True

    def modifica_voto(self, codice, voto):
        if type(codice) != str or type(voto) != int or (voto < 18 or voto >= 33):
            return False
        for i in range(len(self.listaesami)):
            if self.listaesami[i][0] == codice:
                self.listaesami.pop(i) #elimino la tupla codice, voto per aggiungere quella col voto modificato
                self.listaesami.append((codice, voto))
                return True
        else:
            return False

    def cancella_esame(self, codice):
        if type(codice) != str:
            return False
        for i in range(len(self.listaesami)):
            if self.listaesami[i][0] == codice:
                self.listaesami.pop(i)
                return True
        else:
            return False

    def media(self):
        somma = 0
        #controllo che la lista degli esami non sia vuota per evitare una divisione per 0
        if len(self.listaesami) > 0:
            for i in range(len(self.listaesami)):
                somma += self.listaesami[i][1]
            return somma / len(self.listaesami)

class Archivio():

    def __init__(self):
        self.stud = {}

    def inserisci(self, studente, note=""):
        #metodo che inserisce nel dizionario una tupla, contenente un oggetto Studente ed eventuali note
        if isinstance(self.stud, dict) and isinstance(studente, Studente) and isinstance(note, str):
            matricola = studente.get_matricola()
            if matricola not in self.stud.keys(): #controllo per evitare di inserire due studenti con la stessa matricola
                self.stud[matricola] = (studente, note)
                return True
            else:
                return False
        else:
            return False

    def elimina(self, matricola):
        if matricola in self.stud.keys():
            del self.stud[matricola]
            return True
        else:
            return False

    def get_note(self, matricola):
        if matricola in self.stud.keys():
            return self.stud.get(matricola)[1]

    def get_studenti(self):
        return list(self.stud.keys())

    def modifica_note(self, matricola, nota):
        if matricola in self.stud.keys():
            self.stud[matricola] = (self.stud.get(matricola)[0], nota)
            return True

    def __str__(self):
        stringa = ""
        for tupla in self.stud.values():
            stringa += f'{tupla[0]}\n'
        return stringa

    def studente(self, matricola):
        if matricola in self.stud.keys():
            return self.stud.get(matricola)[0]

    def registra_esame(self, matricola, codice, voto):
        if type(codice) != str or type(voto) != int or (voto < 18 or voto >= 33):
            return False
        if matricola in self.stud.keys():
            for i in range(len(self.stud[matricola][0].get_listaesami())):
                if codice == self.stud[matricola][0].get_listaesami()[i][0]: #controllo per evitare di inserire un esame già presente
                    return False
            else:
                self.stud[matricola][0].get_listaesami().append((codice, voto))
                return True
        else:
            return False

    def modifica_voto(self, matricola, codice, voto):
        if type(codice) != str or type(voto) != int or (voto < 18 or voto >= 33):
            return False
        if matricola in self.stud.keys():
            if 18 <= voto <= 33:
                for i in range(len(self.stud[matricola][0].get_listaesami())):
                    if codice == self.stud[matricola][0].get_listaesami()[i][0]:
                        self.stud[matricola][0].get_listaesami().pop(i)
                        self.stud[matricola][0].get_listaesami().append((codice, voto))
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def cancella_esame(self, matricola, codice):
        if matricola in self.stud.keys():
            for i in range(len(self.stud[matricola][0].get_listaesami())):
                if codice == self.stud[matricola][0].get_listaesami()[i][0]:
                    self.stud[matricola][0].get_listaesami().pop(i)
                    return True
            else:
                return False
        else:
            return False

    def media(self, matricola):
        somma = 0
        if matricola in self.stud.keys() and len(self.stud[matricola][0].get_listaesami()) > 0:
            for i in range(len(self.stud[matricola][0].get_listaesami())):
                somma += self.stud[matricola][0].get_listaesami()[i][1]
            return somma / len(self.stud[matricola][0].get_listaesami())

    def lista_studenti_promossi(self, codice, soglia = 18):
        studenti_promossi = list()
        for matricola in self.stud.keys():
            for i in range(len(self.stud[matricola][0].get_listaesami())):
                if codice == self.stud[matricola][0].get_listaesami()[i][0] and self.stud[matricola][0].get_listaesami()[i][1] >= soglia:
                    studenti_promossi.append(f'{self.stud[matricola][0].get_nome()} {self.stud[matricola][0].get_cognome()}')
        return studenti_promossi

    def conta_studenti_promossi(self, codice, soglia = 18):
        return len(self.lista_studenti_promossi(codice, soglia))

    def lista_studenti_media(self, soglia = 18):
        studenti_media = []
        for matricola in self.stud.keys():
            #controllo per verificare che lo studente abbia una media (quindi un output diverso da None) che sia maggiore o uguale della soglia
            if self.media(matricola) != None and self.media(matricola) >= soglia:
                studenti_media.append((self.stud[matricola][0].get_nome(), self.stud[matricola][0].get_cognome(), self.stud[matricola][0].get_matricola()))
        return studenti_media

    def salva(self, nomefile):
        try:
            with open(nomefile, "w") as f:
                for matricola in self.stud.keys():
                    s = self.stud[matricola][0] #oggetto Studente
                    n = self.stud[matricola][1] #stringa con le note
                    f.write(s.get_nome() + ":" + s.get_cognome() + ":" + str(s.get_matricola()) + ":" + str(s.get_listaesami()) + ":" + n + "\n")
                return True
        except IOError as e:
            print(nomefile, ": ", e)
            return False
        except ValueError as e:
            print(nomefile, ": ", e)
            return False

    def carica(self, nomefile):
        try:
            f = open(nomefile, "r")
        except IOError as e:
            print(nomefile, ": ", e)
            return False
        except ValueError as e:
            print(nomefile, ": ", e)
            return False
        else:
            self.stud = {}
            for riga in f:
                riga = riga.replace("\n", "").split(":")
                if len(riga) > 4:
                    nome = riga[0]
                    cognome = riga[1]
                    matricola = int(riga[2])
                    lista_esami = riga[3]
                    note = riga[4]
                    lista_esami = ast.literal_eval(lista_esami) # Converte la rappresentazione stringa di una lista in una lista effettiva
                    oggetto_studente = Studente(cognome, nome, matricola)
                    oggetto_studente.set_listaesami(lista_esami)
                    self.inserisci(oggetto_studente, note)
                elif len(riga) <= 4:
                    nome = riga[0]
                    cognome = riga[1]
                    matricola = int(riga[2])
                    lista_esami = riga[3]
                    lista_esami = ast.literal_eval(lista_esami)
                    oggetto_studente = Studente(cognome, nome, matricola)
                    oggetto_studente.set_listaesami(lista_esami)
                    self.inserisci(oggetto_studente)
            return True
        f.close()


