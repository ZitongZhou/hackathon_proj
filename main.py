alpha=0.5   ##probability of spread from a person with symptom to a close-contact person
beta=0.1    ##probability of spread from a person during incubation to a close-contact person
N=100000    ##number of users
Noldmeet=3  ##average number of close-contact old friends everyday
Nnewmeet=1  ##average number of close-contact strangers everyday
Nfriendpool=100  ##average number of friends
Nsym=10   ##number of users reporting symptom
eg=500    ##predict the probability of carrying virus for user#500 and user#1000
eg2=1000

def predict(alpha,beta,N,Noldmeet,Nnewmeet,Nfriendpool,Nsym,eg,eg2):
    import numpy as np
    import random
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.mlab as mlab
    import seaborn as sns
    # class TrieNode(object):
    #     def __init__(self,x):
    #         self.children = {}
    #         self.issym = False
    #         self.val=x
            #self.maxfre = 0
    ### build pool of memory by recalling
    #np.random.seed(9001)
    time_start=time.time()
    mempool=[]
    for i in range(N):
        new={}
        socialnew=np.random.poisson(lam=Nnewmeet, size=30)
        socialold=np.random.poisson(lam=Noldmeet, size=30)
        friendpool=np.random.randint(N,size=min(np.random.poisson(lam=Nfriendpool),N))
        for date in range(30):
             x=np.random.randint(N,size=socialnew[date])
             y=random.sample(list(friendpool),socialold[date])
             new[date]=tuple(x)+tuple(y)
        mempool.append(new)
    ### build symptom
    sypt={}
    syp=np.random.randint(N,size=Nsym)
    for i in syp:
         date=np.random.randint(30)
         sypt[date]=sypt.get(date,())+tuple([i])
    time_end=time.time()
    print('time cost',time_end-time_start,'s')
    ### update the pool 
    for i, ppl in enumerate(mempool):
         for key in ppl.keys():
            for key2 in ppl[key]:
                 if key not in mempool[key2].keys():
                     mempool[key2][key]=(i)
                 elif i not in mempool[key2][key]:
                     mempool[key2][key]=mempool[key2][key]+tuple([i])
    time_end=time.time()
    print('time cost',time_end-time_start,'s')
    ### optional
    # visited={}
    # root=TrieNode(-1)
    # for i, ppl in enumerate(mempool):
    #      if i not in visited:
    #          level=root
    #      else:
    #          level=TrieNode(i)    
    #      for key in ppl.keys():
    #          level.children[key]=TrieNode(ppl[key])

    ### 
    cpath=[[] for _ in range(N)]   ##path starting from a patient with symptom
    cpathin=[[] for _ in range(N)] ##path starting from a patient in incubation
    prob=[1 for _ in range(N)]    
    for i in syp:
        prob[i]=0
    result=[]
    resultin=[]
    def search(child,count,path,curr_key):
          result.append(path)
          for key1 in mempool[child].keys():
             if key1>=curr_key:               
                for cc in mempool[child][key1]:
                    if count<=1 and cc not in syp:
                         search(cc,count+1,path+[(cc,key1) for cc in [cc]],key1)

    def searchin(child,count,path,curr_key):
          curr_key=max(0,curr_key-np.random.randint(low=0,high=14))  
          resultin.append(path)
          for key1 in mempool[child].keys():
             if key1>=curr_key:               
                for cc in mempool[child][key1]:
                    if count<=0 and cc not in syp:
                         searchin(cc,count+1,path+[(cc,key1) for cc in [cc]],key1)


    for key in sypt.keys():
         for p in sypt[key]:
             search(p,0,[(p,key) for p in [p]],key)
             searchin(p,0,[(p,key) for p in [p]],key)


    for pathi in result:   ###########  spread after symptom
        if len(pathi)!=1:
            cpath[pathi[-1][0]].append(pathi)
            if len(pathi)==2:
                 prob[pathi[-1][0]]*=(1-alpha)
            elif  len(pathi)==3:
                 prob[pathi[-1][0]]*=(1-alpha*beta)
    for pathi in resultin:    ########### spread during  incubation
        if len(pathi)!=1:
             cpathin[pathi[-1][0]].append(pathi)
             if len(pathi)==2:
                 prob[pathi[-1][0]]*=(1-beta)
    prob=[1-i for i in prob]  ##probability of carrying varius
    su=0
    for i in prob:
        if i==0:
            su+=1
    plt.style.use('ggplot')
    plt.hist(prob, 
        bins = 20, 
        color = 'steelblue', 
        edgecolor = 'k', 
        label = 'Probability of infection' )
    plt.xlabel('probability of infection')
    plt.ylabel('number of people')
    plt.savefig('static/hist.png')
    plt.cla()
    #plt.hist(prob,1000)
    labels=['COVID-19 tests needed','COVID-19 tests not needed']
    s=0
    for i in prob:
         if i==0:
                s+=1
    X=[s,len(prob)-s] 
    plt.style.use('ggplot')
    plt.pie(X,labels=labels,autopct='%1.2f%%',colors=sns.color_palette("muted"))
    plt.savefig('static/pie.png')
    plt.cla()
    return su,prob[eg],cpath[eg],cpathin[eg],prob[eg2],cpath[eg2],cpathin[eg2]
    #return prob
    # print('number of safe users',su)##########number of safe people
    # print('Look at user',eg)
    # print('probability of carrying virus',prob[eg])
    # print('how to get the virus from people with symptom',cpath[eg])        ######is eg safe or not   all the path from patient with symptom
    # print('how to get the virus from people during incubation',cpathin[eg])      ######is eg safe or not   all the path from patient during incubation

    # print('Look at user',eg2)
    # print('probability of carrying virus',prob[eg2])
    # print('how to get the virus from people with symptom',cpath[eg2])        ######is eg safe or not   all the path from patient with symptom
    # print('how to get the virus from people during incubation',cpathin[eg2])      ######is eg safe or not   all the path from patient during incubation
    # print('most dangerous users',[i for i in range(len(prob)) if prob[i]>0.1])
predict(alpha,beta,N,Noldmeet,Nnewmeet,Nfriendpool,Nsym,eg,eg2)