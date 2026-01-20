import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Conectare la baza de date
conn = sqlite3.connect('planner_financiar.db')
cursor = conn.cursor()

# Creare tabele
cursor.execute('''CREATE TABLE IF NOT EXISTS tranzactii
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tip TEXT,
                  suma REAL,
                  categorie TEXT,
                  descriere TEXT,
                  data TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS buget
                 (id INTEGER PRIMARY KEY,
                  suma_lunara REAL)''')

conn.commit()

class PlannerFinanciar:
    def __init__(self, root):
        self.root = root
        self.root.title("Planner Financiar")
        self.root.geometry("700x600")
        self.root.configure(bg='#ADD8E6')
        
        
        main_frame = tk.Frame(root, bg='#ADD8E6')
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        
        tk.Label(main_frame, text="Planner Financiar", font=('Arial', 20, 'bold'), 
                bg='#ADD8E6', fg='#2c3e50').pack(pady=10)
        
        
        buget_frame = tk.LabelFrame(main_frame, text="Buget Lunar", font=('Arial', 12, 'bold'),
                                    bg='#ADD8E6', fg='#2c3e50', padx=10, pady=10)
        buget_frame.pack(fill='x', pady=10)
        
        tk.Label(buget_frame, text="Suma:", bg='#ADD8E6').grid(row=0, column=0, sticky='w')
        self.buget_entry = tk.Entry(buget_frame, width=20)
        self.buget_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(buget_frame, text="Setează Buget", command=self.seteaza_buget,
                 bg='#3498db', fg='white', cursor='hand2').grid(row=0, column=2, padx=5)
        
        self.label_buget = tk.Label(buget_frame, text="Buget curent: 0 RON", 
                                    font=('Arial', 10), bg='#ADD8E6')
        self.label_buget.grid(row=1, column=0, columnspan=3, pady=5)
        
        
        tranz_frame = tk.LabelFrame(main_frame, text="Adaugă Tranzacție", 
                                    font=('Arial', 12, 'bold'), bg='#ADD8E6', 
                                    fg='#2c3e50', padx=10, pady=10)
        tranz_frame.pack(fill='x', pady=10)
        
        tk.Label(tranz_frame, text="Tip:", bg='#ADD8E6').grid(row=0, column=0, sticky='w')
        self.tip_var = tk.StringVar(value="Cheltuială")
        tk.Radiobutton(tranz_frame, text="Venit", variable=self.tip_var, 
                      value="Venit", bg='#ADD8E6').grid(row=0, column=1, sticky='w')
        tk.Radiobutton(tranz_frame, text="Cheltuială", variable=self.tip_var, 
                      value="Cheltuială", bg='#ADD8E6').grid(row=0, column=2, sticky='w')
        
        tk.Label(tranz_frame, text="Suma:", bg='#ADD8E6').grid(row=1, column=0, sticky='w', pady=5)
        self.suma_entry = tk.Entry(tranz_frame, width=20)
        self.suma_entry.grid(row=1, column=1, columnspan=2, sticky='w', pady=5)
        
        tk.Label(tranz_frame, text="Categorie:", bg='#ADD8E6').grid(row=2, column=0, sticky='w')
        self.categorie_entry = tk.Entry(tranz_frame, width=20)
        self.categorie_entry.grid(row=2, column=1, columnspan=2, sticky='w')
        
        tk.Label(tranz_frame, text="Descriere:", bg='#ADD8E6').grid(row=3, column=0, sticky='w', pady=5)
        self.descriere_entry = tk.Entry(tranz_frame, width=20)
        self.descriere_entry.grid(row=3, column=1, columnspan=2, sticky='w', pady=5)
        
        tk.Button(tranz_frame, text="Adaugă", command=self.adauga_tranzactie,
                 bg='#27ae60', fg='white', cursor='hand2').grid(row=4, column=0, columnspan=3, pady=10)
        
        
        stats_frame = tk.LabelFrame(main_frame, text="Statistici Luna Curentă", 
                                    font=('Arial', 12, 'bold'), bg='#ADD8E6',
                                    fg='#2c3e50', padx=10, pady=10)
        stats_frame.pack(fill='x', pady=10)
        
        self.label_venituri = tk.Label(stats_frame, text="Venituri totale: 0 RON", 
                                       bg='#ADD8E6', fg='#27ae60', font=('Arial', 10, 'bold'))
        self.label_venituri.pack()
        
        self.label_cheltuieli = tk.Label(stats_frame, text="Cheltuieli totale: 0 RON", 
                                         bg='#ADD8E6', fg='#e74c3c', font=('Arial', 10, 'bold'))
        self.label_cheltuieli.pack()
        
        self.label_balanta = tk.Label(stats_frame, text="Balanță: 0 RON", 
                                      bg='#ADD8E6', font=('Arial', 10, 'bold'))
        self.label_balanta.pack()
        
        
        tk.Button(main_frame, text="Actualizează Statistici", command=self.actualizeaza_statistici,
                 bg='#9b59b6', fg='white', cursor='hand2').pack(pady=10)
        
        
        self.actualizeaza_statistici()
        self.afiseaza_buget()
    
    def seteaza_buget(self):
        try:
            suma = float(self.buget_entry.get())
            if suma <= 0:
                messagebox.showerror("Eroare", "Bugetul trebuie să fie un număr pozitiv!")
                return
            cursor.execute("DELETE FROM buget")
            cursor.execute("INSERT INTO buget (id, suma_lunara) VALUES (1, ?)", (suma,))
            conn.commit()
            messagebox.showinfo("Success", "Bugetul a fost setat!")
            self.afiseaza_buget()
            self.buget_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Eroare", "Introduceti o suma valida!")
    
    def afiseaza_buget(self):
        cursor.execute("SELECT suma_lunara FROM buget WHERE id = 1")
        result = cursor.fetchone()
        if result:
            self.label_buget.config(text=f"Buget curent: {result[0]} RON")
    
    def adauga_tranzactie(self):
        try:
            tip = self.tip_var.get()
            suma = float(self.suma_entry.get())
            if suma <= 0:
                messagebox.showerror("Eroare", "Suma tranzacției trebuie să fie mai mare decât 0!")
                return
            categorie = self.categorie_entry.get()
            descriere = self.descriere_entry.get()
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("INSERT INTO tranzactii (tip, suma, categorie, descriere, data) VALUES (?, ?, ?, ?, ?)",
                          (tip, suma, categorie, descriere, data))
            conn.commit()
            
            messagebox.showinfo("Success", "Tranzactia a fost adaugata!")
            
            self.suma_entry.delete(0, tk.END)
            self.categorie_entry.delete(0, tk.END)
            self.descriere_entry.delete(0, tk.END)
            
            self.actualizeaza_statistici()
            self.verifica_buget()
            
        except ValueError:
            messagebox.showerror("Eroare", "Introduceti o suma valida!")
    
    def actualizeaza_statistici(self):
        luna_curenta = datetime.now().strftime("%Y-%m")
        
        cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip='Venit' AND data LIKE ?", (luna_curenta + '%',))
        venituri = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip='Cheltuială' AND data LIKE ?", (luna_curenta + '%',))
        cheltuieli = cursor.fetchone()[0] or 0
        
        balanta = venituri - cheltuieli
        
        self.label_venituri.config(text=f"Venituri totale: {venituri:.2f} RON")
        self.label_cheltuieli.config(text=f"Cheltuieli totale: {cheltuieli:.2f} RON")
        self.label_balanta.config(text=f"Balanță: {balanta:.2f} RON")
    
    def verifica_buget(self):
        cursor.execute("SELECT suma_lunara FROM buget WHERE id = 1")
        result = cursor.fetchone()
        
        if result:
            buget = result[0]
            luna_curenta = datetime.now().strftime("%Y-%m")
            
            cursor.execute("SELECT SUM(suma) FROM tranzactii WHERE tip='Cheltuială' AND data LIKE ?", 
                          (luna_curenta + '%',))
            cheltuieli = cursor.fetchone()[0] or 0
            
            if cheltuieli > buget:
                messagebox.showwarning("Alertă Buget", 
                                      f"Ai depășit bugetul lunar!\nBuget: {buget} RON\nCheltuieli: {cheltuieli:.2f} RON")


root = tk.Tk()
app = PlannerFinanciar(root)
root.mainloop()


conn.close()