import tkinter as tk
from tkinter import scrolledtext
import dataset 
import sqlite3

connection = sqlite3.connect('todos.db')

db = dataset.connect('sqlite:///todos.db')
#db.query('DROP TABLE IF EXISTS todos')

table = db['todos']
table.insert({'CARD': 'INIT', 'TITLE': '', 'ROW': 0})
db.query('DELETE FROM todos WHERE CARD = "INIT"') # insert data to create columns, then delete row

cards = []
card_row = 0

root = tk.Tk()
root.title('TODOS')
root.tk_setPalette(background='#d080cd', foreground='#11307d')

# entry field for new card
def entry_field(frm):
    e = tk.Entry(frm)
    e.grid(column=0, row=card_row)
    card = ''
    e.bind('<Return>', lambda event=None: save_card(event, frm, card, e))
    return e

def create():
    frm1 = tk.Frame(root)
    frm1.grid()
    frm1.pack()
    rows = []
    for i in table.find():
        btn = tk.Button(frm1, text=i['TITLE'])
        cards.append(btn)
        rows.append(i['ROW'])
    global card_row
    for btn in [x for _, x in sorted(zip(rows, cards))]:
        btn.grid(column=0, row=card_row, sticky='ew')
        btn.bind('<Button-1>', lambda event=None: show_contents(event, frm1))
        cards.append(btn)
        card_row += 1
    e = entry_field(frm1)
    return frm1, e

# save card in dict, create button, close entry field
def save_card(event, frm, card, e):
    card = e.get()
    btn = tk.Button(frm, text=card)
    global card_row
    cards.append(btn)
    table.insert({'CARD': str(btn), 'TITLE': card, 'DESCRIPTION': '', 'ROW': card_row})
    btn.grid(column=0, row=card_row, sticky='ew')
    btn.bind('<Button-1>', lambda event=None: show_contents(frm))
    card_row += 1
    e.destroy()
    entry_field(frm)

# show contents of selected card in new frame
def show_contents(event, frm):
    frm2 = tk.Toplevel(root, highlightthickness=4, borderwidth=10)
    frm2.config(highlightbackground='#541240', highlightcolor='#541240')
    #frm2.pack()
    btn = event.widget
    card = btn.cget('text')

    e = tk.Entry(frm2, font='Helvetica 18 bold', justify='center')
    e.insert('end', card)
    e.pack()
    tk.Label(frm2, text='Description:').pack()
    e1 = scrolledtext.ScrolledText(frm2, height=10, width=50)
    e1.insert('end', [x['DESCRIPTION'] for x in table.find(CARD=str(btn))][0])
    e1.pack()

    tk.Button(frm2, text='Save', command=lambda: update_card(btn, e, e1, frm2)).pack(side='left')
    tk.Button(frm2, text='Close', command=frm2.destroy).pack(side='left')
    frm2.focus_set()  # focus is necessary to bind key to frame
    frm2.bind('<Escape>', lambda event=None: exit(event, frm2))
    tk.Button(frm2, text="Up", command=lambda: move_up(btn, frm)).pack(side='left')
    tk.Button(frm2, text="Down", command=lambda: move_down(btn, frm)).pack(side='left')

# update description and title
def update_card(btn, e, e1, frm):
    table.update({'CARD': str(btn), 'TITLE': e.get(), 'DESCRIPTION': e1.get(1.0, 'end')}, ['CARD'])
    btn.configure(text=e.get())
    frm.destroy()

def exit(event, widget):
    widget.destroy()

# function to recreate a list when moving a card up or down
def recreate_list(frm, rows2):
    for widget in frm.winfo_children():
        widget.grid_forget()
    card_row = 0
    rows2.append(len(rows2))
    for widget in [x for _, x in sorted(zip(rows2, frm.winfo_children()))]:
        widget.grid(column=0, row=card_row, sticky='ew')
        card_row += 1

def move_up(btn, frm):
    ids = [x['id'] for x in table.find()]
    rows = [x['ROW'] for x in table.find()]
    selected = [x['ROW'] for x in table.find(card=str(btn))][0]
    rows2 = []
    for x in rows:
        if x == selected:
            rows2.append(x - 1)
        elif x == selected - 1:
            rows2.append(x + 1)
        else:
            rows2.append(x)
    for i in zip(ids, rows2):
        db.query(f'UPDATE todos SET ROW = {i[1]} WHERE id = {i[0]}')
    recreate_list(frm, rows2)

def move_down(btn, frm):
    ids = [x['id'] for x in table.find()]
    rows = [x['ROW'] for x in table.find()]
    selected = [x['ROW'] for x in table.find(card=str(btn))][0]
    rows2 = []
    for x in rows:
        if x == selected:
            rows2.append(x + 1)
        elif x == selected + 1:
            rows2.append(x - 1)
        else:
            rows2.append(x)
    for i in zip(ids, rows2):
        db.query(f'UPDATE todos SET ROW = {i[1]} WHERE id = {i[0]}')
    recreate_list(frm, rows2)

#

def main():
    frm1, e = create()
    root.mainloop()
        

if __name__ == '__main__':
    main()




""" 
next:
lists 
done list
classes?
 """



