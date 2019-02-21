
#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import math
from math import *
import matplotlib.pyplot as plt
from cooperative_game import * 
import pickle
import string

def powerset(s):
     x = len(s)
     masks = [1 << i for i in range(x)]
     for i in range(1 << x):
         yield [ss for mask, ss in zip(masks, s) if i & mask]


entries={}
party_names={}
polls={}

root = tk.Tk()

FILENAME=askopenfilename()
entries = pickle.load( open( FILENAME, "rb" ) )
root.destroy()

s=0
party_num=0
for k in range(0, 15):
     try:
         polls[k]=float(entries[k+1,3])
         s=s+1
     except ValueError:
         party_num=s


# Initialize parties and coalitions (labelled by letters)

labels=['']*party_num
colors=['']*party_num
excluded=['']*party_num

parties = list(string.ascii_uppercase)[0:party_num]

for k in range(0, party_num):
     party_names[k]=str(entries[k+1,0])
     labels[k]=str(entries[k+1,1])
     colors[k]=str(entries[k+1,2])
     excluded[k]=list(str(entries[k+1,4]))


label = dict(zip(parties,labels))  
color = dict(zip(parties,colors))
coalitions = powerset(parties)


# Introduce campaign commitments

fr={}
friends={}
for k in range(0,party_num):
        fr[k]=list(set(parties) - set(excluded[k]))

for k in range(0,party_num):
    friends[parties[k]]=fr[k]

# Computing seats, Shapley values and all winning coalitions

P=0
for i in range(len(polls)):
     P += polls[i]


# Initialize proportions of seats (precise and rounded)    

s ={}                                                    
sround = {}    
pl = {} 
i = 0  
for p in parties:
     pl[p]=polls[i]
     s[p] = polls[i]/P
     sround[p]= round(float(s[p]*100),1)
     i+=1

worth = {}   
for i in tuple(coalitions):
     sumsp=0
     for r in tuple(i):
         j=set(i).intersection(set(friends[r]))
         if j==set(i):
             sumsp = sumsp +  s[r]
     worth[tuple(i)] = ( copysign(1,(sumsp - 0.5)) + 1)/2
     if ( copysign(1,(sumsp - 0.5)) + 1)==1:
         worth[tuple(i)] = 0


print(worth)
wirth = {}
print(tuple(powerset(i)))
for i in tuple(coalitions):
     wirth[tuple(i)]=0
     for r in tuple(powerset(i)):
         if worth[tuple(r)]==1:
             wirth[tuple(i)]=1
print(wirth)

letter_game = CooperativeGame(worth)
sh = letter_game.shapley_value()
print( "{:<10} {:<10} {:<10} {:<10} {:<10}".format('Label', 'Party', 'Votes (%)', 'Seats (%)', 'Strength') )
for k in parties:
     lb = label[k]
     num = sround[k]
     v = max(sh[k],0)
     print( "{:<10} {:<10} {:<10} {:<10} {:<10}".format(k, lb, round(float(pl[k]),2), num, v) )    

letter_function = {}
for k in worth.keys():            # Find all winning coalitions
     if worth[k] != 0:
         letter_function[k]=worth[k]


# Find all minimal winning coalitions

non_minimal_winning={}
for k in letter_function.keys():
     for j in letter_function.keys():
         if (j!= k) and (set(k).intersection(set(j)) == set(k)):             
             non_minimal_winning[j]=letter_function[j]

minimal_winning={}
for k in letter_function.keys():
    if not(k in non_minimal_winning.keys()):
         minimal_winning[k]=letter_function[k]


# Find all stable coalitions

plt.figure(0)                
chi = {}
power = {}
maxchi = 0
for k in minimal_winning.keys():
     S = 0
     for j in k:
         S += max(sh[j],0)
     chi[k] = minimal_winning[k]/S
     if chi[k] > maxchi:
         maxchi = chi[k]
     u=''
     b = 0
     for j in k:
         po=''
         pc=''
         power[j] = max(0,sh[j])*chi[k]
         if power[j]==0:
             po='('
             pc=')'
         u = u + po + label[j].split('/')[0] + pc + ' '  
     for i in k:
         plt.bar(u, power[i], bottom = b, color = color[i])
         b = b +power[i]
     plt.bar(u, 0.03, bottom=chi[k]/maxchi*(0.9), color='white', width=.2) 
plt.xticks(rotation=-20, fontsize=8, horizontalalignment='left')
plt.show()

print('Minimal winning coalitions and Power distribution') 
print('( Power = Strength x Stability ):')            

S = 0
for j in parties:
     S += max(sh[j],0)

plt.figure(1)                
for i in parties:
     plt.bar(label[i], s[i], color = color[i], width=0.3, align='center')
     plt.bar(label[i], 0.003, bottom = max(0,sh[i])/S, color = 'red', width=0.6, align='center')         
plt.xticks(rotation=-20, fontsize=8, horizontalalignment='left')
plt.show()

