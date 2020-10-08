
def gameResultToLearningReward(allowed, victory, playerID):
    """ 0=game not ended yet
        1= x wins
        2= o wins
        3=draw"""
        
    if allowed:
        if (victory==1 and playerID==0) or (victory==2 and playerID==1):
            return 300
        elif (victory==2 and playerID==0) or (victory==1 and playerID==1):
            return -100        
    else:
        return -500

def learningActionToGameAction(learningAction):
    actions=[0]*45
    counter=0
    for l in range(9):
            for j in range(l):
                actions[counter]=([j,l],2)
                counter+=1
    for l in range(9):
        actions[counter]=([l],1)
        counter+=1
    return actions[learningAction]
                
actions=learningActionToGameAction(3)
#%%
