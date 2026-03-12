import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import random
import os
import requests
import deep_translator
from deep_translator import GoogleTranslator


#Primary configuration
window = tkinter.Tk()
window.title("New Word .machine")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
frame = ttk.Frame(window, padding=20)
frame.pack(expand=True, fill="both")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)
window.minsize(250, 500)


#Language interface
haekieli = ttk.LabelFrame(frame, text="Choose languages", padding=5)
haekieli.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
haekieli.columnconfigure(0, weight=1)
haekieli.columnconfigure(1, weight=1)  


#Lang
LANGUAGES = [
    ("English",    "en"),
    ("Finnish",    "fi"),
    ("Swedish",    "sv"),
    ("German",     "de"),
    ("French",     "fr"),
    ("Spanish",    "es"),
    ("Italian",    "it"),
    ("Portuguese", "pt"),
    ("Russian",    "ru"),
    ("Arabic",     "ar"),
    ("Chinese",    "zh"),
    ("Japanese",   "ja"),
    ("Korean",     "ko"),
    ("Dutch",      "nl"),
    ("Polish",     "pl"),
    ("Turkish",    "tr"),
    ("Ukrainian",  "uk"),
]
LANG_NAMES  = [l[0] for l in LANGUAGES]
LANG_CODES  = {l[0]: l[1] for l in LANGUAGES}


#Language var. CHANGE VALUE TO CHANGE DEFAULT LANGUAGE!
lan_e = tkinter.StringVar(value="Finnish")
lan_t = tkinter.StringVar(value="Swedish")
lan_m = tkinter.StringVar(value="10")
valinta = tkinter.StringVar(value="1")  
file_vars=""


#Selection commands
def update():
    current_val = valinta.get()
    if current_val in ("1", "2"):
        txtlist.config(state="normal")

    else:
        txtlist.config(state="disabled")
        txtlist.config(text="Select file")
    window.update_idletasks()

def selection():
    global file_vars
    current_val = valinta.get()
    if current_val in ("1", "2"):
        if not file_vars:
            messagebox.showinfo("Error", "words.txt not found")
            return
        else:
            getwords()
    else:
        getwords2()       


#Select words command
def data():
    window.update_idletasks()
    current_val = valinta.get()
    if current_val=="1":

    #Run automatically in command folder:
        tiedot = os.path.join(os.getcwd(), "words.txt")
        if not os.path.exists(tiedot):
            messagebox.showinfo("Error", "words.txt not found")
        else:
            messagebox.showinfo("Success", "words.txt found!")        
    #For select files. Can be changed to other file types
    else:
        tiedot=filedialog.askopenfilename(title="Select wordlist", filetypes=[("TXT files","*.txt")])
    if tiedot:
        global file_vars
        file_vars=tiedot
        
        txtlist.config(text="File chosen")

        window.update_idletasks()
        window.geometry("")


def get_random_words(amount):
        if amount >5:
            url = f"https://random-word-api.herokuapp.com/word?number={amount}"
    #Difficulty setting only works for 5 or less words at the time
        else: #CHANGE VALUE DIFF=X FOR DIFFICULTY (1-5)
            url = f"https://random-word-api.herokuapp.com/word?number={amount}&diff=5"
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r.json()  
        except Exception as e:
            return [f"[virhe: {e}]"]


#Button for files
txtlist=tkinter.Button(haekieli, text="Select file", command=data)
txtlist.grid(row=4, column=0, padx=5, pady=5)


#Print words on UI
def sanat(words):
    for widget in sanalista.winfo_children():
        widget.destroy()
    #Otsikkorivi
    ttk.Label(sanalista, text="English").grid(row=0, column=1, padx=10)
    ttk.Label(sanalista, text=lan_e.get()).grid(row=0, column=2, padx=10)
    ttk.Label(sanalista, text=lan_t.get()).grid(row=0, column=3, padx=10)
    #Sanat
    for i, (w1, w2, w3) in enumerate(words, start=1):
        ttk.Label(sanalista, text=str(i)).grid(row=i, column=0)
        ttk.Label(sanalista, text=w1).grid(row=i, column=1, padx=10)
        ttk.Label(sanalista, text=w2).grid(row=i, column=2, padx=10)
        ttk.Label(sanalista, text=w3).grid(row=i, column=3, padx=10)
    

#Options 1 and 2
def getwords():
    btn1.config(text="Translating...", state="disabled")
    window.update_idletasks() 

    with open(file_vars, "r") as file:
        english_words = file.read().split()
    
    lang1 = LANG_CODES.get(lan_e.get())
    lang2 = LANG_CODES.get(lan_t.get())
    amount = int(lan_m.get())
    random_words=random.sample(english_words, amount)
    
    translator1 = GoogleTranslator(source="en", target=lang1)
    translator2 = GoogleTranslator(source="en", target=lang2)

    pairs = []
    for w in random_words:
        t1 = translator1.translate(w)
        t2 = translator2.translate(w)
        pairs.append((w, t1, t2))

    sanat(pairs)

    btn1.config(text="New words!", state="normal")
    window.update_idletasks()

def getwords2():
    btn1.config(text="Translating...", state="disabled")
    window.update_idletasks() 


    lang1 = LANG_CODES.get(lan_e.get())
    lang2 = LANG_CODES.get(lan_t.get())
    amount = int(lan_m.get())
    
    translator1 = GoogleTranslator(source="en", target=lang1)
    translator2 = GoogleTranslator(source="en", target=lang2)

    english_words = get_random_words(amount)
    pairs = []
    for w in english_words:
        t1 = translator1.translate(w)
        t2 = translator2.translate(w)
        pairs.append((w, t1, t2))

    sanat(pairs)

    btn1.config(text="New words!", state="normal")
    window.update_idletasks()


#Interface1
LS1=tkinter.Label(haekieli, text="First language")
LS1.grid(row=1, column=0, padx=5, pady=5)
LS2=tkinter.Label(haekieli, text="Second language")
LS2.grid(row=1, column=1, padx=5, pady=5)
LS3=tkinter.Label(haekieli, text="Number of words")
LS3.grid(row=1, column=2, padx=5, pady=5)
etu=ttk.Combobox(haekieli, textvariable=lan_e, values=LANG_NAMES, width=7)
etu.grid(row=2, column=0)
keski=ttk.Combobox(haekieli, textvariable=lan_t, values=LANG_NAMES, width=7)
keski.grid(row=2, column=1)
reuna=ttk.Combobox(haekieli, values=["5", "10", "20", "30", "40"],textvariable=lan_m, width=7)
reuna.grid(row=2, column=2)
btn1=tkinter.Button(haekieli, text="Get words!", command=selection)
btn1.grid(row=4, column=1, padx=3, pady=3)


#Radio
radio1=tkinter.Radiobutton(haekieli, text="Search for file", value="1", variable=valinta, command=update)
radio2=tkinter.Radiobutton(haekieli, text="Select file", value="2", variable=valinta, command=update)
radio3=tkinter.Radiobutton(haekieli, text="Random words", value="3", variable=valinta, command=update)
radio1.grid(row=3, column=0, padx=3, pady=3)
radio2.grid(row=3, column=1, padx=3, pady=3)
radio3.grid(row=3, column=2, padx=3, pady=3)


#words here
sanalista = ttk.LabelFrame(frame, text="Words to learn", padding=10)
sanalista.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

window.mainloop()
