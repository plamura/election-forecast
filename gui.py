#!/usr/bin/env python3
import tkinter as tk
import pickle

entries={}

entry={}
entry_var={}
root = tk.Tk()

tk.Label(root, text="Country").grid(row=0)
tk.Label(root, text="Poll").grid(row=1)
tk.Label(root, text="Party Name").grid(row=2, column=1)
tk.Label(root, text="Party Label").grid(row=2, column=2)
tk.Label(root, text="Party Color").grid(row=2, column=3)
tk.Label(root, text="Seats Proportion").grid(row=2, column=4)
tk.Label(root, text="Excluded Partners").grid(row=2, column=5)
tk.Label(root, text="A").grid(row=3)
tk.Label(root, text="B").grid(row=4)
tk.Label(root, text="C").grid(row=5)
tk.Label(root, text="D").grid(row=6)
tk.Label(root, text="E").grid(row=7)
tk.Label(root, text="F").grid(row=8)
tk.Label(root, text="G").grid(row=9)
tk.Label(root, text="H").grid(row=10)
tk.Label(root, text="I").grid(row=11)
tk.Label(root, text="J").grid(row=12)
tk.Label(root, text="K").grid(row=13)
tk.Label(root, text="L").grid(row=14)
tk.Label(root, text="M").grid(row=15)
tk.Label(root, text="N").grid(row=16)
tk.Label(root, text="O").grid(row=17)
tk.Label(root, text="P").grid(row=18)
tk.Label(root, text="Q").grid(row=19)
tk.Label(root, text="R").grid(row=20)
tk.Label(root, text="S").grid(row=21)
tk.Label(root, text="T").grid(row=22)
tk.Label(root, text="U").grid(row=23)
tk.Label(root, text="V").grid(row=24)
tk.Label(root, text="W").grid(row=25)
tk.Label(root, text="X").grid(row=26)
tk.Label(root, text="Y").grid(row=27)
tk.Label(root, text="Z").grid(row=28)

for j in range(0,5):
         entry_var[0,j] = tk.StringVar()

entry[0,0] = tk.Entry(root, width=10, textvariable=entry_var[0,0]).grid(row=0,column=1)
entry[0,1] = tk.Entry(root, width=10, textvariable=entry_var[0,1]).grid(row=1,column=1)

for k in range(0,27):
     for j in range(0,5):
         entry_var[k,j] = tk.StringVar()
         entry[k,j] = tk.Entry(root, width=10, textvariable=entry_var[k,j]).grid(row=k+3,column=j+1)



entry[28] = tk.Button(root, text='Quit', command=root.quit).grid(row=30,column=0)
entry[29] = tk.Button(root, text='Load', command=root.quit).grid(row=30,column=1)
entry[30] = tk.Button(root, text='Save', command=root.quit).grid(row=30,column=2)

def autoupdate(*args):
     with open('test.txt', 'w') as f:
         for k in range(0,27):
             for j in range(0,5):
                 f.write(entry_var[k,j].get()+ '\n')
                 entries[k,j]=entry_var[k,j].get()

for k in range(0,27):
     for j in range(0,5):
         entry_var[k,j].trace('w', autoupdate)


root.mainloop()

polls={}
entry_types=('country','poll','party_names','party_labels','seats_proportion','exclusions')
country=entry_var[0,0].get()
poll=entry_var[0,1].get()

pickle.dump(entries, open("save.p", "wb"))
