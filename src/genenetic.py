from nn import *
import numpy as np
from devise import *
from affichage import *
from random import randint
import time
import matplotlib.pyplot as plt

a = plt.subplot(211)
log = 0

def strat(l,devise,neural, verval=False):
    max_holding = 100
    indexx=devise.data.index
    holdings = pd.DataFrame(index=indexx, data={'Holdings': np.array([np.nan] *
        len(indexx))})
    #print(holdings)
    i = 0

    for date in indexx:
        elt = l[i]
        check = True
        for j in elt:
            if math.isnan(i):
                check = False
        if check:
            res = neural.run(np.array([elt]))[0]
            if res[0] > res[1]:
                #if (verval):
                    #print(0,end=' ')
                holdings.loc[date, 'Holdings'] = max_holding
            else:
                #if verval:
                    #print(1, end=' ')
                holdings.loc[date, 'Holdings'] = 0
        i+=1;

    #if verval:
     #   print("")
        #print(neural.model.layers[0].get_weights()[0])
        #print(holdings)
    holdings.ffill(inplace=True)
    holdings.fillna(0, inplace=True)
    #print(holdings)
    holdings['Order'] = holdings.diff()
    holdings.dropna(inplace=True)
    #print(holdings)
    #print("#1")
    #print(holdings.loc[((holdings['Order'] < 0) | (holdings['Order'] > 0)),"Order"])
    #global a
    #print_holding(devise, holdings, a)


    return holdings


def resume(devise, holdings):
    tab_money = devise.data.loc[holdings.loc[((holdings['Order'] < 0) | (holdings['Order'] > 0))].index]['Close']
    benefice = 0
    i = 0
    tmp = 0
    moy = 0
    for elt in tab_money:
        if i % 2 == 0:
            tmp -= elt
        else:
            tmp += elt
            benefice += tmp
            tmp = 0
        i+=1

    if i % 2 == 1:
        i-=1
    if i != 0:
        moy = benefice/(i/2)


    return (benefice, moy, i/2)

def classement(l, devise, l_player):
    l_benef = {}
    l_moy = {}
    l_nb = {}
    size = len(l_player)
    for i in range(size):
        holdings = strat(l, devise, l_player[i])
        benefice, moy, nb = resume(devise, holdings)
        l_benef[i] = benefice
        l_moy[i] = moy
        l_nb[i] = nb
    l_benef_s = sorted(l_benef.items(), key=lambda t: t[1])
    l_moy_s = sorted(l_moy.items(), key=lambda t: t[1])
    l_nb_s = sorted(l_nb.items(), key=lambda t: t[1])

    res = [0 for i in range(size)]
    ib = 0
    save_b = -1000000
    im = 0
    save_m = -1000000
    inb = 0
    save_nb = -1000000
    summery = [[0,0,0] for i in range(size)]
    for i in range(size):
        if l_benef_s[i][1] != save_b:
            save_b = l_benef_s[i][1]
            ib+=1
        res[l_benef_s[i][0]] += ib * 0.5

        if l_moy_s[i][1] != save_m:
            save_m = l_moy_s[i][1]
            im+=1
        res[l_moy_s[i][0]] += im * 0.8

        if l_nb_s[i][1] != save_nb:
            save_nb = l_nb_s[i][1]
            inb+=1
        res[l_nb_s[i][0]] += inb * 1.6

        summery[l_benef_s[i][0]][0] = l_benef_s[i][1]
        summery[l_moy_s[i][0]][1] = l_moy_s[i][1]
        summery[l_nb_s[i][0]][2] = l_nb_s[i][1]

    result = {}
    for i in range(size):
        result[i] = res[i]
    result = sorted(result.items(), key=lambda t: t[1])

    print("Best is ", result[size-1][0], " with ",result[size-1][1])
    print("number :", l_player[result[size-1][0]].name)
    print("benef = ", l_benef.get(result[size-1][0]))
    print("moy = ", l_moy.get(result[size-1][0]))
    print("nb = ", l_nb.get(result[size-1][0]))
    print(summery)
    h = strat(l, devise, l_player[result[size-1][0]], True)
    print(devise.data.loc[h.loc[((h['Order'] < 0) | (h['Order'] > 0))].index]['Close']
)

    return result


def fecondation(papa, maman):
    global log
    child = Genome(log,1)
    tmp = np.array([0 for i in range(13)])
    child.run(np.array([tmp]))

    log+=1
    xc = []

    for ssize in range(len(papa.model.layers)):
        xc = []
        xp = papa.model.layers[ssize].get_weights()[0]
        xm = maman.model.layers[ssize].get_weights()[0]
        for i in range(len(xm)):
            xc.append([])
            for j in range(len(xm[0])):
                if (randint(0,100) % 2 ==0):
                    if (randint(0,100) % 2 ==0):
                        xc[i].append(xp[i][j])
                    else:
                        xc[i].append(xm[i][j])
                else:
                    xc[i].append((xp[i][j]+xm[i][j])/2)
        res = []
        res.append(np.array(xc))
        for i in range(1, len(papa.model.layers[ssize].get_weights())):
            res.append(papa.model.layers[ssize].get_weights()[i])
    
        child.model.layers[ssize].set_weights(res)
    return child



def new_generation(result, l_player):
    global log
    new_l = []
    one = l_player[result[len(result)-1][0]]
    two = l_player[result[len(result)-2][0]]
    tree = l_player[result[len(result)-3][0]]
    new_l.append(one)
    new_l.append(two)
    new_l.append(tree)
    for i in range(int(len(l_player)/2)):
        n = randint(0,100) 
        if (n % 4 == 0):
            new_l.append(fecondation(one, two))
        if (n % 4 == 1):
            new_l.append(fecondation(one, tree))
        if (n % 4 == 2):
            new_l.append(fecondation(two, tree ))
        if (n % 4 == 3):
            new_l.append(fecondation(two, one))
    for i in range(int((len(l_player)/2)-3)):
        new_l.append(Genome(log,3))
        log+=1

    return new_l


def main():
    global a
    global log
    appl = Devise("IBM", (2018,1,1), (2018,12,30))
    setx = appl.set_train()
    #print(setx)
    l = np.array(setx.values.tolist())
    #print(l)
    l_player = []
    for i in range(50):
        l_player.append(Genome(log))
        log+=1
    
    for i in range(100):
        podium = classement(l, appl, l_player)
        l_player = new_generation(podium, l_player)

    #print_holding(appl, holdings, a)
    #a.plot(appl.data.index, appl.data['Adj Close'], label='Close')
        
    #print(holdings)
    #print("#1")
    #print(holdings.loc[(holdings['Order'] > 0),'Order'])
    #print("#2")
    #print(holdings.loc[(holdings['Holdings'] > 0),'Holdings'])



    #plt.show()



         

main()
