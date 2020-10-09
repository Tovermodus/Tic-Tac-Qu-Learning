import game.game as game
import learning.qLearning as learning
import conversions
from copy import deepcopy

actions = 45
statusVariables = 9
class Interface:
    def __init__(self):
        self.g = game.Game()
        self.ql1 = learning.QLearner(0)
        self.ql2 = learning.QLearner(1)

    def main(self):
        for i in range(5):
            self.g.print_table()
            machine = False
            # machine = isMachine()
            allowed = True
            win = 0
            if self.isMachine("X"):
                fields, type = self.getAction(0)
                allowed = self.g.executeMachineTurn(fields, "X", type)
                self.g.print_table()
                win = self.g.check_for_win("X")
                self.g.check_full("X")
                self.sendResult(0, [allowed, win])
            else:
                selectedType = self.g.select_type("X")
                self.g.executeTurn(selectedType, "X")
                self.g.check_full("X")
                self.g.check_for_win("X")

            if i == 4:
                break
            if self.isMachine("O"):
                fields, type = self.getAction(1)
                allowed = self.g.executeMachineTurn(fields, "O", type)
                self.g.print_table()
                win = self.g.check_for_win("X")
                self.g.check_full("O")
                self.sendResult(1, [allowed, win])
            else:
                selectedType = self.g.select_type("O")
                self.g.executeTurn(selectedType, "O")
                self.g.check_full("O")
                self.g.check_for_win("O")
        self.g.final()

    def sendResult(self, playerID, gameResult):
        reward = conversions.gameResultToLearningReward(gameResult[0], gameResult[1], playerID)
        print(reward)
        if playerID == 0:
            self.ql1.saveLearningEntry(reward)
        elif playerID == 1:
            self.ql2.saveLearningEntry(reward)

    def isMachine(self, playerName):
        return True

    def getAction(self, playerID):
        actionID = 0
        if playerID == 0:
            actionID = self.ql1.nextAction(self)
        elif playerID == 1:
            actionID = self.ql2.nextAction(self)
        return conversions.learningActionToGameAction(actionID)


    #return [0],1    #klassischer Zug links oben
    #return [0,1],2  #Superposition links oben, mitte oben


    def getCurrentBoardState(self):
        print(self.g)
        return self.g.get_board_state()


    def getStateAfterAction(self,playerID, actionID):
        fields, type = conversions.learningActionToGameAction(actionID)
        copygame = deepcopy(self.g)
        if playerID == 0:
            copygame.executeMachineTurn(fields, "X", type)
        elif playerID == 1:
            copygame.executeMachineTurn(fields, "X", type)
        return copygame.get_board_state()


if __name__ == "__main__":
    interface = Interface()
    interface.main()


