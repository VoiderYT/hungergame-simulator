import copy
import math
import random


attack_msg = {"fist" : ["p1 punched p2, dealing dmg damage",
"p1 kicked p2, dealing dmg damage","p1 elbowed p2 for dmg"], "rock" :
["p1 threw a rock at p2, hitting p2's leg",
 "p1 lobbed a stone at p2, hitting p2's chest",
 "p1 hurrled a rock at p2, hitting p2's head"], "spear" :
["p1 threw a spear at p2 but it turned, hitting p2 with the blunt side",
 "p1 threw a spear at p2, cutting their arm",
 "p1 threw a spear at p2, cutting their chest",
 "p1 threw a spear at p2, hitting p2's head"]}


supprise_text = ["p1 catches p2 off guard", "p2 doesn't expect p1's attack", "p1 attacks while p2 is distracted", "p1 attacks p2 while p2 was resting"]


sponsor_drops = [{"wood":1}, {"rock":1}, {"water":5}, {"food":3}, {"purifier":1}]


class Weapon:
  def __init__(self, name, ranged, damageMin, damageMax, consume=True) -> None:
    self.ranged = ranged
    self.name = name
    self.damageMin = damageMin
    self.damageMax = damageMax
    self.consume = consume
  def attack(self, attacker, p, ranged, origin=True):
    supprised = False
    if ranged == self.ranged:
      supprised = random.randint(1, 2) == 1
      if supprised and origin:
        msg = random.choice(supprise_text)
        msg = msg.replace("p1", attacker.name)
        msg = msg.replace("p2", p.name)
        print(msg)
        
      if random.randint(1, 5) > 1:
        dmg = random.randint(self.damageMin, self.damageMax)
        if not origin:
          dmg = dmg//2
        if self.name in attack_msg:
          dmgType = math.ceil((dmg-self.damageMin)/(self.damageMax-self.damageMin)*len(attack_msg[self.name]))-1
          msg = attack_msg[self.name][dmgType]
          msg =msg.replace("p1", attacker.name)
          msg = msg.replace("p2", p.name)
          msg = msg.replace("dmg", str(dmg))
          print(msg)
          
        p.health -= dmg
        if p.health <= 0:
          p.health = 0
          print(p.name + " IS ELIMINATED!")
          
          for item in p.items:
            attacker.collect(item, p.items[item])
          if p in players:
            players.remove(p)
        if self.consume:
          attacker.collect(self.name, -1)
      else:
        print(attacker.name + " missed when trying to attack " + p.name + "!")
        
    if not self.ranged and origin and (p in players) and not supprised:
      p.attack(attacker, self.ranged, origin=False)


weapons = {"rock":Weapon(name="rock",ranged=True,damageMin=25,damageMax=50, consume=True), "spear":Weapon(name="spear", ranged=True,damageMin=20,damageMax=90, consume=True)}


fist = Weapon(name="fist",ranged=False,damageMin=15, damageMax=30, consume=False)


