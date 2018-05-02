
# coding: utf-8

# In[1]:

import sys
opt={}                                #OP-Codes
# assigning the object codes
opt['STL'] = '14'
opt['JSUB'] = '48'
opt['LDA'] = '00'
opt['COMP'] = '28'
opt['JEQ'] = '30'
opt['STA'] = '0C'
opt['RSUB'] = '4C'
opt['J'] = '3C'
opt['LDL'] = '08'
opt['LDX'] = '04'
opt['MUL'] = '20'
opt['DIV'] = '24'
opt['ADD'] = '18'
opt['SUB'] = '1C'
opt['START'] = '-1'
opt['END'] = '-1'
opt['WORD'] = '-1'
opt['RESW'] = '-1'
opt['RESB'] = '-1'
opt['BYTE'] = '-1'
# ASSIGNMENT OVER

NUM=12                            #holds the number of input lines
loc=[0]*(NUM+1)                         #location counter
code=[]                                 #input code
sym_table={}                         #labels and variables
file=open(r"C:\Users\Suraj\Desktop\simple_interest.txt","r")
for i in range(NUM):
    x=file.readline().split(' ')
    if i<NUM-1:
        x[-1]=x[-1][:-1] #removes newline character
    code.append(x)
#print code
loc[0]=' '
loc[1]=code[0][2] #sets LOC to start address
for i in range(1,NUM):                  #FIRST PASS
    if code[i][-2] not in opt.keys():
        print("ERROR: OPCODE '%s' not found!"%code[i][-2])
        print(i)
        sys.exit()
    if len(code[i])==3: 
        sym_table[code[i][0]]=loc[i]
        if code[i][1]=='RESW':
            loc[i+1]=hex((int(loc[i],16) +3*int(code[i][2])))[2:]
        elif code[i][1]=='RESB':
            loc[i+1] = hex((int(loc[i],16) + int(code[i][2])))[2:]
        else:
            loc[i+1] = hex(int(loc[i],16) + 3)[2:]
    else:
        code[i].insert(0,' ')
        loc[i+1] = hex(int(loc[i],16) + 3)[2:]
#print "Symbol Table at the end of Pass 1 is ", sym_table
objcode=[]
print(opt, sym_table)
objcode.append(' ')
for i in range(1,NUM):                      #SECOND PASS
    try:
        if code[i][-2] == 'RESW' or code[i][-2] == 'RESB' or code[i][-2] == 'END':
            objcode.append(' ')
            continue
        if code[i][-2] == 'WORD':
            objcode.append(hex(int(code[i][2]))[2:].rjust(6, '0'))
            #print(hex(int(code[i][2]))[2:].rjust(6, '0'))
        else:
            objcode.append(str(opt[code[i][-2]]) + str(sym_table[code[i][-1]]))
            #print(opt[code[i][-2]], end='')
            #print(loc_for_opnd[code[i][-1]])
    except KeyError:
        print("ERROR: OPERATOR '%s' not in symbol table!"%code[i][-1])
        sys.exit()
#print(len(loc[:-1]),len([code[i][0] for i in range(0,NUM)]),len([code[i][1] for i in range(0,NUM)]),len([code[i][2] for i in range(0,NUM)]),len(objcode))

#x=pandas.DataFrame.from_items([('LOC',loc[:-1]),('Lable',[code[i][0] for i in range(0,NUM)]),('OPCODE',[code[i][1] for i in range(NUM)]),('OPERAND',[code[i][2] for i in range(NUM)]),('OBJECT code',objcode)])

#print(x)
#x.to_csv(r"H:\out.csv")
print ("LOC".center(8,' '),"LABEL".center(8,' '),"OPCODE".center(8,' '),"OPERAND".center(8,' '),"OBJCODE".center(8,' '))
for i in range(NUM):
    print (str(loc[i]).center(8,' '),str(code[i][0]).center(8,' '),str(code[i][1]).center(8,' '),str(code[i][2]).center(8,' '),str(objcode[i]).center(8,' '))
file.close()
file = open(r"outputnew.txt","w")
file.write('H^')
file.write(code[0][0]) #Program name
file.write(' ' * (6 - len(code[0][0])))
file.write('^') 
file.write('0' * (6 - len(code[0][2])))
file.write(code[0][2]) #Starting address of object program
file.write('^')
file.write('0' * 4) #Prints 0's to fill extra spaces 
file.write(hex(int(loc[NUM-1],16)-int(loc[1],16))[-2:]) #prints length of entire program
file.write("\n")
file.write("T^")
file.write('0' * (6 - len(code[0][2])))
file.write(code[0][2]) #Starting address for object code in this record

#length of object code : 
nobj=0
for i in range(1,len(objcode)):
    if objcode[i] != ' ':
        nobj=nobj+1 #nobj*3 beacuse 6*4/8 =3 ; 6-bits in objcode 4-convert to hex  8- to calc in bytes
file.write('^')
file.write(hex(int(nobj*3))[-2:]) #writing length col 8-9 therefore -2(last 2 only)
for i in range(1,len(objcode)):
    if objcode[i] != ' ':
        file.write('^')
        file.write(objcode[i])
file.write("\nE^")
file.write('0' * (6 - len(code[0][2])))
file.write(code[0][2])
file.close()


# In[ ]:



