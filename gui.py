import tkinter as tk
from tkinter import filedialog
from archivio import *
import ast

#definizione della classe FinestraPrincipale che ospiterà l'archivio studenti sotto forma di label in un frame
class FinestraPrincipale:
    def __init__(self, root):
        self.root = root
        self.root.title("Archivio Studenti")
        self.root.resizable(False, False)

        # creazione di due frame: uno per entry e bottoni, uno per visualizzare l'archivio
        self.frameB = tk.Frame(self.root, background="#E0FFFF")
        self.frameB.pack(side=tk.LEFT, fill=tk.Y)

        self.frameE = tk.Frame(self.root, width=600, height=600, background="#E0FFFF")
        self.frameE.pack(fill=tk.BOTH)


        # creazione dei bottoni da inserire nel frame a sinistra
        # utilizzo delle funzioni anonime lambda per richiamare due metodi contemporaneamente come parametro di command
        self.buttonca = tk.Button(self.frameB, width=40, height=2, background="red", text="Chiudi applicazione", command=lambda: (self.cambia_contenuto_label(), self.chiudi_applicazione()))
        self.buttonca.pack(side=tk.BOTTOM)

        self.buttonca = tk.Button(self.frameB, width=40, height=2, background="orange", text="Salva archivio in un file", command=lambda: (self.cambia_contenuto_label(), self.salva_archivio()))
        self.buttonca.pack(side=tk.BOTTOM)

        self.buttoncf = tk.Button(self.frameB, width=40, height=2, background="yellow", text="Carica archivio da file", command=lambda: (self.cambia_contenuto_label(), self.carica_archivio()))
        self.buttoncf.pack(side=tk.BOTTOM)

        self.APRI = tk.Button(self.frameB, width=40, height=2, background="light blue", text="Inserisci nuovo studente", command=lambda: (self.cambia_contenuto_label(), self.apri_finestra_secondaria("Inserisci nuovo studente", "no")))
        self.APRI.pack()

        self.buttonm = tk.Button(self.frameB, width=40, height=2, background="light blue", text="Modifica dati studente", command=lambda: (self.cambia_contenuto_label(), self.apri_finestra_secondaria("Modifica dati studente", "si")))
        self.buttonm.pack()

        self.buttond = tk.Button(self.frameB, width=40, height=2, background="light blue", text="Elimina studente", command=self.elimina_studente)
        self.buttond.pack()

        self.buttoncv = tk.Button(self.frameB, width=40, height=2, background="light blue", text="Calcola media voti studente", command=lambda: (self.cambia_contenuto_label(), self.media_studente()))
        self.buttoncv.pack()

        # inserimento di una label dove comparirà la media
        self.labelL = tk.Label(self.frameB, width=40, height=2, text="", background="light blue")
        self.labelL.pack()
        self.labelL.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # inserimento di una label dove appariranno eventuali messaggi di errore
        self.labelAvvisi = tk.Label(self.frameB, width=40, height=2, text="", background="light blue", wraplength=200, justify="left")
        self.labelAvvisi.pack()
        self.labelAvvisi.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Canvas all'interno del frame a destra, che permette di scorrere il contenuto con una barra laterale
        self.canvas = tk.Canvas(self.frameE, width=600, height=600, borderwidth=0, background="#E0FFFF")
        self.scrollable_frame = tk.Frame(self.canvas, width=600, height=600, background="#E0FFFF")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollbar = tk.Scrollbar(self.frameE, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # definizione di parametri generali della classe, utili per i metodi
        self.archivio = Archivio()
        self.diz_label = {} # dizionario che memorizza le label degli studenti
        self.file_path = None # parametro che memorizza il percorso del file, per capire se è già stato caricato o meno
        self.chiave_label_selezionata = "" # parametro che memorizza la chiave della label selezionata con il mouse
        self.archivio_salvato = False # parametro che memorizza se l'archivio è stato salvato o meno

    def cambia_contenuto_label(self, messaggio=""): # metodo per far comparire eventuali errori in una label nel frame a sinistra
        if messaggio != "":
            self.labelAvvisi.config(text=messaggio)
        else:
            self.labelAvvisi.config(text="")

    def apri_finestra_secondaria(self, titoloFinestraSecondaria, modifica): # metodo per aprire una finestra secondaria. Il valore di modifica indica se si vuole inserire o modificare uno studente
        if modifica == "si": # valore che mi permette di modificare uno studente già presente nell'archivio
            if self.chiave_label_selezionata in self.diz_label.keys(): # verifica che sia stata selezionata una label
                for chiave in self.diz_label:
                    if chiave == self.chiave_label_selezionata:
                        studente = self.archivio.studente(chiave)
                        nome = studente.get_nome()
                        cognome = studente.get_cognome()
                        matricola = chiave
                        esami = studente.get_listaesami()
                        note = self.archivio.get_note(matricola)
                        if esami == []:
                            esami = "no"
                            # tipo di finestra secondaria in cui si modifica uno studente
                            finestra_secondaria = FinestraSecondaria1(self.root, self.labelL, self, titoloFinestraSecondaria, modifica, nome, cognome, matricola, esami, note)
                        else:
                            finestra_secondaria = FinestraSecondaria1(self.root, self.labelL, self, titoloFinestraSecondaria, modifica, nome, cognome, matricola, esami, note)
            else:
                self.cambia_contenuto_label("Nessuna label selezionata")
        else:
            # tipo di finestra secondaria in cui si inserisce uno studente
            finestra_secondaria = FinestraSecondaria1(self.root, self.labelL, self, titoloFinestraSecondaria, modifica)

    def on_label_click(self, event, clicked_key): # metodo per selezionare, anche a livello visivo, una label con il mouse
        for chiave in self.diz_label:
            if chiave == clicked_key:
                self.diz_label[chiave].config(bg="lightblue") # evidenzia la label selezionata in blu
                self.chiave_label_selezionata = chiave
            else:
                self.diz_label[chiave].config(bg="white") # mostra le altre label in bianco

    def on_mousewheel(self, event): # metodo per scorrere il contenuto della finestra
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ordina_label(self):
        # Ordina le label in ordine alfabetico
        sorted_keys = sorted(self.diz_label.keys(), key=lambda chiave: self.diz_label[chiave]['text'])
        for matricola in self.diz_label.keys():
            self.diz_label[matricola].pack_forget()
        for key in sorted_keys:
            self.diz_label[key].config(height=2)
            self.diz_label[key].config(padx=20)
            self.diz_label[key].pack(padx=20, pady=10, anchor='w')

    def carica_archivio(self):
        file_path = filedialog.askopenfilename() # dialog per scegliere il file da importare
        self.file_path = file_path
        if file_path:
            if self.archivio.carica(file_path) == False:
                self.cambia_contenuto_label("Caricamento fallito: il file non è del formato corretto")
            else:
                self.archivio.carica(file_path)

                for matricola in self.archivio.get_studenti():
                    riga_stud = str(self.archivio.studente(matricola))

                    # Controllo se la matricola è già presente nel dizionario esistente
                    if matricola not in self.diz_label:
                        label = tk.Label(self.scrollable_frame, text=riga_stud, bg="white")
                        label.pack(padx=20, pady=10)

                        self.diz_label[matricola] = label
                        # associa il click del tasto sinistro del mouse al metodo on_label_click
                        label.bind("<Button-1>", lambda event, chiave=matricola: self.on_label_click(event, chiave))

                self.ordina_label() # richiama il metodo per ordinare le label
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                self.cambia_contenuto_label("Archivio caricato correttamente")
        else:
            self.cambia_contenuto_label("Nessun file selezionato")

    def salva_archivio(self):
        try:
            if self.diz_label != {}:
                file_destinazione = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("File di testo", "*.txt")]) # Apre una finestra di dialogo per chiedere all'utente il percorso e il nome del file di destinazione
                self.file_path = file_destinazione
                file_origine = self.file_path
                self.archivio.salva(file_origine) # salva l'oggetto Archivio richiamando un metodo della classe Archivio
                self.archivio_salvato = True
                self.cambia_contenuto_label("Copia del file creata correttamente.")
            else:
                self.cambia_contenuto_label("Questo archivio è vuoto, impossibile salvare una copia")
        except FileNotFoundError:
                self.cambia_contenuto_label("Il file specificato non esiste.")
        except IOError as e:
                self.cambia_contenuto_label("Errore di I/O:", e)

    def elimina_studente(self):
        if self.chiave_label_selezionata:
            if self.chiave_label_selezionata in self.diz_label:
                # se c'è una label selezionata, elimina lo studente e la label associati alla label
                self.diz_label[self.chiave_label_selezionata].pack_forget()
                del self.diz_label[self.chiave_label_selezionata]
                self.archivio.elimina(self.chiave_label_selezionata)
                # Aggiorna la visualizzazione dopo l'eliminazione
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

                self.chiave_label_selezionata = ""
                self.cambia_contenuto_label("Studente eliminato con successo")
        else:
            self.cambia_contenuto_label("Seleziona uno studente da eliminare prima di cliccare su 'Elimina studente'")

    def media_studente(self): # metodo per calcolare la media di uno studente selezionato, se è presente almeno un esame

        if self.chiave_label_selezionata:
            studente = self.archivio.studente(self.chiave_label_selezionata)
            media = studente.media()

            if media is not None:
                self.labelL.config(text=f"La media dello studente {self.chiave_label_selezionata} è {media:.2f}")
            else:
                self.labelL.config(text=f"Lo studente {self.chiave_label_selezionata} non ha esami con voti.")
            self.cambia_contenuto_label()
        else:
            self.cambia_contenuto_label("Seleziona uno studente per calcolare la media")

    def chiudi_applicazione(self):
        if self.archivio_salvato == True:
            conferma = tk.messagebox.askquestion("Conferma", "Sei sicuro/a di voler chiudere l'applicazione?")
            if conferma == 'yes':
                self.root.destroy()
        elif self.diz_label == {}:
            conferma = tk.messagebox.askquestion("Conferma", "Sei sicuro/a di voler chiudere l'applicazione?")
            if conferma == 'yes':
                self.root.destroy()
        else:
            # messaggio che compare se l'archivio non è vuoto e non è stato ancora salvato
            conferma = tk.messagebox.askquestion("Conferma", "L'archivio non è stato salvato. Sei sicuro/a di voler chiudere comunque l'applicazione?")
            if conferma == 'yes':
                self.root.destroy()

