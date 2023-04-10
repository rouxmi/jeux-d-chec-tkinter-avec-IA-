# -*- coding: utf-8 -*-
# importe les bibliothèques
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import sqlite3
import random
import time
from functools import partial
from playsound import playsound
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class jeu:
    # initialisent les variables
    def __init__(self):
        self.temp_debut=0
        self.selection_piece = "Button-1"
        self.selection_case = "Button-3"
        self.deplacer_piece = "Double-Button-1"
        self.tou = [1]
        self.Cs = -1
        self.fen = tk.Tk()
        self.fen.title("Echec")
        self.cote = 510
        self.marge_i = 150
        self.marge_j = 25
        self.Plateau = tk.Canvas(self.fen, bg="light gray", height=2 * self.marge_j + self.cote, width=self.cote + 2 * self.marge_i)
        self.Plateau.pack()
        self.NB_DE_CASES = 8
        self.pas = self.cote / self.NB_DE_CASES
        self.mn = []
        self.mb = []
        self.Cp = {}
        self.Pp = {}
        self.Statut = {}
        self.move_rock = {}
        self.tout_coup_possible = {}
        self.dpiece = [1]
        self.x_1, self.y_1 = [-3], [-3]
        self.rock_x, self.rock_y = [], []
        self.special_x, self.special_y = [-2], [-2]
        self.roi_x, self.roi_y = [-2], [-2]
        self.niveau_ordi = [-1]
        self.niveau_ordi2 = [-1]
        self.couleur_ordi = ['rien']
        # Image des pièces
        self.Cn = tk.PhotoImage(file='Image/Cn.gif')
        self.Dn = tk.PhotoImage(file='Image/Dn.gif')
        self.Pn = tk.PhotoImage(file='Image/Pn.gif')
        self.Fn = tk.PhotoImage(file='Image/Fn.gif')
        self.Tn = tk.PhotoImage(file='Image/Tn.gif')
        self.Rn = tk.PhotoImage(file='Image/Rn.gif')
        self.Tb = tk.PhotoImage(file='Image/Tb.gif')
        self.Rb = tk.PhotoImage(file='Image/Rb.gif')
        self.Fb = tk.PhotoImage(file='Image/Fb.gif')
        self.Db = tk.PhotoImage(file='Image/Db.gif')
        self.Pb = tk.PhotoImage(file='Image/Pb.gif')
        self.Cb = tk.PhotoImage(file='Image/Cb.gif')

        self.B = [self.Db, self.Tb, self.Fb, self.Cb, self.Rb, self.Pb]
        self.N = [self.Dn, self.Tn, self.Fn, self.Cn, self.Rn, self.Pn]
        # Plateau vide
        self.BaseVide = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

        self.pion_eval = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]

        self.cavalier_eval = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]

        self.fou_eval = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]

        self.tour_eval = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
        ]

        self.reine_eval = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]

        self.roi_eval = [

            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
        ]
        self.menubar = tk.Menu(self.fen)
        self.PMenu = tk.Menu(self.menubar)
        self.PMenu.add_command(label='Nouvelle Partie', command=partial(jeu.rejouer,self))
        self.PMenu.add_separator()
        self.PMenu.add_command(label='Quitter', command=partial(jeu.fin,self))
        self.menubar.add_cascade(label='Partie', menu=self.PMenu)
        DMenu = tk.Menu(self.menubar)
        DMenu.add_command(label="Retour en arrière", command=partial(jeu.nombre_retour,self))
        DMenu.add_command(label="Analyse de Partie", command=partial(jeu.analyse, self))
        self.menubar.add_cascade(label='Gestion des coups', menu=DMenu)
        self.fen.config(menu=self.menubar)
        # création de la Base de données
        self.totalTables = 0
        self.connection = sqlite3.connect("jeu_d'échec.db")
        self.curseur = self.connection.cursor()
        self.curseur.execute("drop table if exists partie")
        self.curseur.execute("create table partie (n°coup, id_piece, id_prise,col_depart,lig_depart,col_arrivé,lig_arrivé,temp_jeu)")
        self.connection.commit()
        self.connection.close()
        jeu.creation_table_inverse(self)
        jeu.nombre_joueurs(self)
        self.fen.bind('<' + self.selection_case + '>',partial(jeu.Selectionner_une_piece,self))
        self.fen.mainloop()

    def nombre_joueurs(self):
        """
        :return:un Menu de séléction des joueurs et affiche la suite du programme
        """
        self.Plateau.pack_forget()

        R = ttk.Style()
        R.configure('Wild.TButton',
                    background='black',
                    foreground='gray',
                    highlightthickness='20',
                    font=('Helvetica', 18, 'bold'))
        R.map('Wild.TButton',
              foreground=[('pressed', 'red'),
                          ('active', 'blue')],
              background=[('pressed', 'cyan'),
                          ('active', 'green')],
              relief=[('pressed', 'groove'),
                      ('!pressed', 'ridge')])
        text = tk.Text(self.fen, height=15)
        text.insert(tk.INSERT, "Bonjour, \nBienvenue dans le monde des échecs. \n"
                            "Pour comprendre comment jouer, suivez ces instructions:\n"
                            "-Pour sélectionner une pièce, faites clique-droit\n"
                            "-Pour déplacer une pièce, faites double-clique gauche\n"
                            "-Pour sélectionner une case, faites clique-gauche.\n"
                            "-Pour faire jouer l'ordinateur, faites clique-gauche.\n"
                            "Vos coups possibles seront guidés par des points sur le plateau.\n"
                            "Si vous ne connaissez pas les règles, voici un lien vers les règles des échecs:\n"
                               " https://fr.wikipedia.org \n"
                            "Vous avez un seul et unique but, mettre l’adversaire en échec et mat. \n" 
                            "Pour le reste, laisser votre raisonnement et vos intuitions prendre les devants.\n \nBon jeu!\n"
                            "Combien de joueurs ?")
        text.pack(side='top')

        def demmarage():
            self.Plateau.pack()
            choix_1.destroy()
            choix_2.destroy()
            choix_3.destroy()
            text.destroy()
            jeu.rafraichir_damier(self)
            jeu.Update(self)
            self.Plateau.create_rectangle(self.marge_i + -4 * self.pas, self.marge_j + 12 * self.pas, self.marge_i + (-4 + 1) * self.pas,
                                     self.marge_j + (12 + 1) * self.pas,
                                     width=3, outline='Red')
            self.Plateau.create_rectangle(self.cote / 2 + self.marge_i - 50, self.cote + self.marge_j * 3 / 2 - 10,
                                     self.cote / 2 + self.marge_i + 50, self.cote + self.marge_j * 3 / 2 + 10, fill='lightgray')
            self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(self.tou[0]) + ": Blanc", font='Bold',
                                tags='del')
            self.temp_debut = time.time()

        choix_1 = ttk.Radiobutton(self.fen, text="2 joueurs", command=demmarage, style='Wild.TButton')

        def selection_difficulte():
            choix_1.destroy()
            choix_2.destroy()
            choix_3.destroy()
            text.destroy()
            self.Plateau.pack_forget()
            valeur_ordi = tk.IntVar()

            T = ttk.Style()
            T.configure('Wild.TButton',
                        background='black',
                        foreground='gray',
                        highlightthickness='20',
                        font=('Helvetica', 18, 'bold'))
            T.map('Wild.TButton',
                  foreground=[('pressed', 'red'),
                              ('active', 'blue')],
                  background=[('pressed', 'cyan'),
                              ('active', 'green')],
                  relief=[('pressed', 'groove'),
                          ('!pressed', 'ridge')])
            tex = tk.Text(self.fen, height=1)
            tex.insert(tk.INSERT, "Choisissez votre niveau de difficulté :")
            tex.pack(side='top')
            a_1 = ttk.Radiobutton(self.fen, text="Très facile", value=1, variable=valeur_ordi, style='Wild.TButton')

            a_2 = ttk.Radiobutton(self.fen, text="Facile", value=2, variable=valeur_ordi, style='Wild.TButton')

            a_3 = ttk.Radiobutton(self.fen, text="Modéré", value=3, variable=valeur_ordi, style='Wild.TButton')

            a_4 = ttk.Radiobutton(self.fen, text="Difficile", value=4, variable=valeur_ordi, style='Wild.TButton')

            def diffi():
                self.Plateau.pack()
                a_1.destroy()
                a_2.destroy()
                a_3.destroy()
                a_4.destroy()
                b.destroy()
                tex.destroy()
                valeur = valeur_ordi.get()
                if valeur != 0:
                    def choix_couleur():
                        self.Plateau.pack_forget()

                        Q = ttk.Style()
                        Q.configure('Wild.TButton',
                                    background='black',
                                    foreground='gray',
                                    highlightthickness='20',
                                    font=('Helvetica', 18, 'bold'))
                        Q.map('Wild.TButton',
                              foreground=[('pressed', 'red'),
                                          ('active', 'blue')],
                              background=[('pressed', 'cyan'),
                                          ('active', 'green')],
                              relief=[('pressed', 'groove'),
                                      ('!pressed', 'ridge')])
                        texxt = tk.Text(self.fen, height=1, width=40)
                        texxt.insert(tk.INSERT, "Quelle couleur voulez-vous joué ?")
                        texxt.pack(side='top')

                        def blanc():
                            self.Plateau.pack()
                            texxt.destroy()
                            choix_Noir.destroy()
                            choix_Blanc.destroy()
                            self.couleur_ordi.pop(0)
                            self.couleur_ordi.append('Noir')
                            jeu.rafraichir_damier(self)
                            jeu.Update(self)
                            self.Plateau.create_rectangle(self.marge_i + -4 * self.pas, self.marge_j + 12 * self.pas, self.marge_i + (-4 + 1) * self.pas,
                                                     self.marge_j + (12 + 1) * self.pas,
                                                     width=3, outline='Red')
                            self.Plateau.create_rectangle(self.cote / 2 + self.marge_i - 50, self.cote + self.marge_j * 3 / 2 - 10,
                                                     self.cote / 2 + self.marge_i + 50, self.cote + self.marge_j * 3 / 2 + 10, fill='lightgray')
                            self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(self.tou[0]) + ": Blanc",
                                                font='Bold',
                                                tags='del')
                            self.temp_debut = time.time()

                        choix_Blanc = ttk.Radiobutton(self.fen, text="Blanc", command=blanc, style='Wild.TButton')

                        def noir():
                            self.Plateau.pack()
                            texxt.destroy()
                            choix_Noir.destroy()
                            choix_Blanc.destroy()
                            self.couleur_ordi.pop(0)
                            self.couleur_ordi.append('Blanc')
                            jeu.rafraichir_damier(self)
                            jeu.Update(self)
                            self.Plateau.create_rectangle(self.marge_i + -4 * self.pas, self.marge_j + 12 * self.pas, self.marge_i + (-4 + 1) * self.pas,
                                                     self.marge_j + (12 + 1) * self.pas,
                                                     width=3, outline='Red')
                            self.Plateau.create_rectangle(self.cote / 2 + self.marge_i - 50, self.cote + self.marge_j * 3 / 2 - 10,
                                                     self.cote / 2 + self.marge_i + 50, self.cote + self.marge_j * 3 / 2 + 10, fill='lightgray')
                            self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(self.tou[0]) + ": Blanc",
                                                font='Bold',
                                                tags='del')
                            jeu.tour_suivant(self)
                            self.temp_debut=time.time()

                        choix_Noir = ttk.Radiobutton(self.fen, text="Noir", command=noir, style='Wild.TButton')

                        choix_Blanc.pack(side='left')
                        choix_Noir.pack(side='left')

                    choix_couleur()
                    self.niveau_ordi.pop(0)
                    self.niveau_ordi.append(valeur)

                else:
                    selection_difficulte()

            b = ttk.Button(self.fen, text='Valider', command=diffi, style='Wild.TButton')
            a_1.pack(side='top')
            a_2.pack(side='top')
            a_3.pack(side='top')
            a_4.pack(side='top')
            b.pack(side='bottom', pady=15)

        choix_2 = ttk.Radiobutton(self.fen, text="1 joueur", command=selection_difficulte, style='Wild.TButton')

        def parametrage():
            choix_1.destroy()
            choix_2.destroy()
            choix_3.destroy()
            text.destroy()
            self.Plateau.pack_forget()
            valeur_ordi = tk.IntVar()

            T = ttk.Style()
            T.configure('Wild.TButton',
                        background='black',
                        foreground='gray',
                        highlightthickness='20',
                        font=('Helvetica', 18, 'bold'))
            T.map('Wild.TButton',
                  foreground=[('pressed', 'red'),
                              ('active', 'blue')],
                  background=[('pressed', 'cyan'),
                              ('active', 'green')],
                  relief=[('pressed', 'groove'),
                          ('!pressed', 'ridge')])
            texte = tk.Text(self.fen, height=1)
            texte.insert(tk.INSERT, "Choisissez votre niveau de difficulté de l'ordi Blanc:")
            texte.pack(side='top')
            a_1 = ttk.Radiobutton(self.fen, text="Très facile", value=1, variable=valeur_ordi, style='Wild.TButton')

            a_2 = ttk.Radiobutton(self.fen, text="Facile", value=2, variable=valeur_ordi, style='Wild.TButton')

            a_3 = ttk.Radiobutton(self.fen, text="Modéré", value=3, variable=valeur_ordi, style='Wild.TButton')

            a_4 = ttk.Radiobutton(self.fen, text="Difficile", value=4, variable=valeur_ordi, style='Wild.TButton')

            def diffi():
                self.Plateau.pack()
                a_1.destroy()
                a_2.destroy()
                a_3.destroy()
                a_4.destroy()
                b.destroy()
                texte.destroy()
                valeur = valeur_ordi.get()
                if valeur != 0:
                    def choix_niveau_ordi():
                        self.Plateau.pack_forget()
                        valeur_ordi_2 = tk.IntVar()

                        T = ttk.Style()
                        T.configure('Wild.TButton',
                                    background='black',
                                    foreground='gray',
                                    highlightthickness='20',
                                    font=('Helvetica', 18, 'bold'))
                        T.map('Wild.TButton',
                              foreground=[('pressed', 'red'),
                                          ('active', 'blue')],
                              background=[('pressed', 'cyan'),
                                          ('active', 'green')],
                              relief=[('pressed', 'groove'),
                                      ('!pressed', 'ridge')])
                        tex = tk.Text(self.fen, height=1)
                        tex.insert(tk.INSERT, "Choisissez votre niveau de difficulté de l'ordi Noir:")
                        tex.pack(side='top')
                        bu_1 = ttk.Radiobutton(self.fen, text="Très facile", value=1, variable=valeur_ordi_2,
                                               style='Wild.TButton')

                        bu_2 = ttk.Radiobutton(self.fen, text="Facile", value=2, variable=valeur_ordi_2, style='Wild.TButton')

                        bu_3 = ttk.Radiobutton(self.fen, text="Modéré", value=3, variable=valeur_ordi_2, style='Wild.TButton')

                        bu_4 = ttk.Radiobutton(self.fen, text="Difficile", value=4, variable=valeur_ordi_2, style='Wild.TButton')

                        def valider():
                            self.Plateau.pack()
                            bu_1.destroy()
                            bu_2.destroy()
                            bu_3.destroy()
                            bu_4.destroy()
                            cu.destroy()
                            tex.destroy()
                            valeur2 = valeur_ordi_2.get()
                            if valeur2 != 0:
                                self.niveau_ordi2.pop(0)
                                self.niveau_ordi2.append(valeur2)
                                self.Plateau.pack()
                                jeu.rafraichir_damier(self)
                                jeu.Update(self)
                                self.Plateau.create_rectangle(self.marge_i + -4 * self.pas, self.marge_j + 12 * self.pas, self.marge_i + (-4 + 1) * self.pas,
                                                         self.marge_j + (12 + 1) * self.pas,
                                                         width=3, outline='Red')
                                self.Plateau.create_rectangle(self.cote / 2 + self.marge_i - 50, self.cote + self.marge_j * 3 / 2 - 10,
                                                         self.cote / 2 + self.marge_i + 50, self.cote + self.marge_j * 3 / 2 + 10,
                                                         fill='lightgray')
                                self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2,
                                                    text=str(self.tou[0]) + ": Blanc",
                                                    font='Bold',
                                                    tags='del')
                                self.temp_debut=time.time()
                                self.fen.unbind('<' + self.selection_piece + '>')
                                self.fen.bind('<' + self.selection_piece + '>', jeu.tour_suivant)
                            else:
                                choix_niveau_ordi()

                        cu = ttk.Button(self.fen, text='Valider', command=valider, style='Wild.TButton')
                        bu_1.pack(side='top')
                        bu_2.pack(side='top')
                        bu_3.pack(side='top')
                        bu_4.pack(side='top')
                        cu.pack(side='bottom', pady=15)

                    choix_niveau_ordi()
                    self.niveau_ordi.pop(0)
                    self.niveau_ordi.append(valeur)

                else:
                    parametrage()

            b = ttk.Button(self.fen, text='Valider', command=diffi, style='Wild.TButton')
            a_1.pack(side='top')
            a_2.pack(side='top')
            a_3.pack(side='top')
            a_4.pack(side='top')
            b.pack(side='bottom', pady=15)

        choix_3 = ttk.Radiobutton(self.fen, text="0 joueur", command=parametrage, style='Wild.TButton')

        choix_1.pack(side='top')
        choix_2.pack(side='top')
        choix_3.pack(side='top')


    def neg_eval(self,table):
        table_inverse = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]
        for table_col in range(len(table)):
            for table_lig in range(len(table[table_col])):
                table_inverse[table_col][table_lig] = (-(table[table_col][table_lig]))
        return table_inverse
    def creation_table_inverse(self):
        self.fou_eval_N,  self.cavalier_eval_N,  self.reine_eval_N,  self.tour_eval_N,  self.pion_eval_N,  self.roi_eval_N = jeu.neg_eval(self, self.fou_eval), jeu.neg_eval(self,
            self.cavalier_eval), jeu.neg_eval( self,self.reine_eval), jeu.neg_eval(self, self.fou_eval), jeu.neg_eval( self,self.pion_eval), jeu.neg_eval( self,self.roi_eval)
        self.fou_eval_B, self.cavalier_eval_B, self.reine_eval_B, self.tour_eval_B, self.pion_eval_B, self.roi_eval_B = jeu.retourne_eval(self, self.fou_eval), jeu.retourne_eval(self, self.cavalier_eval), jeu.retourne_eval(self, self.reine_eval), jeu.retourne_eval(self, self.fou_eval), jeu.retourne_eval(self, self.pion_eval), jeu.retourne_eval(self, self.roi_eval)

    def retourne_eval(self,table):
        table_inverse = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]
        for table_col in range(len(table)):
            for table_lig in range(len(table[table_col])):
                table_inverse[7 - table_col][7 - table_lig] = table[table_col][table_lig]
        return table_inverse







    # Création du Damier

    def rafraichir_damier(self):
        self.Plateau.create_rectangle(self.marge_i - 2, self.marge_j - 2, self.cote + self.marge_i + 2, self.cote + self.marge_j + 2, fill='light gray',
                                 tag='Prom')
        for l in range(self.NB_DE_CASES):
            for k in range(self.NB_DE_CASES):
                if (k + l) % 2 == 0:
                    self.Plateau.create_rectangle(self.marge_i + l * self.pas, self.marge_j + k * self.pas, self.marge_i + (l + 1) * self.pas,
                                             self.marge_j + (k + 1) * self.pas, fill='black', tag='Prom')
                else:
                    self.Plateau.create_rectangle(self.marge_i + l * self.pas, self.marge_j + k * self.pas, self.marge_i + (l + 1) * self.pas,
                                             self.marge_j + (k + 1) * self.pas, fill='white', tag='Prom')


    # fonction permettant d'afficher les pièces
    def dessiner(self,img, couleur, x, y, Id):
        if couleur == self.B:
            self.Plateau.create_image(self.marge_i + self.pas / 2 + self.pas * x, self.marge_j + self.pas / 2 + self.pas * y, image=self.B[img], tags='del')
        else:
            self.Plateau.create_image(self.marge_i + self.pas / 2 + self.pas * x, self.marge_j + self.pas / 2 + self.pas * y, image=self.N[img], tags='del')


    # permet de Rafraichir le Plateau
    def afficher(self):
        for i in range(self.NB_DE_CASES):
            for j in range(self.NB_DE_CASES):
                Id = self.Base[i][j]
                if Id != 0:
                    if Id < 100:
                        color = self.B
                        ID = Id
                    else:
                        color = self.N
                        ID = Id - 100
                    if ID < 10:
                        img = 0
                    elif ID < 20:
                        img = 1
                    elif ID < 30:
                        img = 2
                    elif ID < 40:
                        img = 3
                    elif ID < 50:
                        img = 4
                    else:
                        img = 5
                    jeu.dessiner(self,img, color, j, i, Id)


    def Update(self):
        d = self.Plateau.find_withtag('del')
        for i in range(len(d)):
            t = d[i]
            self.Plateau.delete(t)
        jeu.afficher(self)


    # Création de la situation de Départ:
    StartBase = [[11, 31, 21, 1, 41, 22, 32, 12], [51, 52, 53, 54, 55, 56, 57, 58], [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                 [151, 152, 153, 154, 155, 156, 157, 158], [111, 131, 121, 101, 141, 122, 132, 112]]

    Base = [[11, 31, 21, 1, 41, 22, 32, 12], [51, 52, 53, 54, 55, 56, 57, 58], [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
            [151, 152, 153, 154, 155, 156, 157, 158], [111, 131, 121, 101, 141, 122, 132, 112]]




    def rejouer(self):
        for i in range(self.NB_DE_CASES):
            for j in range(self.NB_DE_CASES):
                self.Base[i][j] = self.StartBase[i][j]
        jeu.Update(self)
        self.Statut.clear()
        self.mb.clear()
        self.mn.clear()
        self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(1) + ": Blanc", font='Bold',
                            tags='del')
        d = self.Plateau.find_withtag('rej')
        for i in range(len(d)):
            t = d[i]
            self.Plateau.delete(t)
        h = self.Plateau.find_withtag('de')
        for i in range(len(h)):
            g = h[i]
            self.Plateau.delete(g)
        connection = sqlite3.connect("jeu_d'échec.db")
        curseur = connection.cursor()
        curseur.execute("drop table if exists partie")
        curseur.execute("create table partie (n°coup, id_piece, id_prise,col_depart,lig_depart,col_arrivé,lig_arrivé,temp_jeu)")
        connection.commit()
        connection.close()


    # création du Menu
    def fin(self):
        self.fen.destroy()


    def retour(self):
        tour = 0
        for i in self.Statut:
            tour += self.Statut[i]
        if tour > 0:
            connection = sqlite3.connect("jeu_d'échec.db")
            curseur = connection.cursor()
            curseur.execute("SELECT * FROM partie WHERE n°coup=?", (tour,))
            info = curseur.fetchall()
            (t, Id, prise, x, y, d_x, d_y,temp) = info[0]
            self.Base[y][x] = Id
            self.Base[d_y][d_x] = prise
            if prise > 100:
                j = 0
                for i in range(len(self.mn)):
                    i -= j
                    if self.mn[i] == prise:
                        self.mn.pop(i)
                        j = 1

                        continue
            elif 100 > prise > 0:
                j = 0
                for i in range(len(self.mb)):
                    i -= j
                    if self.mb[i] == prise:
                        self.mb.pop(i)
                        j = 1

                        continue
            if self.Statut[Id] == 1:
                self.Statut.pop(Id)
            else:
                self.Statut[Id] -= 1
            d = self.Plateau.find_withtag('rej')
            for i in range(len(d)):
                t = d[i]
                self.Plateau.delete(t)
            for i in range(len(self.mn)):
                jeu.mort(self,self.mn[i], False)
            for i in range(len(self.mb)):
                jeu.mort(self,self.mb[i], False)
            d = self.Plateau.find_withtag('de')
            for i in range(len(d)):
                t = d[i]
                self.Plateau.delete(t)
            curseur.execute("DELETE FROM partie WHERE n°coup=?", (tour,))
            tour = 0
            for i in self.Statut:
                tour += self.Statut[i]
            if tour % 2 == 0:
                c_tour = "Blanc"
            else:
                c_tour = 'Noir'
            self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(tour + 1) + ":" + c_tour, font='Bold',
                                tags='de')
            connection.commit()
            connection.close()
            jeu.Update(self)
        else:
            tk.messagebox.showinfo("Commencez d'abord à jouer", "Vous n'avez joué aucun coup")


    def nombre_retour(self):
        playsound('Image/retour.wav')
        jeu.retour(self)



    def coord(self,Id):
        for i in range(self.NB_DE_CASES):
            for j in range(self.NB_DE_CASES):
                if self.Base[i][j] == Id:
                    fx, fy = j, i
                    return int(fx), int(fy)


    # crée la promotion
    def Promotion(self,cou, x, y, Bot):
        self.Plateau.pack_forget()

        def ajout_promu(self,promu):
            self.Plateau.pack()
            num = 1
            for i in range(self.NB_DE_CASES):
                for j in range(self.NB_DE_CASES):
                    couleut, imag = jeu.Tri(self,self.Base[j][i])
                    if self.Base[j][i] > 100:
                        couleurK = 'N'
                        if couleurK == cou and imag == promu and self.Base[j][i] > 0:
                            num = num + 1
                    elif 100 > self.Base[j][i] > 0:
                        couleurK = 'B'
                        if couleurK == cou and imag == promu and self.Base[j][i] > 0:
                            num = num + 1
            if cou == 'N':
                num = 100 + num
            if promu == 3:
                num = num + 30
            elif promu == 1:
                num = num + 10
            elif promu == 2:
                num = num + 20
            self.Base[y][x] = num
            jeu.rafraichir_damier(self)

            jeu.Update(self)
            couleut, imag = jeu.Tri(self,self.Base[y][x])
            if not Bot:
                for i in range(len(self.mb)):
                    jeu.mort(self,self.mb[i],False)
                for j in range(len(self.mn)):
                    jeu.mort(self,self.mn[j],False)
                jeu.check_echec(self,couleut, True)
                if jeu.check_echec(self,couleut, False):
                    jeu.check_echec_et_mat(self,couleut)
            playsound('Image/teleportation.mp3')

        if Bot:
            ajout_promu(self,0)
        else:
            deleted_1 = self.Plateau.find_withtag('de')
            for i in range(len(deleted_1)):
                t = deleted_1[i]
                self.Plateau.delete(t)
            deleted_2 = self.Plateau.find_withtag('Prom')
            for i in range(len(deleted_2)):
                t = deleted_2[i]
                self.Plateau.delete(t)
            deleted_3 = self.Plateau.find_withtag('rej')
            for i in range(len(deleted_3)):
                t = deleted_3[i]
                self.Plateau.delete(t)
            selected = tk.IntVar()
            s = ttk.Style()
            s.configure('Wild.TButton',
                        background='black',
                        foreground='white',
                        highlightthickness='20',
                        font=('Helvetica', 18, 'bold'))
            s.map('Wild.TButton',
                  foreground=[('pressed', 'red'),
                              ('active', 'blue')],
                  background=[('pressed', 'cyan'),
                              ('active', 'green')],
                  relief=[('pressed', 'groove'),
                          ('!pressed', 'ridge')])

            rad1 = ttk.Radiobutton(self.fen, style='Wild.TButton', text='Reine', value=1, variable=selected)

            rad2 = ttk.Radiobutton(self.fen, style='Wild.TButton', text='Tour', value=2, variable=selected)

            rad3 = ttk.Radiobutton(self.fen, text='Fou', style='Wild.TButton', value=3, variable=selected)

            rad4 = ttk.Radiobutton(self.fen, text='Cavalier', style='Wild.TButton', value=4, variable=selected)

            def clicked():
                rad1.destroy()
                rad2.destroy()
                rad3.destroy()
                rad4.destroy()
                btn.destroy()
                if selected.get() == 0:
                    self.Promotion(cou, x, y, Bot)
                else:
                    promu = selected.get() - 1
                    ajout_promu(self,promu)

            btn = ttk.Button(self.fen, style='Wild.TButton', text="Valider", command=clicked)

            rad1.pack(side='left')

            rad2.pack(side='left')

            rad3.pack(side='left')

            rad4.pack(side='left')

            btn.pack(side='bottom', pady=20)


    # selectionne une piece uniquement sur l'échequier et la deplace
    def Selectionner_une_piece(self,event):
        """
        :param event: choisis la pièce sur la case sélectionné
        :return: renvoie et affiche les coups possibles
        """
        d = self.Plateau.find_withtag('de')
        for i in range(len(d)):
            t = d[i]
            self.Plateau.delete(t)
        self.Cp.clear()
        self.Pp.clear()
        self.x_1.pop(0)
        self.y_1.pop(0)
        self.x_1.append(-3)
        self.y_1.append(-3)
        P = {}
        self.fen.unbind('<' + self.selection_piece + '>')
        jeu.Update(self)
        tour = 0
        for i in self.Statut:
            tour += self.Statut[i]
        if tour % 2 == 0:
            c_tour = "Blanc"
        else:
            c_tour = 'Noir'

        self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(tour + 1) + ":" + c_tour, font='Bold',
                            tags='de')
        a = self.Plateau.create_rectangle(self.marge_i + -4 * self.pas, self.marge_j + 12 * self.pas, self.marge_i + (-4 + 1) * self.pas,
                                     self.marge_j + (12 + 1) * self.pas,
                                     width=3, outline='Blue', tags='del')
        x0, y0 = event.x, event.y
        fx, fy, f_x, f_y = self.Plateau.coords(a)
        x, y = (x0 - self.marge_i) // self.pas, (y0 - self.marge_j) // self.pas
        fx, fy = ((fx - self.marge_i) // self.pas), (fy - self.marge_j) // self.pas
        dx, dy = x - fx, y - fy
        dx, dy = dx * self.pas, dy * self.pas
        self.Plateau.move(a, dx, dy)
        vx, vy, v_x, v_y = self.Plateau.coords(a)
        vx, vy, v_x, v_y = ((v_x - self.marge_i) // self.pas), (v_y - self.marge_j) // self.pas, ((v_x - self.marge_i) // self.pas), (
                v_y - self.marge_j) // self.pas
        if vx > 8 or vx < 1 or vy > 8 or vy < 1 or v_x > 8 or v_x < 0 or v_y > 8 or v_y < 0:
            self.Plateau.move(a, -dx, -dy)

        def move_event(event):
            self.fen.unbind('<' + self.deplacer_piece + '>')
            self.fen.unbind('<' + self.selection_piece + '>')
            P = {**self.Cp, **self.Pp}
            for i in P:
                (r, t) = P[i]
                if (r, t) == (self.x_1[0], self.y_1[0]):
                    ax, ay = event.x, event.y
                    ax, ay = ((ax - self.marge_i) // self.pas), (ay - self.marge_j) // self.pas
                    ay, ax = int(ay), int(ax)
                    jeu.move(self,y, x, ay, ax, True)

        def deplace(event):
            x1, y1 = event.x, event.y
            fx1, fy1, f_x1, f_y1 = self.marge_i + -8 * self.pas, self.marge_j + 16 * self.pas, self.marge_i + (-8 + 1) * self.pas, self.marge_j + (
                    16 + 1) * self.pas
            x1, y1 = (x1 - self.marge_i) // self.pas, (y1 - self.marge_j) // self.pas
            b = self.Plateau.create_rectangle(self.marge_i + -8 * self.pas, self.marge_j + 16 * self.pas, self.marge_i + (-8 + 1) * self.pas,
                                         self.marge_j + (16 + 1) * self.pas,
                                         width=3, outline='Green', tags='del')
            fx1, fy1 = ((fx1 - self.marge_i) // self.pas), (fy1 - self.marge_j) // self.pas
            dx1, dy1 = x1 - fx1, y1 - fy1
            dx1, dy1 = dx1 * self.pas, dy1 * self.pas
            P = {**self.Cp, **self.Pp}
            for i in P:
                (r, t) = P[i]
                if (r, t) == (x1, y1):
                    self.x_1.pop(0)
                    self.y_1.pop(0)
                    self.x_1.append(x1)
                    self.y_1.append(y1)
                    self.Plateau.move(b, dx1, dy1)
                    self.fen.bind('<' + self.deplacer_piece + '>', move_event)

            vx, vy, v_x, v_y = self.Plateau.coords(b)
            vx, vy, v_x, v_y = ((v_x - self.marge_i) // self.pas) + 1, (v_y - self.marge_j) // self.pas, ((v_x - self.marge_i) // self.pas) + 1, (
                    v_y - self.marge_j) // self.pas
            if vx > 9 or vx < 2 or vy > 8 or vy < 1 or v_x > 9 or v_x < 1 or v_y > 8 or v_y < 0:
                self.Plateau.move(b, -dx1, -dy1)
            self.fen.unbind('<' + self.selection_piece + '>')

            def redeplace(event):
                self.fen.unbind('<' + self.deplacer_piece + '>')
                x1, y1 = event.x, event.y
                fx1, fy1, f_x1, f_y1 = self.Plateau.coords(b)
                x1, y1 = (x1 - self.marge_i) // self.pas, (y1 - self.marge_j) // self.pas
                fx1, fy1 = ((fx1 - self.marge_i) // self.pas), (fy1 - self.marge_j) // self.pas
                dx1, dy1 = x1 - fx1, y1 - fy1
                dx1, dy1 = dx1 * self.pas, dy1 * self.pas
                P = {**self.Cp, **self.Pp}
                for i in P:
                    (r, t) = P[i]
                    if (r, t) == (x1, y1):
                        self.x_1.pop(0)
                        self.y_1.pop(0)
                        self.x_1.append(x1)
                        self.y_1.append(y1)
                        self.Plateau.move(b, dx1, dy1)
                        self.fen.bind('<' + self.deplacer_piece + '>', move_event)
                vx, vy, v_x, v_y = self.Plateau.coords(b)
                vx, vy, v_x, v_y = ((v_x - self.marge_i) // self.pas) + 1, (v_y - self.marge_j) // self.pas, ((v_x - self.marge_i) // self.pas) + 1, (
                        v_y - self.marge_j) // self.pas
                if vx > 9 or vx < 2 or vy > 8 or vy < 1 or v_x > 9 or v_x < 1 or v_y > 8 or v_y < 0:
                    self.Plateau.move(b, -dx1, -dy1)

            self.fen.bind('<' + self.selection_piece + '>', redeplace)

        if 0 <= x < 8 and 0 <= y < 8:
            x, y = int(x), int(y)
            Cs = self.Base[y][x]
            if tour % 2 == 0:
                if Cs < 100:
                    jeu.coup_possible(self,Cs, x, y, True)
                else:
                    self.Plateau.move(a, -dx, -dy)
            else:
                if Cs > 100:
                    jeu.coup_possible(self,Cs, x, y, True)
                else:
                    self.Plateau.move(a, -dx, -dy)
        if self.niveau_ordi[0] > 0:
            jeu.tour_suivant(self)
        self.fen.bind('<' + self.selection_piece + '>', deplace)


    # fonction qui permet de bouger les pièces:

    def move(self,start_y, start_x, end_y, end_x, joueur):
        """

        :param start_y: collone de la pièce
        :param start_x: ligne de la pièce
        :param end_y: collone de la case voulu
        :param end_x: ligne de la case voulu
        :param joueur: si c'est un joueur qui joue ou un ordinateur
        :return: affiche le plateau, les morts et met à jour la base de données ainsi que le statut des pièces
        """
        t = self.Base[start_y][start_x]
        d = self.Base[end_y][end_x]
        for i in range(len(self.rock_x)):
            o, k = self.rock_x[i], self.rock_y[i]
            if o == self.x_1[0] and k == self.y_1[0]:
                w, z, (u, v) = self.move_rock[(o, k)]
                self.Base[z][w] = self.Base[v][u]
                self.Base[v][u] = 0
        if self.x_1[0] == self.special_x[0] and self.y_1[0] == self.special_y[0]:
            d = self.Base[int(start_y)][int(self.x_1[0])]
            self.Base[int(start_y)][int(self.x_1[0])] = 0
        if t != 0 and t != d:
            self.Base[start_y][start_x] = 0
            self.Base[end_y][end_x] = t
            color, img = jeu.Tri(self,t)
            if color == self.B:
                ncolor = self.N
            else:
                ncolor = self.B
            if jeu.check_echec(self,ncolor, False):
                self.Base[end_y][end_x] = d
                self.Base[start_y][start_x] = t
                t = 0
                d = 0
                tk.messagebox.showinfo('Pièce Clouté', "En bougeant cette pièce vous mettez échec votre Roi")

            """ animation trés lourd
            p = Plateau.create_image(marge_i + pas / 2 + pas * x, marge_j + pas / 2 + pas * y,
                                     image=color[img])
            def deplace(p, x0, y0, x, y):
                def f(t):
                    return (1 - t) * x0 + t * x, (1 - t) * y0 + y * t
    
                t = [0]
    
                def bouge():
                    t[0] += 0.01
                    if t[0] <= 1:
                        x, y = f(t[0])
                        Plateau.coords(p, x, y)
                        fen.after(8, bouge)
    
                fen.after(8, bouge)
                """

            if 100 > t > 50:
                if end_y == 7:
                    jeu.Promotion(self,'B', end_x, end_y, False)
            elif t > 150:
                if end_y == 0:
                    jeu.Promotion(self,'N', end_x, end_y, True)
            jeu.add_statut(self,t)
            f = self.Plateau.find_withtag('de')
            for i in range(len(f)):
                e = f[i]
                self.Plateau.delete(e)
            tour = 0
            for i in self.Statut:
                tour += self.Statut[i]
            if tour % 2 == 0:
                c_tour = "Blanc"
            else:
                c_tour = 'Noir'

            self.Plateau.create_text(self.cote / 2 + self.marge_i, self.cote + self.marge_j * 3 / 2, text=str(tour + 1) + ":" + c_tour,
                                font='Bold', tags='de')
            connection = sqlite3.connect("jeu_d'échec.db")
            curseur = connection.cursor()

            if t > 0:
                if not joueur:
                    curseur.execute("insert into partie (n°coup, id_piece, id_prise,col_depart,lig_depart,col_arrivé,lig_arrivé,temp_jeu) values (?, ?, ?,?,?,?,?,?)",
                                (tour, t, d, start_x, start_y, end_x, end_y,0))
                if joueur:
                    curseur.execute(
                        "insert into partie (n°coup, id_piece, id_prise,col_depart,lig_depart,col_arrivé,lig_arrivé,temp_jeu) values (?, ?, ?,?,?,?,?,?)",
                            (tour, t, d, start_x, start_y, end_x, end_y, float(time.time()-self.temp_debut)))
            connection.commit()
            connection.close()
            self.dpiece.pop(0)
            self.dpiece.append(t)
            jeu.mort(self,d, True)
            if joueur:
                jeu.Update(self)
                self.temp_debut=time.time()
                playsound('Image/deplacement.wav')
                jeu.check_echec(self,color, True)
                if jeu.check_echec(self,color, False):
                    jeu.check_echec_et_mat(self,color)


    def tour_suivant(self):
        tour = 0
        for i in self.Statut:
            tour += self.Statut[i]
        if tour % 2 == 0:
            au_tour = "Blanc"
        else:
            au_tour = 'Noir'
        if au_tour == self.couleur_ordi[0]:
            if self.niveau_ordi[0] > 0:
                jeu.coup_IA(self)
        if self.niveau_ordi2[0] > 0:
            jeu.coup_IA(self)


    # Permet de savoir le nombre de coup jouer avec une piece
    def add_statut(self,Id):
        if Id > 0:
            if Id in self.Statut:
                self.Statut[Id] = self.Statut[Id] + 1

            else:
                self.Statut[Id] = 1


    def donne_valeur(self,piece):
        piece_x, piece_y = jeu.coord(self,piece)
        if piece == 0:
            return 0
        if 10 > piece > 0:
            return 90 + self.reine_eval_B[piece_y][piece_x]
        if 20 > piece > 10:
            return 50 + self.tour_eval_B[piece_y][piece_x]
        if 30 > piece > 20:
            return 30 + self.fou_eval_B[piece_y][piece_x]
        if 40 > piece > 30:
            return 30 + self.cavalier_eval_B[piece_y][piece_x]
        if 50 > piece > 40:
            return 900 + self.roi_eval_B[piece_y][piece_x]
        if 100 > piece > 50:
            return 10 + self.pion_eval_B[piece_y][piece_x]
        if 110 > piece > 100:
            return -90 + self.reine_eval_N[piece_y][piece_x]
        if 120 > piece > 110:
            return -50 + self.tour_eval_N[piece_y][piece_x]
        if 130 > piece > 120:
            return -30 + self.fou_eval_N[piece_y][piece_x]
        if 140 > piece > 130:
            return -30 + self.cavalier_eval_N[piece_y][piece_x]
        if 150 > piece > 140:
            return -900 + self.roi_eval_N[piece_y][piece_x]
        if 160 > piece > 150:
            return -10 + self.pion_eval_N[piece_y][piece_x]


    def valeur_plateau(self):
        valeur_plat = 0
        for lignes in range(self.NB_DE_CASES):
            for collones in range(self.NB_DE_CASES):
                valeur_plat += jeu.donne_valeur(self,self.Base[lignes][collones])
        return valeur_plat


    def meilleur_coup(self,coup):
        """

        :param coup:dictionnaire contenant tout les coups
        :return: le coup qui mange la piece de plus grande valeur
        """
        piece_IA = random.choice(list(coup.keys()))
        a, b = random.choice(self.tout_coup_possible[piece_IA])
        meilleur = (a, b)
        meilleur_score = -(jeu.valeur_plateau(self))
        meilleur_piece = int(piece_IA)
        for piece_test in coup:
            for coup_test in range(len(coup[piece_test])):
                test_x_depart, test_y_depart = jeu.coord(self,piece_test)
                test_x_arrive, test_y_arrive = coup[piece_test][coup_test]
                jeu.move(self,test_y_depart, test_x_depart, test_y_arrive, test_x_arrive, False)
                test_plateau = -(jeu.valeur_plateau(self))
                jeu.retour(self)
                if test_plateau > meilleur_score:
                    meilleur_score = test_plateau
                    meilleur = (test_x_arrive, test_y_arrive)
                    meilleur_piece = piece_test
        return meilleur, meilleur_piece


    def cloute(self,coup):
        """

        :param coup:verifie si ce deplacement ne met pas echec le roi
        :return: un dictionnaire sans coup mettant echec le roi
        """
        a_enlever = []
        color = 0
        for c in coup:
            j = 0
            for r in range(len(coup[c])):
                r -= j
                start_x, start_y = jeu.coord(self,c)
                end_x, end_y = coup[c][r]
                t = self.Base[start_y][start_x]
                d = self.Base[end_y][end_x]
                for i in range(len(self.rock_x)):
                    o, k = self.rock_x[i], self.rock_y[i]
                    if o == self.x_1[0] and k == self.y_1[0]:
                        w, z, (u, v) = self.move_rock[(o, k)]
                        self.Base[z][w] = self.Base[v][u]
                        self.Base[v][u] = 0
                if self.x_1[0] == self.special_x[0] and self.y_1[0] == self.special_y[0]:
                    d = self.Base[int(start_y)][int(self.x_1[0])]
                    self.Base[int(start_y)][int(self.x_1[0])] = 0
                if t != 0 and t != d:
                    self.Base[start_y][start_x] = 0
                    self.Base[end_y][end_x] = t
                    color, img = jeu.Tri(self,t)
                    if color == self.B:
                        ncolor = self.N
                    else:
                        ncolor = self.B
                    if jeu.check_echec(self,ncolor, False):
                        coup[c].pop(r)
                        j += 1
                    self.Base[end_y][end_x] = d
                    self.Base[start_y][start_x] = t
        for cop in coup:
            if coup[cop] == []:
                a_enlever.append(cop)
        for coup_vide in a_enlever:
            coup.pop(coup_vide)
        if len(coup) != 0:
            return coup
        else:
            if not jeu.check_echec(self,color, False):
                rejoue = tk.messagebox.askyesno('Egalité',
                                                'Pat(le joueur adverse ne peux pas bouger)\nVoulez-vous rejouer ?')
                if rejoue:
                    jeu.rejouer(self)
                    jeu.Update(self)
                else:
                    self.Plateau.quit()
            return 0


    def minimax_racine(self,profondeur, Maximiser_le_joueur, couleur_bot):
        """

        :param profondeur: sur combien de niveau la recherche des coups se fait
        :param Maximiser_le_joueur: si le joueur doit être avantagé ou non
        :param couleur_bot: la couleur joué
        :return: renvoie le coup evalué comme le meilleur
        """
        meilleur = tuple()
        meilleur_piece = int()
        meilleur_score_possible = -9999
        pouc_b = {}
        for col in range(self.NB_DE_CASES):
            for lig in range(self.NB_DE_CASES):
                if self.Base[col][lig] > 0:
                    co, image = jeu.Tri(self,self.Base[col][lig])
                    if co == couleur_bot:
                        coup_piece = []
                        jeu.coup_possible(self,self.Base[col][lig], lig, col, False)
                        for i in self.Cp:
                            coup_piece.append(self.Cp[i])
                        for i in self.Pp:
                            coup_piece.append((self.Pp[i]))
                        pouc_b[self.Base[col][lig]] = coup_piece
        coup_minimax_racine = pouc_b
        coup_minimax_racine_tri = jeu.cloute(self,coup_minimax_racine)
        for piece_test in coup_minimax_racine_tri:
            for coup_test in range(len(coup_minimax_racine_tri[piece_test])):
                test_x_depart, test_y_depart = jeu.coord(self,piece_test)
                test_x_arrive, test_y_arrive = coup_minimax_racine_tri[piece_test][coup_test]
                jeu.move(self,test_y_depart, test_x_depart, test_y_arrive, test_x_arrive, False)
                valeur = jeu.minimax(self,profondeur - 1, Maximiser_le_joueur, -10000, 10000, couleur_bot)
                jeu.retour(self)
                if valeur > meilleur_score_possible:
                    meilleur_score_possible = valeur
                    meilleur = (test_x_arrive, test_y_arrive)
                    meilleur_piece = piece_test
        return meilleur, meilleur_piece


    def minimax(self,profondeur, Maximiser_le_joueur, alpha, beta, couleur_bot):
        """
        :param profondeur:calcule les branches suivantes ou donne la valeur des coups
        :param Maximiser_le_joueur:cherche le meilleur coup ou le pire coup
        :param alpha:permet d'enlever les coups peu avantageux de l'arboresance
        :param beta:permet d'enlever les coups peu avantageux de l'arboresance
        :param couleur_bot:couleur de l'ordi
        :return:la valeur du plateau si on est la profondeur max sinon fait un coup de plus
        """
        if profondeur == 0:
            if couleur_bot == self.N:
                return -jeu.valeur_plateau(self)
            elif couleur_bot == self.B:
                return jeu.valeur_plateau(self)

        if Maximiser_le_joueur:
            pouc_minimax_N = {}
            for col in range(self.NB_DE_CASES):
                for lig in range(self.NB_DE_CASES):
                    if self.Base[col][lig] > 0:
                        co, image = jeu.Tri(self,self.Base[col][lig])
                        if co == couleur_bot:
                            coup_piece = []
                            jeu.coup_possible(self,self.Base[col][lig], lig, col, False)
                            for i in self.Cp:
                                coup_piece.append(self.Cp[i])
                            for i in self.Pp:
                                coup_piece.append((self.Pp[i]))
                            pouc_minimax_N[self.Base[col][lig]] = coup_piece
            coup_minimax_N = pouc_minimax_N
            pouc_N = jeu.cloute(self,coup_minimax_N)
            meilleur_score_po = -9999
            if pouc_N != 0:
                for piece_test1 in pouc_N:
                    for coup_test1 in range(len(pouc_N[piece_test1])):
                        Maximiser_le_joueur = not Maximiser_le_joueur
                        test_x_depart1, test_y_depart1 = jeu.coord(self,piece_test1)
                        test_x_arrive1, test_y_arrive1 = pouc_N[piece_test1][coup_test1]
                        mort_remettre = self.Base[test_y_arrive1][test_x_arrive1]
                        if mort_remettre != 41 and mort_remettre != 141:
                            self.Base[test_y_arrive1][test_x_arrive1] = piece_test1
                            self.Base[test_y_depart1][test_x_depart1] = 0
                            meilleur_score_po = max(meilleur_score_po,
                                                    jeu.minimax(self,profondeur - 1, Maximiser_le_joueur, alpha, beta, couleur_bot))
                            # move(test_y_depart1, test_x_depart1, test_y_arrive1, test_x_arrive1,False)
                            self.Base[test_y_arrive1][test_x_arrive1] = mort_remettre
                            self.Base[test_y_depart1][test_x_depart1] = piece_test1
                            # retour()
                        else:
                            meilleur_score_po = max(meilleur_score_po,
                                                    jeu.minimax(self,profondeur - 1, Maximiser_le_joueur, alpha, beta, couleur_bot))
                        alpha = max(alpha, meilleur_score_po)
                        if beta <= alpha:
                            return meilleur_score_po
            return meilleur_score_po
        else:
            pouc_minimax_B = {}
            for col in range(self.NB_DE_CASES):
                for lig in range(self.NB_DE_CASES):
                    if self.Base[col][lig] > 0:
                        co, image = jeu.Tri(self,self.Base[col][lig])
                        if co != couleur_bot:
                            coup_piece = []
                            jeu.coup_possible(self,self.Base[col][lig], lig, col, False)
                            for i in self.Cp:
                                coup_piece.append(self.Cp[i])
                            for i in self.Pp:
                                coup_piece.append((self.Pp[i]))
                            pouc_minimax_B[self.Base[col][lig]] = coup_piece
            coup_minimax_B = pouc_minimax_B
            pouc_B = jeu.cloute(self,coup_minimax_B)
            meilleur_score_po1 = 9999
            if pouc_B != 0:
                for piece_test2 in pouc_B:
                    for coup_test2 in range(len(pouc_B[piece_test2])):
                        Maximiser_le_joueur = not Maximiser_le_joueur
                        test_x_depart2, test_y_depart2 = jeu.coord(self,piece_test2)
                        test_x_arrive2, test_y_arrive2 = pouc_B[piece_test2][coup_test2]
                        mort_a_remettre = self.Base[test_y_arrive2][test_x_arrive2]
                        if mort_a_remettre != 41 and mort_a_remettre != 141:
                            # move(test_y_depart2, test_x_depart2, test_y_arrive2, test_x_arrive2,False)
                            self.Base[test_y_arrive2][test_x_arrive2] = piece_test2
                            self.Base[test_y_depart2][test_x_depart2] = 0
                            meilleur_score_po1 = min(meilleur_score_po1,
                                                     jeu.minimax(self,profondeur - 1, Maximiser_le_joueur, alpha, beta, couleur_bot))
                            self.Base[test_y_arrive2][test_x_arrive2] = mort_a_remettre
                            self.Base[test_y_depart2][test_x_depart2] = piece_test2
                            # retour()
                        else:
                            meilleur_score_po1 = min(meilleur_score_po1,
                                                     jeu.minimax(self,profondeur - 1, Maximiser_le_joueur, alpha, beta, couleur_bot))
                        beta = min(beta, meilleur_score_po1)
                        if beta <= alpha:
                            return meilleur_score_po1
            return meilleur_score_po1


    # fait jouer l'IA
    def coup_IA(self):
        """

        :return: choisis la bonne fonction suivant le niveau du bot
        """
        if self.niveau_ordi2[0] < 0:
            if self.couleur_ordi[0] == "Noir":
                couleur_bot = self.N
            else:
                couleur_bot = self.B
        else:
            tour = 0
            for i in self.Statut:
                tour += self.Statut[i]
            if tour % 2 == 0:
                couleur_bot = self.B
            else:
                couleur_bot = self.N
        coup = jeu.tout_coup(self,couleur_bot)
        coup_trie = jeu.cloute(self,coup)
        if self.niveau_ordi[0] == 4:
            """Bot niveau 4"""
            if type(coup_trie) == dict:
                (best_a, best_b), meilleur_piece = jeu.minimax_racine(self,3, True, couleur_bot)
                best_x, best_y = jeu.coord(self,meilleur_piece)
                jeu.move(self,best_y, best_x, best_b, best_a, True)
        if self.niveau_ordi[0] == 3:
            """Bot niveau 3"""
            if type(coup_trie) == dict:
                (best_a, best_b), meilleur_piece = jeu.minimax_racine(self,2, True, couleur_bot)
                best_x, best_y = jeu.coord(self,meilleur_piece)
                jeu.move(self,best_y, best_x, best_b, best_a, True)
        if self.niveau_ordi[0] == 2:
            """Bot niveau 2:"""
            if type(coup_trie) == dict:
                (best_a, best_b), meilleur_piece = jeu.meilleur_coup(self,coup_trie)
                best_x, best_y = jeu.coord(self,meilleur_piece)
                jeu.move(self,best_y, best_x, best_b, best_a, True)
        if self.niveau_ordi[0] == 1:
            """Bot niveau 1:"""
            if type(coup_trie) == dict:
                piece_IA = random.choice(list(coup_trie.keys()))
                a, b = random.choice(self.tout_coup_possible[piece_IA])
                x, y = jeu.coord(self,piece_IA)
                jeu.move(self,y, x, b, a, True)


    # regarde si il y a echec par une piece couleur
    def check_echec(self,couleur, pop_up):
        """

        :param couleur: couleur qui mettrait echec
        :param pop_up: affiche une pop_up ou non
        :return: indique si la couelur est echec a l'aide d'un booléen
        """
        echec = False
        for k in range(self.NB_DE_CASES):
            for j in range(self.NB_DE_CASES):
                coul, img = jeu.Tri(self,self.Base[k][j])
                if coul == couleur:
                    Test = self.Base[k][j]
                    x, y = jeu.coord(self,Test)
                    jeu.coup_possible(self,Test, x, y, False)
                    for i in self.Pp:
                        (tx, ty) = self.Pp[i]
                        if couleur == self.B:
                            if self.Base[ty][tx] == 141:
                                echec = True
                                if pop_up:
                                    tk.messagebox.showwarning('Attention', 'Vous êtes en échec')
                        elif couleur == self.N:
                            if self.Base[ty][tx] == 41:
                                echec = True
                                if pop_up:
                                    tk.messagebox.showwarning('Attention', 'Vous êtes en échec')

        return echec


    # regarde l'échec et mat
    def check_echec_et_mat(self,couleur):
        echec = 0
        test = 0
        for i in range(self.NB_DE_CASES):
            for j in range(self.NB_DE_CASES):
                piece_test = self.Base[j][i]
                col, im = jeu.Tri(self,piece_test)
                if col != couleur:
                    jeu.coup_possible(self,piece_test, i, j, False)
                    P = {**self.Cp, **self.Pp}
                    for coup in P:
                        test = test + 1
                        (x, y) = P[coup]
                        piece_prise = self.Base[y][x]
                        self.Base[y][x] = piece_test
                        self.Base[j][i] = 0
                        if jeu.check_echec(self,couleur, False):
                            echec = echec + 1
                        self.Base[j][i] = piece_test
                        self.Base[y][x] = piece_prise
        if test == echec:

            if couleur == self.B:
                tk.messagebox.showinfo('Fin de Partie', 'Les Blancs remportent la partie')
                playsound('Image/fin.mp3')
            else:
                tk.messagebox.showinfo('Fin de Partie', 'Les Noirs remportent la partie')
                playsound('Image/fin.mp3')
            rejoue = tk.messagebox.askyesno('Rejouez ?', 'Voulez-vous rejouer ?')
            if rejoue:
                jeu.rejouer(self)
                jeu.Update(self)
            else:
                self.Plateau.quit()


    # calcul des coups possibles
    def tout_coup(self,couleur):
        self.tout_coup_possible.clear()
        for col in range(self.NB_DE_CASES):
            for lig in range(self.NB_DE_CASES):
                if self.Base[col][lig] > 0:
                    co, image = jeu.Tri(self,self.Base[col][lig])
                    if co == couleur:
                        coup_piece = []
                        jeu.coup_possible(self,self.Base[col][lig], lig, col, False)
                        for i in self.Cp:
                            coup_piece.append(self.Cp[i])
                        for i in self.Pp:
                            coup_piece.append((self.Pp[i]))
                        self.tout_coup_possible[self.Base[col][lig]] = coup_piece
        return self.tout_coup_possible


    # affiche les pieces sur le côté

    def mort(self,Id, add):
        couleur, img = jeu.Tri(self,Id)
        if Id > 0:
            if couleur == self.B:
                if add:
                    self.mb.append(Id)
                for i in range(len(self.mb)):
                    if self.mb[i] == Id:
                        self.Plateau.create_image(self.marge_i * 1 / 4 + self.marge_i * (i % 2 / 2),
                                             self.marge_j * 2 + (i // 2) * self.pas, image=couleur[img],
                                             tags='rej')
            else:
                if add:
                    self.mn.append(Id)
                for j in range(len(self.mn)):
                    if self.mn[j] == Id:
                        self.Plateau.create_image(self.marge_i * 5 / 4 + self.cote + self.marge_i * (j % 2 / 2), self.marge_j * 2 + (j // 2) * self.pas,
                                             image=couleur[img], tags='rej')


    def Tri(self,Id):
        if Id < 100:
            color = self.B
            ID = Id
        else:
            color = self.N
            ID = Id - 100
        if ID < 10:
            img = 0
        elif ID < 20:
            img = 1
        elif ID < 30:
            img = 2
        elif ID < 40:
            img = 3
        elif ID < 50:
            img = 4
        else:
            img = 5
        return color, img


    # tri les pieces
    def coup_possible(self,Id, x, y, dessine):
        """

        :param Id: la pièces sélectionnés
        :param x: sa ligne
        :param y: sa collone
        :param dessine: si on veut afficher les coups possibles ou non
        :return: les coups de la pièce et les "affiches" si voulus
        """
        self.rock_x.clear()
        self.rock_y.clear()
        if 0 <= x < 8 and 0 <= y < 8:
            if Id > 0:
                couleur, img = jeu.Tri(self,Id)
                if img == 0:
                    jeu.coup_possible_Reine(self,couleur, x, y, dessine)
                elif img == 1:
                    jeu.coup_possible_Tour(self,couleur, x, y, Id, dessine)
                elif img == 2:
                    jeu.coup_possible_Fou(self,couleur, x, y, dessine)
                elif img == 3:
                    jeu.coup_possible_Cavalier(self,couleur, x, y, dessine)
                elif img == 4:
                    jeu.coup_possible_Roi(self,couleur, x, y, Id, dessine)
                else:
                    jeu.coup_possible_Pion(self,couleur, x, y, Id, dessine)
            else:
                self.Cp.clear()
                self. Pp.clear()


    # Coup par pieces
    def coup_possible_Reine(self,couleur, x, y, dessine):
        Cp_x, Cp_y = [], []
        a, b, c, d, e, f, g, h = 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(1, 8):
            if x + i < 8 and y + i < 8 and e != 1:
                if self.Base[y + i][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y + i)
                    e = 1
            if y + i < 8 and x - i >= 0 and f != 1:
                if self.Base[y + i][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y + i)
                    f = 1
            if x + i < 8 and y - i >= 0 and g != 1:
                if self.Base[y - i][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y - i)
                    g = 1
            if y - i >= 0 and x - i >= 0 and h != 1:
                if self.Base[y - i][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y - i)
                    h = 1
            if x + i < 8 and a != 1:
                if self.Base[y][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y)
                    a = 1
            if y + i < 8 and b != 1:
                if self.Base[y + i][x] == 0:
                    Cp_x.append(x)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x)
                    Cp_y.append(y + i)
                    b = 1
            if x - i >= 0 and c != 1:
                if self.Base[y][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y)
                    c = 1
            if y - i >= 0 and d != 1:
                if self.Base[y - i][x] == 0:
                    Cp_x.append(x)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x)
                    Cp_y.append(y - i)
                    d = 1
        jeu.check_libre(self,couleur, Cp_x, Cp_y, dessine, False)


    def coup_possible_Tour(self,couleur, x, y, Id, dessine):
        Cp_x, Cp_y = [], []
        a, b, c, d = 0, 0, 0, 0
        for i in range(1, 8):
            if x + i < 8 and a != 1:
                if self.Base[y][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y)
                    a = 1
            if y + i < 8 and b != 1:
                if self.Base[y + i][x] == 0:
                    Cp_x.append(x)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x)
                    Cp_y.append(y + i)
                    b = 1
            if x - i >= 0 and c != 1:
                if self.Base[y][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y)
                    c = 1
            if y - i >= 0 and d != 1:
                if self.Base[y - i][x] == 0:
                    Cp_x.append(x)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x)
                    Cp_y.append(y - i)
                    d = 1
        if dessine:
            jeu.check_Rock(self,Id)
        jeu.check_libre(self,couleur, Cp_x, Cp_y, dessine, False)


    def coup_possible_Fou(self,couleur, x, y, dessine):
        Cp_x, Cp_y = [], []
        e, f, g, h = 0, 0, 0, 0
        for i in range(1, 8):
            if x + i < 8 and y + i < 8 and e != 1:
                if self.Base[y + i][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y + i)
                    e = 1
            if y + i < 8 and x - i >= 0 and f != 1:
                if self.Base[y + i][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y + i)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y + i)
                    f = 1
            if x + i < 8 and y - i >= 0 and g != 1:
                if self.Base[y - i][x + i] == 0:
                    Cp_x.append(x + i)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x + i)
                    Cp_y.append(y - i)
                    g = 1
            if y - i >= 0 and x - i >= 0 and h != 1:
                if self.Base[y - i][x - i] == 0:
                    Cp_x.append(x - i)
                    Cp_y.append(y - i)
                else:
                    Cp_x.append(x - i)
                    Cp_y.append(y - i)
                    h = 1
        jeu.check_libre(self,couleur, Cp_x, Cp_y, dessine, False)


    def coup_possible_Cavalier(self,couleur, x, y, dessine):
        Cp_x, Cp_y = [], []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i != 0 and j != 0:
                    if i + j == 3 or (i + j) == -3 or (i + j) == -1 or (i + j) == 1:
                        if 0 <= x + i < 8 and 0 <= y + j < 8:
                            Cp_x.append(x + i)
                            Cp_y.append(y + j)
        jeu.check_libre(self,couleur, Cp_x, Cp_y, dessine, False)


    def check_Rock(self,Id):
        x, y = jeu.coord(self,Id)
        for i in range(len(self.rock_y)):
            self.rock_x.pop(len(self.rock_x) - i - 1)
            self.rock_y.pop(len(self.rock_y) - i - 1)
        col, img = jeu.Tri(self,Id)
        if col == self.B:
            echec = jeu.check_echec(self,self.N, False)
        else:
            echec = jeu.check_echec(self,self.B, False)
        if not echec:
            if Id == 141:
                if 111 not in self.Statut and Id not in self.Statut:
                    if self.Base[7][1] == 0 and self.Base[7][2] == 0 and self.Base[7][3] == 0:
                        self.Base[7][1], self.Base[7][2], self.Base[7][3] = Id, Id, Id
                        if not self.check_echec(self.B, False):
                            self.rock_x.append(2)
                            self.rock_y.append(7)
                            self.move_rock[(2, 7)] = (3, 7, jeu.coord(self,111))
                        self.Base[7][1], self.Base[7][2], self.Base[7][3] = 0, 0, 0
                if Id not in self.Statut and 112 not in self.Statut:
                    if self.Base[7][5] == 0 and self.Base[7][6] == 0:
                        self.Base[7][5], self.Base[7][6] = Id, Id
                        if not jeu.check_echec(self,self.B, False):
                            self.rock_x.append(6)
                            self.rock_y.append(7)
                            self.move_rock[(6, 7)] = (5, 7, jeu.coord(self,112))
                        self.Base[7][5], self.Base[7][6] = 0, 0

            elif Id == 41:
                if 11 not in self.Statut and Id not in self.Statut:
                    if self.Base[0][1] == 0 and self.Base[0][2] == 0 and self.Base[0][3] == 0:
                        self.Base[0][1], self.Base[0][2], self.Base[0][3] = Id, Id, Id
                        if not jeu.check_echec(self,self.N, False):
                            self.rock_x.append(2)
                            self.rock_y.append(0)
                            self.move_rock[(2, 0)] = (3, 0, jeu.coord(self,11))
                        self.Base[0][1], self.Base[0][2], self.Base[0][3] = 0, 0, 0

                if 12 not in self.Statut and Id not in self.Statut:
                    if self.Base[0][5] == 0 and self.Base[0][6] == 0:
                        self.Base[0][5], self.Base[0][6] = Id, Id
                        if not jeu.check_echec(self,self.N, False):
                            self.rock_x.append(6)
                            self.rock_y.append(0)
                            self.move_rock[(6, 0)] = (self,5, 0, jeu.coord(self,12))
                        self.Base[0][5], self.Base[0][6] = 0, 0


    def coup_possible_Roi(self,couleur, x, y, Id, dessine):
        Cp_x, Cp_y = [], []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if 0 <= x + i < 8 and 0 <= y + j < 8:
                        Cp_x.append(x + i)
                        Cp_y.append(y + j)
        if dessine:
            jeu.check_Rock(self,Id)
        jeu.check_libre(self,couleur, Cp_x, Cp_y, dessine, True)


    def coup_possible_Pion(self,couleur, x, y, Id, dessine):
        self.Pp.clear()
        self.Cp.clear()
        Cp_x, Cp_y = [], []
        P_x, P_y = [], []
        d = 1
        self.roi_x[0], self.roi_y[0] = -2, -2

        def coup_pion(d):
            if couleur == self.B:
                Cp_x.append(x)
                Cp_y.append(y + d)
            else:
                Cp_x.append(x)
                Cp_y.append(y - d)

        coup_pion(1)
        if Id not in self.Statut:
            d = 2
            coup_pion(d)

        def prisse_en_passant(couleur, Id):
            self.special_x[0], self.special_y[0] = -2, -2
            x, y = jeu.coord(self,Id)
            if couleur == self.N:
                if y == 3:
                    if x - 1 >= 0:
                        if 50 <= self.Base[y][x - 1] < 60:
                            if self.Base[y][x - 1] in self.Statut:
                                if self.Statut[self.Base[y][x - 1]] == 1 and self.dpiece[0] == self.Base[y][x - 1]:
                                    self.special_x.pop(0)
                                    self.special_y.pop(0)
                                    self.special_x.append(x - 1)
                                    self.special_y.append(y - 1)
                    if x + 1 < 8:
                        if 50 <= self.Base[y][x + 1] < 60:
                            if self.Base[y][x + 1] in self.Statut:
                                if self.Statut[self.Base[y][x + 1]] == 1 and self.dpiece[0] == self.Base[y][x + 1]:
                                    self.special_x.pop(0)
                                    self.special_y.pop(0)
                                    self.special_x.append(x + 1)
                                    self.special_y.append(y - 1)
            else:
                if y == 4:
                    if x - 1 >= 0:
                        if 150 <= self.Base[y][x - 1] < 160:
                            if self.Base[y][x - 1] in self.Statut:
                                if self.Statut[self.Base[y][x - 1]] == 1 and self.dpiece[0] == self.Base[y][x - 1]:
                                    self.special_x.pop(0)
                                    self.special_y.pop(0)
                                    self.special_x.append(x - 1)
                                    self.special_y.append(y + 1)
                    if x + 1 < 8:
                        if 150 <= self.Base[y][x + 1] < 160:
                            if self.Base[y][x + 1] in self.Statut:
                                if self.Statut[self.Base[y][x + 1]] == 1 and self.dpiece[0] == self.Base[y][x + 1]:
                                    self.special_x.pop(0)
                                    self.special_y.pop(0)
                                    self.special_x.append(x + 1)
                                    self.special_y.append(y + 1)

        if couleur == self.B:
            if x + 1 < 8 and y + 1 < 8:
                if self.Base[y + 1][x + 1] == 141:
                    self.roi_x.pop(0)
                    self.roi_y.pop(0)
                    self.roi_x.append(x + 1)
                    self.roi_y.append(y + 1)
                if self.Base[y + 1][x + 1] != 0 and self.Base[y + 1][x + 1] > 100 and self.Base[y + 1][x + 1] != 141:
                    P_x.append(x + 1)
                    P_y.append(y + 1)
            if x - 1 >= 0 and y + 1 < 8:
                if self.Base[y + 1][x - 1] == 141:
                    self.roi_x.pop(0)
                    self.roi_y.pop(0)
                    self.roi_x.append(x - 1)
                    self.roi_y.append(y + 1)
                if self.Base[y + 1][x - 1] != 0 and self.Base[y + 1][x - 1] > 100 and self.Base[y + 1][x - 1] != 141:
                    P_x.append(x - 1)
                    P_y.append(y + 1)
        else:
            if x + 1 < 8 and y - 1 >= 0:
                if self.Base[y - 1][x + 1] == 41:
                    self.roi_x.pop(0)
                    self.roi_y.pop(0)
                    self.roi_x.append(x + 1)
                    self.roi_y.append(y - 1)
                if self.Base[y - 1][x + 1] != 0 and self.Base[y - 1][x + 1] < 100 and self.Base[y - 1][x + 1] != 41:
                    P_x.append(x + 1)
                    P_y.append(y - 1)
            if x - 1 >= 0 and y - 1 >= 0:
                if self.Base[y - 1][x - 1] == 41:
                    self.roi_x.pop(0)
                    self.roi_y.pop(0)
                    self.roi_x.append(x - 1)
                    self.roi_y.append(y - 1)

                if self.Base[y - 1][x - 1] != 0 and self.Base[y - 1][x - 1] < 100 and self.Base[y - 1][x - 1] != 41:
                    P_x.append(x - 1)
                    P_y.append(y - 1)
        Cp1_x = list(Cp_x)
        Cp1_y = list(Cp_y)
        j = -1
        for i in range(len(Cp_x)):
            x, y = Cp_x[i], Cp_y[i]
            j = j + 1
            if d == 2:
                if couleur == self.B:
                    if self.Base[y][x] != 0 and self.Base[(y - 1)][x] == Id and self.Base[y + 1][x] != 0:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                    if self.Base[(y - 1)][x] != Id and self.Base[(y - 1)][x] != 0 and self.Base[y][x] == 0:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        Cp1_x.pop(j - 1)
                        Cp1_y.pop(j - 1)
                        j = j - 2
                    if self.Base[y][x] != 0 and self.Base[(y - 2)][x] == Id:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                elif couleur == self.N:
                    if self.Base[y][x] != 0 and self.Base[(y + 1)][x] == Id and self.Base[y - 1][x] != 0:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                    if self.Base[(y + 1)][x] != Id and self.Base[(y + 1)][x] != 0 and self.Base[y][x] == 0:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        Cp1_x.pop(j - 1)
                        Cp1_y.pop(j - 1)
                        j = j - 2
                    if self.Base[y][x] != 0 and self.Base[(y + 2)][x] == Id:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
            else:
                if 0 <= y < 8 and 0 <= x < 8:
                    if self.Base[y][x] != 0:
                        Cp1_x.pop(i)
                        Cp1_y.pop(i)
                if 0 > y or y > 7 or 0 > x or x > 7:
                    Cp1_x.pop(i)
                    Cp1_y.pop(i)
        prisse_en_passant(couleur, Id)
        if self.special_y[0] != -2:
            P_x = P_x + self.special_x
            P_y = P_y + self.special_y
        if not dessine and self.roi_x[0] != -2:
            P_x = P_x + self.roi_x
            P_y = P_y + self.roi_y
        for i in range(len(Cp1_x)):
            self.Cp[i] = (Cp1_x[i], Cp1_y[i])
        for i in range(len(P_x)):
            self.Pp[(100 + i)] = (P_x[i], P_y[i])
        if dessine:
            jeu.Pastille(self,'Red', Cp1_x, Cp1_y)
            jeu.Pastille(self,'Blue', P_x, P_y)


    # verifie si les cases sont libres
    def check_libre(self,couleur, Cp_x, Cp_y, dessine, roi):
        """

        :param couleur: couleur de la pièce
        :param Cp_x: les coordonnées en lignes des coups
        :param Cp_y: les coordonnées en collones des coups
        :param dessine: si on l'affiche ou non
        :param roi: regarde les paramètres du roi
        :return: repartie les coups en 3 catégories: prises, déplacement, impossible
        """
        self.Pp.clear()
        self.Cp.clear()
        Pp_x = []
        Pp_y = []
        Cp1_x = list(Cp_x)
        Cp1_y = list(Cp_y)
        j = -1
        self.roi_x[0], self.roi_y[0] = -2, -2
        for i in range(len(Cp_x)):
            x, y = Cp_x[i], Cp_y[i]
            j = j + 1
            if self.Base[y][x] != 0:
                if couleur == self.B:
                    if self.Base[y][x] == 141:
                        self.roi_x.pop(0)
                        self.roi_y.pop(0)
                        self.roi_x.append(x)
                        self.roi_y.append(y)
                    if self.Base[y][x] > 100 and self.Base[y][x] != 141:
                        Pp_x.append(Cp1_x[j])
                        Pp_y.append(Cp1_y[j])
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                    else:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                else:
                    if self.Base[y][x] == 41:
                        self.roi_x.pop(0)
                        self.roi_y.pop(0)
                        self.roi_x.append(x)
                        self.roi_y.append(y)
                    if self.Base[y][x] < 100 and self.Base[y][x] != 41:
                        Pp_x.append(Cp1_x[j])
                        Pp_y.append(Cp1_y[j])
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
                    else:
                        Cp1_x.pop(j)
                        Cp1_y.pop(j)
                        j = j - 1
        if not dessine and self.roi_x[0] != -2:
            Pp_x = Pp_x + self.roi_x
            Pp_y = Pp_y + self.roi_y
        if dessine:
            Cp_xy, x, y = [], [1], [1]
            for i in range(len(Cp1_x)):
                Cp_xy.append((Cp1_x[i], Cp1_y[i]))
            for j in range(len(self.rock_x)):
                x.pop(0)
                y.pop(0)
                x.append(self.rock_x[j])
                y.append(self.rock_y[j])
                if (x[0], y[0]) not in Cp_xy:
                    Cp1_x = Cp1_x + x
                    Cp1_y = Cp1_y + y
        for i in range(len(Cp1_x)):
            self.Cp[i] = (Cp1_x[i], Cp1_y[i])
        for i in range(len(Pp_x)):
            self.Pp[(100 + i)] = (Pp_x[i], Pp_y[i])
        if dessine:
            jeu.Pastille(self,'Red', Cp1_x, Cp1_y)
            jeu.Pastille(self,'Blue', Pp_x, Pp_y)
            jeu.Pastille(self,'Green', self.rock_x, self.rock_y)


    # calcul tout les coups possibles


    # indique les cases possibles
    def Pastille(self,couleur, Cp_x, Cp_y):
        r = 15  # rayon
        for i in range(len(Cp_x)):
            x = self.marge_i + self.pas * (Cp_x[i] + 1 / 2)
            y = self.marge_j + self.pas * (Cp_y[i] + 1 / 2)
            # ici la fonction renvoie le cercle créé
            self.Plateau.create_oval(x - r, y - r, x + r, y + r, fill=couleur, outline='black', tags='del')


    def analyse(self):
        self.Plateau.pack_forget()
        def affiche_analyse(self,valeur):
            if valeur==2:
                titre ='Temp par coup'
                titre_X ="COUP"
                titre_Y ="TEMP"
            else:
                titre='Prise par coup'
                titre_X="COUP"
                titre_Y="PRISE"
            rad2.destroy()
            rad3.destroy()
            data_x = []
            data_v = []
            data_v2 = []
            connection = sqlite3.connect("jeu_d'échec.db")
            curseur = connection.cursor()
            curseur.execute("SELECT Count(*) FROM partie")
            nombre=curseur.fetchall()
            nb_prise_B = int()
            nb_prise_N = int()
            for i in range(nombre[0][0]):
                curseur.execute("SELECT * FROM partie WHERE n°coup=?", (i+1,))
                info = curseur.fetchall()
                (t, Id, prise, x, y, d_x, d_y, temp) = info[0]
                if valeur == 2:
                    data_x.append(t)
                    data_v.append(temp)
                else:
                    if prise!=0:
                        if prise>100:
                            nb_prise_B+=1
                        else:
                            nb_prise_N+=1
                    data_x.append(t)
                    data_v.append(nb_prise_B)
                    data_v2.append(nb_prise_N)


            x = np.array(data_x)
            v = np.array(data_v)

            fig = Figure(figsize=(6, 6))
            a = fig.add_subplot(111)
            a.scatter(x, v, color='red')
            a.plot(range(max(x)),v, color='blue')
            if valeur==3:
                v2= np.array(data_v2)
                a.scatter(x, v2, color='green')
                a.plot(range(max(x)), v2, color='purple')


            a.set_title(str(titre), fontsize=16)
            a.set_ylabel(str(titre_Y), fontsize=14)
            a.set_xlabel(str(titre_X), fontsize=14)

            canvas = FigureCanvasTkAgg(fig, master=self.fen)
            canvas.get_tk_widget().pack()
            canvas.draw()
            def retour_partie(self):
                canvas.get_tk_widget().pack_forget()
                retourne.destroy()
                self.Plateau.pack()
                jeu.rafraichir_damier(self)
                jeu.Update(self)
                for i in range(len(self.mb)):
                    jeu.mort(self, self.mb[i], False)
                for j in range(len(self.mn)):
                    jeu.mort(self, self.mn[j], False)
                jeu.check_echec(self, self.B, True)
                if jeu.check_echec(self, self.B, False):
                    jeu.check_echec_et_mat(self, self.B)
                jeu.check_echec(self, self.N, True)
                if jeu.check_echec(self, self.N, False):
                    jeu.check_echec_et_mat(self, self.N)
                playsound('Image/teleportation.mp3')

            retourne = ttk.Radiobutton(self.fen, style='Wild.TButton', text='Retour à la partie',
                                   command=lambda *args:retour_partie(self))
            retourne.pack(side='bottom')
        deleted_1 = self.Plateau.find_withtag('de')
        for i in range(len(deleted_1)):
            t = deleted_1[i]
            self.Plateau.delete(t)
        deleted_2 = self.Plateau.find_withtag('Prom')
        for i in range(len(deleted_2)):
            t = deleted_2[i]
            self.Plateau.delete(t)
        deleted_3 = self.Plateau.find_withtag('rej')
        for i in range(len(deleted_3)):
            t = deleted_3[i]
            self.Plateau.delete(t)
        s = ttk.Style()
        s.configure('Wild.TButton',
                    background='black',
                    foreground='white',
                    highlightthickness='20',
                    font=('Helvetica', 18, 'bold'))
        s.map('Wild.TButton',
                foreground=[('pressed', 'red'),
                            ('active', 'blue')],
                background=[('pressed', 'cyan'),
                            ('active', 'green')],
                relief=[('pressed', 'groove'),
                        ('!pressed', 'ridge')])


        rad2 = ttk.Radiobutton(self.fen, style='Wild.TButton', text='Temp par coup', command=lambda *args:affiche_analyse(self,2))

        rad3 = ttk.Radiobutton(self.fen, text='Prise par coup', style='Wild.TButton', command=lambda *args:affiche_analyse(self,3))


        rad2.pack(side='left')

        rad3.pack(side='left')



jeu()