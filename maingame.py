import os
import random
import sys
import discord


from People.arvin import Arvin
from People.jay import Jay
from People.sean import Sean
from People.jiyang import Jiyang
from People.sara import Sara
from People.peter import Peter
from People.phillip import Phillip
from People.romir import Romir
from People.emily import Emily
from People.rahul import Rahul
from People.jessica import Jessica
from People.kyle import Kyle
from People.yash import Yash
from People.jeanell import Jeanell
#from People.arvin import Hat



# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')  # There might be a way to do this only using sys not sure


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


class MainFight(object):
    turn = 1

    def __init__(self, teams): #add discord id as a part of this
        self.teams = teams
        self.p1 = self.teams["team1"][0]
        self.p2 = self.teams["team2"][0]
        
        for q in self.teams["team1"]:
            q.team = self.teams["team1"]
            
        for q in self.teams["team2"]:
            q.team = self.teams["team2"]    
        

        self.p2.enemy = self.p1
        self.p1.enemy = self.p2
        self.run()

    # make universally probably
    def damage(self, attacker, victim):
        damage = None

        actualattack = attacker.getActualATK()
        actualdodge = victim.getActualDODGE()
        actualcrit = attacker.getActualCRIT()
        actualdefense = victim.getActualDEF()

        print(
            "Atk = {}\nDodge = {}\nCrit = {}\nDef = {}\n".format(actualattack, actualdodge, actualcrit, actualdefense))

        if actualdefense > 0:
            damage = victim.doesdodge * (max(0, attacker.doescrit * actualattack - actualdefense))
        else:
            damage = victim.doesdodge * (max(0, attacker.doescrit * actualattack - (2 * actualdefense)))

        if victim.doesdodge == 0:
            print("The attack was dodged")
        else:
            if attacker.doescrit > 1:  # its greater than 1 because some characters will have a 3 crit multiplier
                print("Was dealt a critical hit")
            print("({}) took {} damage".format(victim.name, damage))
        victim.hp -= damage


    def deathcheck(self):
        if self.p2.hp <= 0:
            self.p2.onDeath()
            if self.p2.hp <= 0:
                self.teams["team2"].remove(self.p2)
                
                if not self.teams["team2"]:
                    return 1                              
                
                                
                print(self.teams["team2"])
                p2c = -1
                while int(p2c) not in range(1, len(self.teams["team2"])+1):               
                    p2c = input("Select Who to Swap to: ")    
                    
                choice = int(p2c)             
                self.p2 = self.teams["team2"][choice-1]           
                print("player 2 now uses {}".format(self.p2.name))       
                
                
        if self.p1.hp <= 0:
            self.p1.onDeath()            
            if self.p1.hp <= 0:
                self.teams["team1"].remove(self.p1)
                
                if not self.teams["team1"]:
                    return 2
                
                
                print(self.teams["team1"])
                p1c = -1
                while int(p1c) not in range(1, len(self.teams["team1"])+1):               
                    p1c = input("Select Who to Swap to: ")  
                    
                choice = int(p1c)                     
                self.p1 = self.teams["team1"][choice-1]
                print("player 1 now uses {}".format(self.p1.name))
            
        self.p2.enemy = self.p1
        self.p1.enemy = self.p2
                    
      ########################
            
                    

                  
                
    def run(self):     
        lose = None

        while True:
            #print info
            print("TURN {}".format(self.turn))
            print("{}'s Resource count: {}".format(self.p1.name, self.p1.resource))
            print("{}'s Resource count: {}".format(self.p2.name, self.p2.resource))
            print("Player 1 ({}) HP: {}".format(self.p1.name, self.p1.hp))
            print("Player 2 ({}) HP: {}".format(self.p2.name, self.p2.hp))

            # check for deaths

            fuck = self.deathcheck()
            
            
            
            if fuck == 1:
                print("Player 1 wins")
                break
                
            if fuck == 2:
                print("Player 2 wins")
                break

            #test if players will dodge or crit

            self.p1.testdodged()
            self.p2.testdodged()
            self.p1.testcrit()
            self.p2.testcrit()

            # start passives

            self.p1.passive()
            self.p2.passive()

            #prompt move
            print(self.teams["team1"])
            p1c = input("{}: Select your move ({})".format(self.p1.name,
                                                           "a, s, d#" if self.p1.resource >= self.p1.srec else "a, d#"))
           
            while p1c.lower()[0] == "d" and (int(p1c.lower()[1])-1 == self.teams["team1"].index(self.p1) or int(p1c.lower()[1])-1 not in range(len(self.teams["team1"]))):
                p1c = input("{}: Can't Swap to Same Character! Select your move ({})".format(self.p1.name,
                                                           "a, s, d#" if self.p1.resource >= self.p1.srec else "a, d#"))
                                                           
            print(self.teams["team2"])
            p2c = input("{}: Select your move ({})".format(self.p2.name,
                                                           "a, s, d#" if self.p2.resource >= self.p2.srec else "a, d#"))
                                                           
            while p2c.lower()[0] == "d" and (int(p2c.lower()[1])-1 == self.teams["team2"].index(self.p2) or int(p2c.lower()[1])-1 not in range(len(self.teams["team2"]))):
                p2c = input("{}: Can't Swap to Same Character! Select your move ({})".format(self.p2.name,
                                                           "a, s, d#" if self.p2.resource >= self.p2.srec else "a, d#"))

            
            
            #swaps
            
            
            if p1c.lower()[0] == "d" and not self.p1.isParalyzed:
                choice = int(p1c.lower()[1])
                
                self.p1.onSwapOut()
                self.p1 = self.teams["team1"][choice-1]
                self.p1.swappedin = True
                self.p1.onSwapIn()
                print("player 1 swaps")
                    
          
            if p2c.lower()[0] == "d" and not self.p2.isParalyzed:
                choice = int(p2c.lower()[1])
                
                self.p2.onSwapOut()
                self.p2 = self.teams["team2"][choice-1]
                self.p2.swappedin = True
                self.p2.onSwapIn()
                
                print("player 2 swaps")
                
            
            self.p2.enemy = self.p1
            self.p1.enemy = self.p2
            
            # specials
            if p1c.lower() == "s" and not self.p1.isParalyzed:
                if self.p1.resource >= self.p1.srec:
                    self.p1.isSpecial = True
                    self.p1.special()

            if p2c.lower() == "s" and not self.p2.isParalyzed:
                if self.p2.resource >= self.p2.srec:
                    self.p2.isSpecial = True
                    self.p2.special()


            self.p1.midround()
            self.p2.midround()

            # force swaps
            if self.p1.forceSwapped:
                p2mc = int(input("p2 choose who p1 the opponent should swap too: "))
                while p2mc-1 == self.teams["team1"].index(self.p1) or p2mc-1 not in range(len(self.teams["team1"])):
                    p2mc = int(input("p2 cannot force player to swap to themselves or to someone not there. Choose someone else to swap to: "))
                self.p1.forceSwapped = False
                self.p1.onSwapOut()
                self.p1 = self.teams["team1"][p2mc-1]
                self.p1.swappedin = True
                self.p1.onSwapIn()
                print("player 1 is forced to swap")

            if self.p2.forceSwapped:
                p1mc = int(input("p1 choose who p2 the opponent should swap too: "))
                while p1mc-1 == self.teams["team2"].index(self.p2) or p1mc-1 not in range(len(self.teams["team2"])):
                    p1mc = int(input("p2 cannot force player to swap to themselves or to someone not there. Choose someone else to swap to: "))
                self.p2.forceSwapped = False
                self.p2.onSwapOut()
                self.p2 = self.teams["team2"][p1mc-1]
                self.p2.swappedin = True
                self.p2.onSwapIn()
                print("player 2 is forced to swap")

                    
            # p1 attacks p2
            """
            print("({}) attacks ({})".format(self.p1.name, self.p2.name))

            p1.doescrit = 2 if random.uniform(1, 100) < self.p1.crit else 1
            self.p2.damage(self.p1.attack, doescrit)

            #p2 attacks p1
            print("({}) attacks ({})".format(self.p2.name, self.p1.name))

            p2.doescrit = 2 if random.uniform(1, 100) < self.p2.crit else 1
            self.p1.damage(self.p2.attack, doescrit)
            """
            # p1 attacks p2
            if not self.p1.swappedin and not self.p1.isParalyzed:
                print("({}) attacks ({})".format(self.p1.name, self.p2.name))
                self.damage(self.p1, self.p2)

            # p2 attacks p1
            if not self.p2.swappedin and not self.p2.isParalyzed:
                print("({}) attacks ({})".format(self.p2.name, self.p1.name))
                self.damage(self.p2, self.p1)

            # If p1 or p2 is paralyzed
            if self.p1.isParalyzed:
                print("({}) is Paralyzed and can't move".format(self.p1.name))
            if self.p1.isParalyzed:
                print("({}) is Paralyzed and can't move".format(self.p1.name))

            print("MODIFIERS")
            print(self.p1.modifiers)
            print(self.p2.modifiers)
            print("-----------------------------------")


            self.p1.passiveend()
            self.p2.passiveend()

            self.p1.endround()
            self.p2.endround()

            self.turn += 1
            print("\n\n")

        #print("{} loses!".format(lose.name))
        #print("{} : {}\n{} : {}".format(self.p1.name, self.p1.hp, self.p2.name, self.p2.hp))
        #enablePrint()
        #return lose.name

if __name__ == "__main__":
    teams = {   "team1" : [Emily(), Phillip(), Sara()],
                "team2" : [Sean(), Jay(), Peter()]}
                
    coinflip = random.randint(0, 1)
    if coinflip == 0:
        teams["team1"], teams["team2"] = teams["team2"], teams["team1"]
    
    print(teams)
        
    game = MainFight(teams)