class FinestraSecondaria1: # classe che crea una finestra secondaria attraverso cui inserire uno studente o modificare i dati di uno già inserito
    # se stiamo modificando uno studente, vengono passati i parametri che saranno i valori iniziali dei widget
    def __init__(self, root, label_finestra_principale, finestra_principale, titoloFinestraSecondaria, modifica, nome="", cognome="", matricola="", esami="", note=""):
        self.root = tk.Toplevel(root)
        self.root.title(titoloFinestraSecondaria)
        self.root.resizable(False, False)
        # creazione di frame per separare visivamente i widget
        self.frameAlto = tk.Frame(self.root, width=60)
        self.frameAlto.pack(fill=tk.BOTH, expand=True)
        self.frameS = tk.Frame(self.root, width=60)
        self.frameS.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frameD = tk.Frame(self.root, width=60)
        self.frameD.pack(fill=tk.BOTH, expand=True)
        self.frameBasso = tk.Frame(self.root, width=60)
        self.frameBasso.pack(fill=tk.BOTH, expand=True)

        var_nome = tk.StringVar()
        var_cognome = tk.StringVar()
        var_matricola = tk.StringVar()
        var_esami = tk.StringVar()
        var_note = tk.StringVar()

        self.label_finestra_principale = label_finestra_principale
        self.finestra_principale = finestra_principale
        self.modifica = modifica # parametro che ha valore "no" se sto inserendo uno studente, "si" se sto modificando uno studente

        self.nome = ""
        self.cognome = ""
        self.matricola = ""
        self.esami = ""
        self.note = ""

        self.label = tk.Label(self.frameAlto, width=60, text="")
        self.label.pack()
        self.label = tk.Label(self.frameS, width=60, text="Nome:")
        self.label.pack()
        self.entryNome = tk.Entry(self.frameD, width=60, textvariable=var_nome)
        self.entryNome.pack()
        self.label = tk.Label(self.frameS, width=60, text="Cognome:")
        self.label.pack()
        self.entryCognome = tk.Entry(self.frameD, width=60, textvariable=var_cognome)
        self.entryCognome.pack()
        self.label = tk.Label(self.frameS, width=60, text="Matricola (non sarà modificabile in seguito):")
        self.label.pack()
        if self.modifica == "no": # se sto inserendo uno studente
            self.entryMatricola = tk.Entry(self.frameD, width=60, textvariable=var_matricola) # se sto inserendo uno studente, creo una entry dove mettere il numero di matricola
            self.entryMatricola.pack()
            self.label = tk.Label(self.frameS, width=60, text='Esami, se dati, nel formato [("abc45", 28)], altrimenti scrivere "no":')
            self.label.pack()
            self.entryEsami = tk.Entry(self.frameD, width=60, textvariable=var_esami)
            self.entryEsami.pack()
            self.label = tk.Label(self.frameS, width=60, text='Note, se ci sono, altrimenti scrivere "no":')
            self.label.pack()
            self.entryNote = tk.Entry(self.frameD, width=60, textvariable=var_note)
            self.entryNote.pack()
            self.bottone = tk.Button(self.frameBasso, width=30, text="Conferma", command=self.ottieni_testo)
            self.bottone.pack()
        else: # sto modificando uno studente inserito precedentemente
            self.labelMatricola = tk.Label(self.frameD, width=60, textvariable=var_matricola) # se sto modificando uno studente, creo una label con la sua matricola
            self.labelMatricola.pack()
            self.label = tk.Label(self.frameS, width=60, text='Esami, se dati, nel formato [("abc45", 28)], altrimenti scrivere "no":')
            self.label.pack()
            self.entryEsami = tk.Entry(self.frameD, width=60, textvariable=var_esami)
            self.entryEsami.pack()
            self.label = tk.Label(self.frameS, width=60, text='Note, se ci sono, altrimenti scrivere "no":')
            self.label.pack()
            self.entryNote = tk.Entry(self.frameD, width=60, textvariable=var_note)
            self.entryNote.pack()
            self.bottone = tk.Button(self.frameBasso, width=30, text="Conferma", command=self.ottieni_testo)
            self.bottone.pack()

        if nome and cognome and matricola and esami: # se li ho passati come parametri della classe, setto il loro valore come testo dei widget
            var_nome.set(nome)
            var_cognome.set(cognome)
            var_matricola.set(matricola)
            var_esami.set(str(esami))
            var_note.set(note)

    def lista_contenuto_label(self): # metodo ausiliare per recuperare in una lista il contenuto dei widget
        lista_contenuto = list()
        nome = self.entryNome.get()
        cognome = self.entryCognome.get()
        esami = self.entryEsami.get()
        note = self.entryNote.get()
        if self.modifica == "no":
            matricola = self.entryMatricola.get()
            lista_contenuto.append(nome)
            lista_contenuto.append(cognome)
            lista_contenuto.append(matricola)
            lista_contenuto.append(esami)
            lista_contenuto.append(note)
            return lista_contenuto
        else:
            matricola = self.labelMatricola.cget("text")
            lista_contenuto.append(nome)
            lista_contenuto.append(cognome)
            lista_contenuto.append(matricola)
            lista_contenuto.append(esami)
            lista_contenuto.append(note)
            return lista_contenuto

    def converti_stringa(self,stringa): # metodo ausiliario per convertire una stringa, se sotto forma di intero, in un type intero
        try:
            intero = int(stringa)
            return intero
        except ValueError:
            return stringa

    def prendo_contenuto_fin_second(self): # serve a cambiare il valore degli attributi della classe e gestire la differenza fra self.entryMatricola e self.labelMatricola

        nome = self.entryNome.get()
        cognome = self.entryCognome.get()
        esami = self.entryEsami.get()
        note = self.entryNote.get()
        if self.modifica == "no":
                matricola = self.entryMatricola.get()
                if not len(self.lista_contenuto_label()) == 5:  # serve a controllare se tutte le entry sono state riempite dall'utente
                    self.finestra_principale.cambia_contenuto_label("Errore nell'inserimento dei dati:\nle entry non vanno lasciate vuote")
                    self.root.destroy()
                else:
                    self.nome = nome
                    self.cognome = cognome
                    self.matricola = matricola
                    self.esami = esami
                    self.note = note
        else:
            matricola = self.labelMatricola.cget("text")
            if not len(self.lista_contenuto_label()) == 5:
                self.finestra_principale.cambia_contenuto_label("Errore nell'inserimento dei dati:\nle entry non vanno lasciate vuote")
                self.root.destroy()
            else:
                self.nome = nome
                self.cognome = cognome
                self.matricola = matricola
                self.esami = esami
                self.note = note

    def controllo_tipi_entry(self): # serve a controllare che i tipi degli entry siano corretti
        self.prendo_contenuto_fin_second()

        nome = self.converti_stringa(self.nome)
        cognome = self.converti_stringa(self.cognome)
        matricola = self.converti_stringa(self.matricola)
        esami = self.esami
        note = self.note

        try:
            if not (isinstance(nome, str) and isinstance(cognome, str) and isinstance(matricola, int)):
                raise TypeError("nome/cognome devono essere stringhe, matricola una matricola")

            matricola = int(matricola)
            if matricola <= 0:
                raise ValueError("La matricola deve essere un numero positivo")

            if esami == "no":
                return True
            elif esami == "":
                raise ValueError('se lo studente non ha ancora esami, scrivere "no"')
            elif "[" and "]" not in esami:
                raise TypeError('Gli esami devono essere inseriti in una lista')
            elif "[" and "]" in esami:
                lista_esami = ast.literal_eval(esami) # metodo del modulo ast che legge una stringa e la trasforma nell'oggetto Python corrispondente, come fosse un interprete
                if not isinstance(lista_esami, list):
                    raise TypeError('La lista degli esami deve essere una lista come [("abc45", 28)]')

                for esame in lista_esami:
                    if not (isinstance(esame, tuple) and len(esame) == 2 and isinstance(esame[0], str) and isinstance(
                            esame[1], int)):
                        raise TypeError(
                            'Ogni esame nella lista deve essere una tupla (stringa, intero) come [("abc45", 28)]')

                    voto = esame[1]
                    if not (18 <= voto <= 33):
                        raise ValueError("Il voto deve essere compreso tra 18 e 33")
                if note == "no" or isinstance(note, str):
                    return True

        except (TypeError, ValueError) as e:
            self.finestra_principale.cambia_contenuto_label(f"Errore nell'inserimento dei dati:\n {e}")
            self.root.destroy()
            return False

    def inserisci_studente_label(self, oggetto_studente, matricola, note): # metodo per inserire un oggetto studente all'archivio e aggiungere la label nel dizionario delle label. Entrambi hanno come chiave la matricola
        studente = Studente(oggetto_studente.get_cognome(), oggetto_studente.get_nome(), matricola)
        if oggetto_studente.get_listaesami():
            studente.set_listaesami(oggetto_studente.get_listaesami())
        # Aggiungi lo studente all'archivio
        self.finestra_principale.archivio.inserisci(studente, note)

        studente_e_note = str(self.finestra_principale.archivio.studente(matricola)) + " " + str(note)
        # le label aggiunte hanno come testo l'oggetto Studente e le note e possono essere selezionate col mouse
        label = tk.Label(self.finestra_principale.scrollable_frame, text=studente_e_note, bg="white")
        self.finestra_principale.diz_label[matricola] = label
        label.bind("<Button-1>", lambda event, chiave=matricola: self.finestra_principale.on_label_click(event, chiave))
        self.finestra_principale.ordina_label()

    def ottieni_testo(self): # metodo per ottenere i parametri per inserire un oggetto studente nell'archivio e aggiungere la label con le note nel dizionario delle label
        if self.controllo_tipi_entry() is True:
            nome = self.entryNome.get()
            cognome = self.entryCognome.get()
            matricola = int(self.matricola)
            esami = self.entryEsami.get()
            note = self.entryNote.get()
            if self.modifica == "no":
                if matricola in self.finestra_principale.archivio.get_studenti(): # prima di inserire una nuova label controlla se esiste già una label con la matricola che si vuole inserire
                    self.finestra_principale.cambia_contenuto_label("la matricola è già presente nel dizionario")
                    self.root.destroy()
                else:
                    oggetto_studente = Studente(cognome, nome, matricola)
                    if esami == "no" or esami == "":
                        self.inserisci_studente_label(oggetto_studente, matricola, note)
                        self.finestra_principale.ordina_label()
                        self.root.destroy()
                    else: # se esami è una lista di tuple
                        esami = ast.literal_eval(self.entryEsami.get())
                        oggetto_studente.set_listaesami(esami)
                        self.inserisci_studente_label(oggetto_studente, matricola, note)
                        self.finestra_principale.ordina_label()
                        self.root.destroy()
            else:
                oggetto_studente = Studente(cognome, nome, matricola)
                if esami != "no": # ci sono esami da inserire
                    self.finestra_principale.archivio.elimina(matricola)
                    self.finestra_principale.diz_label[matricola].pack_forget()
                    esami = ast.literal_eval(esami)
                    oggetto_studente.set_listaesami(esami)
                    self.inserisci_studente_label(oggetto_studente, matricola, note)
                    self.finestra_principale.ordina_label()
                    self.root.destroy()
                else:
                    self.finestra_principale.archivio.elimina(matricola)
                    self.finestra_principale.diz_label[matricola].pack_forget()
                    self.inserisci_studente_label(oggetto_studente, matricola, note)
                    self.finestra_principale.ordina_label()
                    self.root.destroy()
        else:
            self.root.destroy()


root = tk.Tk()
finestra = FinestraPrincipale(root)
root.mainloop()