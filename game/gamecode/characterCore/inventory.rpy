label InitInventory:
    python:
        class Item:
            def __init__(self, name, itemType, cost, tags=[], requires=[""], requiresEvent=[],hp=0,ep=0,sp=0, Exp=0, Power=0, Tech=0, Int=0, Allure=0, Willpower=0, Luck=0, statusEffect="",
                        statusChance=0,statusPotency=0, descrips="", useOutcome="",useMiss="", BodySensitivity=BodySensitivity(), resistancesStatusEffects=ResistancesStatusEffects(), perks=[], skills=[], isSkill="False", consumableLimit=-1):
                self.name = name
                self.itemType = itemType #Healing, StatusEffect, Ring, keyItem
                self.cost = cost

                self.tags = tags
                self.requires = requires
                self.requiresEvent = requiresEvent

                self.perks = perks
                self.skills = skills

                self.hp=hp
                self.ep=ep
                self.sp=sp

                self.Exp = Exp

                self.Power = Power
                self.Tech = Tech
                self.Int = Int
                self.Allure = Allure
                self.Willpower = Willpower
                self.Luck = Luck

                self.statusEffect = statusEffect
                self.statusChance = statusChance
                self.statusPotency = statusPotency

                self.descrips = descrips #text
                self.useOutcome = useOutcome #text
                self.useMiss = useMiss #text

                self.NumberHeld=1

                self.BodySensitivity = BodySensitivity
                self.resistancesStatusEffects = resistancesStatusEffects

                #self.onEquip = onEquip #on equip variables for equip events, turned off for now cause they dont really work the way i want
                #self.onUnequip = onUnequip

                self.isSkill = "False"

                #CODEMOD
                self.consumableLimit = consumableLimit

            def Update(self):
                try:
                    self.Int
                except:
                    setattr(self, 'Int', 0)
                try:
                    self.tags
                except:
                    setattr(self, 'tags', [])
                return

                #CODEMOD
                try:
                    self.consumableLimit
                except:
                    setattr(self, 'consumableLimit', -1)
                return

            def getStat(self, statName):
                if statName == "Arousal":
                    return self.hp
                if statName == "Energy":
                    return self.ep
                if statName == "Spirit":
                    return self.sp

                if statName == "Power":
                    return self.Power
                if statName == "Technique":
                    return self.Tech
                if statName == "Intelligence":
                    return self.Int
                if statName == "Allure":
                    return self.Allure
                if statName == "Willpower":
                    return self.Willpower
                if statName == "Luck":
                    return self.Luck

                return 0

        class Inventory:
            def __init__(self, money=500):
                self.money = money
                self.items = []

                self.RuneSlotOne = Item("Empty", "Rune", "0")
                self.RuneSlotTwo = Item("Empty", "Rune", "0")
                self.RuneSlotThree = Item("Empty", "Rune", "0")

                self.AccessorySlot = Item("Empty", "Accessory", "0")

            def useItem(self, item):
                if self.items[getFromName(item, self.items)] != -1:
                    if(self.items[getFromName(item, self.items)].NumberHeld == 1):
                        del self.items[getFromName(item, self.items)]
                    else:
                        self.items[getFromName(item, self.items)].NumberHeld -= 1

            def HasExcess(self):
                ExcessYes = 0
                for each in self.items:
                    if each.itemType == "Rune":
                        NumberFullyHeld = 0
                        if self.RuneSlotOne.name == each.name:
                            NumberFullyHeld += 1
                        if self.RuneSlotTwo.name == each.name:
                            NumberFullyHeld += 1
                        if self.RuneSlotThree.name == each.name:
                            NumberFullyHeld += 1
                        if (each.NumberHeld + NumberFullyHeld) > 3:
                            ExcessYes = 1
                    elif each.itemType == "Accessory":
                        NumberFullyHeld = 0
                        if self.AccessorySlot.name == each.name:
                            NumberFullyHeld += 1
                        if (each.NumberHeld + NumberFullyHeld) > 1:
                            ExcessYes = 1
                return ExcessYes

            def HasLoot(self):
                for each in self.items:
                    if each.itemType == "Loot":
                        return True
                return False

            def equip(self, slot, player, equipOrUnequip):
                equipping = Item("Empty", "Rune", "0")
                if slot == 1:
                    equipping = self.RuneSlotOne
                if slot == 2:
                    equipping = self.RuneSlotTwo
                if slot == 3:
                    equipping = self.RuneSlotThree
                if slot == 4:
                    equipping = self.AccessorySlot


                try:
                    for each in equipping.skills:
                        if equipOrUnequip >= 1:
                            if each != "":
                                fetchSkill = getFromName(each, SkillsDatabase)
                                player.learnSkill(SkillsDatabase[fetchSkill])
                        else:
                            if each != "":
                                foundskill = 0
                                for skill in player.skillList:
                                    if skill.name == each and foundskill == 0:
                                        player.removeSkill(each)
                                        foundskill = 1
                except:
                        foundskill = 1

                for each in equipping.perks:
                    if equipOrUnequip >= 1:
                        if each != "":
                            player.giveOrTakePerk(each, 1)
                    else:
                        if each != "":
                            p = 0
                            foundperk = 0
                            for eachP in player.perks:
                                if eachP.name == each and foundperk == 0:
                                    player.giveOrTakePerk(each, -1)
                                    foundperk = 1
                                p += 1


                player.stats.max_hp += equipping.hp * equipOrUnequip
                player.stats.max_ep += equipping.ep * equipOrUnequip
                player.stats.max_sp += equipping.sp * equipOrUnequip

                player.stats.Power += equipping.Power * equipOrUnequip
                player.stats.Tech += equipping.Tech * equipOrUnequip
                player.stats.Int += equipping.Int * equipOrUnequip
                player.stats.Allure += equipping.Allure * equipOrUnequip
                player.stats.Willpower += equipping.Willpower * equipOrUnequip
                player.stats.Luck += equipping.Luck * equipOrUnequip

                player.BodySensitivity.Sex += equipping.BodySensitivity.Sex * equipOrUnequip
                player.BodySensitivity.Ass += equipping.BodySensitivity.Ass * equipOrUnequip
                player.BodySensitivity.Breasts +=  equipping.BodySensitivity.Breasts * equipOrUnequip
                player.BodySensitivity.Mouth +=  equipping.BodySensitivity.Mouth * equipOrUnequip
                player.BodySensitivity.Seduction +=  equipping.BodySensitivity.Seduction * equipOrUnequip
                player.BodySensitivity.Magic +=  equipping.BodySensitivity.Magic * equipOrUnequip
                player.BodySensitivity.Pain +=  equipping.BodySensitivity.Pain * equipOrUnequip
                player.BodySensitivity.Holy +=  equipping.BodySensitivity.Holy * equipOrUnequip
                player.BodySensitivity.Unholy +=  equipping.BodySensitivity.Unholy * equipOrUnequip

                player.resistancesStatusEffects.Stun += equipping.resistancesStatusEffects.Stun * equipOrUnequip
                player.resistancesStatusEffects.Charm += equipping.resistancesStatusEffects.Charm * equipOrUnequip
                player.resistancesStatusEffects.Aphrodisiac += equipping.resistancesStatusEffects.Aphrodisiac * equipOrUnequip
                player.resistancesStatusEffects.Restraints += equipping.resistancesStatusEffects.Restraints * equipOrUnequip
                player.resistancesStatusEffects.Sleep += equipping.resistancesStatusEffects.Sleep * equipOrUnequip
                player.resistancesStatusEffects.Trance += equipping.resistancesStatusEffects.Trance * equipOrUnequip
                player.resistancesStatusEffects.Paralysis += equipping.resistancesStatusEffects.Paralysis * equipOrUnequip
                player.resistancesStatusEffects.Debuff += equipping.resistancesStatusEffects.Debuff * equipOrUnequip


            def buy(self, item, amount=1):
                if self.money >= item.cost*amount:
                    self.money -= item.cost*amount

                    if(self.has_item(item)):
                        self.items[getFromName(item.name, self.items)].NumberHeld +=amount
                    else:
                        item.NumberHeld = amount
                        self.items.append(item)
                    return True
                else:
                    return False


            def getFromName(theName, searchThis):
                i = 0
                for x in searchThis:
                    if searchThis[i].name == theName:
                        return i
                    i += 1
                return -1

            def give(self, itemName, amount=1):
                testPass = 0
                dataTarget = getFromName(itemName, ItemDatabase)
                blankItem =  copy.deepcopy(ItemDatabase[dataTarget])

                i = 0
                selectedItem = 0
                while i < len(self.items):
                    if(self.items[i].name == itemName):
                        testPass = 1
                        selectedItem = i
                    i += 1

                if(testPass == 1):
                    self.items[selectedItem].NumberHeld += amount
                else:
                    blankItem.NumberHeld = amount
                    self.items.append(blankItem)


            def Update(self):
                self.RuneSlotOne.resistancesStatusEffects.Update()
                self.RuneSlotTwo.resistancesStatusEffects.Update()
                self.RuneSlotThree.resistancesStatusEffects.Update()

                self.AccessorySlot.resistancesStatusEffects.Update()

                self.RuneSlotOne.Update()
                self.RuneSlotTwo.Update()
                self.RuneSlotThree.Update()
                self.AccessorySlot.Update()
                #self.resistancesStatusEffects.Update()
                return

            def earn(self, amount):
                self.money += amount

            def has_item(self, item):
                    if getFromName(item.name, self.items) != -1:
                        return True
                    else:
                        return False

        #CODEMOD: Inventory Subclass that will allow for consumables to be limited while storing excess items in a separate "stash" list
        class StashInventory(Inventory):
            
            def __init__(self, money = 500, inventory=None):
                super().__init__(money)
                self.stash = []
                self.stashActive = False

                if inventory:
                    self.items = copy.deepcopy(inventory.items)
                    self.money = inventory.money

                    self.RuneSlotOne = copy.deepcopy(inventory.RuneSlotOne)
                    self.RuneSlotTwo = copy.deepcopy(inventory.RuneSlotTwo)
                    self.RuneSlotThree = copy.deepcopy(inventory.RuneSlotThree)

                    self.AccessorySlot = copy.deepcopy(inventory.AccessorySlot)
            
            #Static variable denoting the default number of consumables that can be used per item per adventure
            DEFAULTLIMIT = -1

            @staticmethod
            def revertInventory(stashInventory):
                if type(stashInventory) is not StashInventory:
                    return None

                copiedInventory = copy.deepcopy(stashInventory)
                copiedInventory.deactivateStash()

                inventory = Inventory()
                inventory.items = copy.deepcopy(copiedInventory.items)
                inventory.money = copiedInventory.money

                inventory.RuneSlotOne = copy.deepcopy(copiedInventory.RuneSlotOne)
                inventory.RuneSlotTwo = copy.deepcopy(copiedInventory.RuneSlotTwo)
                inventory.RuneSlotThree = copy.deepcopy(copiedInventory.RuneSlotThree)

                inventory.AccessorySlot = copy.deepcopy(copiedInventory.AccessorySlot)
                return inventory
            
            @staticmethod
            def isConsumable(item):
                return item.itemType in ["Consumable", "DissonantConsumable", "CombatConsumable", "CombatConsumable", "NotCombatConsumable"]

            @staticmethod
            def isItemOverLimit(item):
                return StashInventory.isConsumable(item) and item.consumableLimit > 0 and item.NumberHeld > item.consumableLimit

            @staticmethod
            def isInTown():
                return not explorationDeck

            def limitItemCount(self, item):
                if not self.stashActive:
                    return False
                
                if StashInventory.isItemOverLimit(item):
                    excessCount = item.NumberHeld - item.consumableLimit
                    item.NumberHeld = item.consumableLimit
                    
                    existsInStash = getFromName(item.name, self.stash)

                    if existsInStash > -1:
                        self.stash[existsInStash].NumberHeld += excessCount
                    else:
                        itemCopy = copy.deepcopy(item)
                        itemCopy.NumberHeld = excessCount
                        self.stash.append(itemCopy)
                    
                    return True

                return False

            
            def activateStash(self):
                if self.stashActive:
                    return False

                self.stashActive = True

                for item in self.items:
                    self.limitItemCount(item)

                return True

            def deactivateStash(self):
                if not self.stashActive:
                    return False

                self.stashActive = False

                for item in self.stash:
                    existsinInventory = getFromName(item.name, self.items)

                    if existsinInventory > -1:
                        self.items[existsinInventory].NumberHeld += item.NumberHeld
                    else:
                        itemCopy = copy.deepcopy(item)
                        self.items.append(itemCopy)
                
                self.stash.clear()

                #Reset "on_charactermenu.rpy" variable, so only the main inventory is shown
                global MainOrStash
                MainOrStash = "Main"

                return True

            def buy(self, item, amount=1):
                result = super().buy(item, amount)

                if result:
                    self.limitItemCount(self.items[getFromName(item.name, self.items)])
                
                return result

            def give(self, itemName, amount=1):
                super().give(itemName, amount)
                self.limitItemCount(self.items[getFromName(itemName, self.items)])
           
            def Update(self):
                super().Update()

                try:
                    self.stash
                except:
                    setattr(self, "stash", [])
                
                try:
                    self.stashActive
                except:
                    setattr(self, "stashActive", not StashInventory.isInTown())
