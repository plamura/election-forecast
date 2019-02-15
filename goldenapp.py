#!/usr/bin/env python3
import math
from math import *
import matplotlib.pyplot as plt
from cooperative_game import * 
import pickle
import string

# Initialize proportions of seats (precise and rounded)

def powerset(s):
     x = len(s)
     masks = [1 << i for i in range(x)]
     for i in range(1 << x):
         yield [ss for mask, ss in zip(masks, s) if i & mask]


entries={}
entries = pickle.load( open( "save.p", "rb" ) )

party_names={}
polls={}
s=0
party_num=0
for k in range(0, 15):
     try:
         polls[k]=float(entries[k,3])
         s=s+1
     except ValueError:
         party_num=s
         polls[k]=0


# Initialize parties and coalitions (labelled by letters)

labels=['']*party_num
colors=['']*party_num

for k in range(0, party_num):
     party_names[k]=str(entries[k,0])
     labels[k]=str(entries[k,1])
     colors[k]=str(entries[k,2])

parties = list(string.ascii_uppercase)[0:party_num]

label = dict(zip(parties,labels))  
color = dict(zip(parties,colors))
coalitions = powerset(parties)

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


# Introduce campaign commitments

friends={}
friends['A']='A', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'N'
friends['B']='B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
friends['C']='B', 'C', 'D', 'E', 'J', 'L', 'M', 'N'
friends['D']='A','B', 'C', 'D', 'E', 'I', 'j', 'K', 'L', 'M', 'N'
friends['E']='A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
friends['F']='A','B', 'E', 'F', 'G', 'H', 'K', 'M', 'N'
friends['G']='A','B', 'E', 'F', 'G', 'H', 'K', 'M', 'N'
friends['H']='A','B', 'E', 'F', 'G', 'H', 'K', 'M', 'N'
friends['I']='A','B', 'D', 'E', 'I', 'J', 'K', 'M', 'N'
friends['J']='B', 'C', 'D', 'E', 'I', 'J', 'K', 'L', 'M', 'N'
friends['K']='A','B', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N'
friends['L']='B', 'C', 'D', 'E', 'J', 'L', 'M', 'N'
friends['M']='B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
friends['N']='A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'

worth = {}                                           # Assign worth to coalitions
for i in tuple(coalitions):
     sumsp=0
     for r in tuple(i):
         j=set(i).intersection(set(friends[r]))
         if j==set(i):
             sumsp = sumsp +  s[r]
     worth[tuple(i)] = ( copysign(1,(sumsp - 0.5)) + 1)/2
     if ( copysign(1,(sumsp - 0.5)) + 1)==1:
         worth[tuple(i)] = 0
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
     plt.bar(label[i], pl[i], color = color[i], width=0.3, align='center')
     plt.bar(label[i], 0.003, bottom = max(0,sh[i])/S, color = 'red', width=0.6, align='center')         
plt.xticks(rotation=-20, fontsize=8, horizontalalignment='left')
plt.show()