class Player:


  def __init__(self, name):
    self.name = name
    self.items = {'water': 3, 'food': 2}
    self.health = 100
    self.hunger = 100
    self.thirst = 100
    self.location = 'Clearing'


  def turn(self):
    choices = ['Hide', 'Explore', 'Fight', 'Fight', 'Fight', 'Sleep']
    if "wood" in self.items and self.items["wood"] > 0 and "rock" in self.items and self.items["rock"] > 0 and 'spear' not in self.items:
      for _ in range(3):
        choices.append("Craft Spear")
    self.thirst -= 5
    if self.thirst < 75:
      if self.items['water'] > 0:
        choices.append('Drink')
      else:
        choices.append('Explore')
    if self.thirst < 50:
      if self.items['water'] > 0:
        choices.append('Drink')
      else:
        choices.append('Explore')
    if self.thirst < 25:
      if self.items['water'] > 0:
        choices.append('Drink')
      else:
        choices.append('Explore')
    if self.thirst < 10:
      if self.items['water'] > 0:
        choices.append('Drink')
      else:
        choices.append('Explore')
    self.hunger -= 5
    if self.hunger < 75:
      choices.append('Eat')
    if self.hunger < 50:
      choices.append('Eat')
    if self.hunger < 25:
      choices.append('Eat')
    if self.hunger < 10:
      choices.append('Eat')
    choice = random.choice(choices)
    #print(self.name + ' chooses ' + choice)
    if choice == 'Hide':
      self.health -= 5
      print(self.name + ' hides!')
      
    elif choice == 'Explore':
      self.health -= 10
      for _ in range(random.randint(1, 2)):
        if not(self in players):
            return
        if self.health <= 0:
            players.remove(self)
            print(self.name + ''' WAS ELIMINATED!
''')
            return
        areas = [
            'Water', 'Food', 'Water', 'Food', "Trip", "Cave", "Forest",
            "Mountain"
        ]
        area = random.choice(areas)
        if area == 'Water':
          print(self.name + ' finds a water source!')
          
          if "purifier" in self.items:
            self.items["water"] += 1
            print(self.name + ' purifies the water!')
            
          else:
            print(self.name + " can't purify the water!")
            
        elif area == 'Food':
          print(self.name + ' finds some food!')
          
          if "wood" in self.items and self.items["wood"] > 0:
            self.items["food"] += 2
            print(self.name + ' lights a fire and cooks the food!')
            
            self.items["wood"] -= 1
          else:
            self.items["food"] += 1
            print(self.name + " can't cook the food!")
            
        elif area == 'Trip':
            print(self.name + ' has tripped!')
            
            self.health -= 10
        elif area == "Cave":
          self.location = area
          if random.randint(1, 2) == 1:
              print(self.name + ' finds a cave!')
          else:
              print(self.name + ' finds a cave with a rock!')
              self.collect('rock')
          
        elif area == "Forest":
          self.location = area
          if random.randint(1, 2) == 1:
              print(self.name + ' finds a forest!')
          else:
              print(self.name + ' finds a forest and collects wood!')
              self.collect('wood', 3)
          
        else:
          self.location = area
          print(self.name + ' finds a ' + area + '!')
          
    elif choice == 'Sleep':
      print(self.name + ' takes a nap!')
      
      self.health += 20
    elif choice == 'Drink':
      if self.items['water'] > 0:
        self.health += 10
        self.thirst += 10
        self.items['water'] -= 1
        print(self.name + ' drinks some water!')
        
    elif choice == 'Eat':
      if self.items['food'] > 0:
        self.health += 10
        self.hunger += 10
        self.items['food'] -= 1
        print(self.name + ' eats some food!')
        
    elif choice == 'Fight':
      #max = None
      #w = None
      #for i in self.items:
      #  if i in weapons and (max is None or weapons[i].damageMin > max):
      #    max = weapons[i].damageMin
      #    w = weapons[i]
      #if w is None:
      #  w = fist
      ps = players
      random.shuffle(ps)
      vic = None
      for p in ps:
        if p != self:
          vic = p
          break
      if vic is None:
         pass
      else:
        self.attack(vic, False)
    elif choice == "Craft Spear":
      print(self.name + ' makes a spear using a peice of wood and a rock!')
      
      self.collect('wood', -1)
      self.collect('stone', -1)
      self.collect('spear', 1)


    if self.hunger <= 0:
      self.health -= 20
      print(self.name + " is starving!")
      
    if self.thirst <= 0:
      self.health -= 20
      print(self.name + " is thirsty!")
      


    self.health = min(self.health, 100)
    if self.health <= 0:
      if self in players:
        players.remove(self)
        print(self.name + " IS ELIMINATED!")
        


  def attack(self, attacker, ranged, origin=True):
    max = None
    w = None
    for i in self.items:
      if i in weapons and (max is None or weapons[i].damageMin > max):
        max = weapons[i].damageMin
        w = weapons[i]
    if w is None:
      w = fist
    w.attack(self, attacker, ranged, origin=origin)


  def status(self):
    print(self.name + ':')
    print(' Health: ' + str(self.health))
    print(' Hunger: ' + str(self.hunger))
    print(' Thirst: ' + str(self.thirst))
    print(' Items: ' + str(self.items))


  def collect(self, item, amount=1):
    if item in self.items:
      self.items[item] += amount
    else:
      self.items[item] = amount




ap = input('How many players: ')
ap = int(ap)
players = []
if ap >= 10:
  for i in range(ap):
    players.append(Player(str(i)))
else:
  for i in range(ap):
    name = input(f'Player {1+i} name: ')
    players.append(Player(name))


day = True
dayNumber = 1
while len(players) > 1:
  time = 0
  if day:
    print('Day ' + str(dayNumber) + ':')
  else:
    print('Night ' + str(dayNumber) + ':')
    dayNumber += 1
  plys = copy.copy(players)
  random.shuffle(plys)
  for p in plys:
    if not(p in players):
        continue
    if random.randint(1,2) == 1:
      input("")
      if day:
          print("Day " + str(dayNumber))
      else:
        print("Night " + str(dayNumber))
   # print('Time: ' + str(time))
    p.turn()
    if random.randint(1, 10) == 1:
      spons = random.choice(sponsor_drops)
      msg = ""
      for item in spons:
        p.collect(item, spons[item])
        msg += str(spons[item]) + "x" + str(item) + ","
      print(p.name + " gets a sponsor and receives " + msg[0:-1])
      
    #p.status()
  day = not (day)
  input()
print(players[0].name + ' wins!')
