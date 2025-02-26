screen ON_SkillPrompt(useSkillTarget):
    modal True
    zorder 300
    style_prefix "confirm"
    add Solid("#00000099")

    frame:
        xminimum 1000 yminimum 300
        xmaximum 1000 ymaximum 300

        label _("Use " + player.skillList[useSkillTarget].name + "?"):
            style "confirm_prompt"
            xalign 0.5 yalign 0.1

        fixed:
            xalign 0.15 yalign 1.0
            xsize 324 ysize 81
            use ON_TextButton(text="Use",
            action=[SelectedIf(False), Hide("ON_SkillPrompt"), Function(useSkillFromMenu, useSkillTarget=useSkillTarget)])
        fixed:
            xalign 0.85 yalign 1.0
            xsize 324 ysize 81
            use ON_TextButton(text="Cancel",
            action=[SelectedIf(False), Hide("ON_SkillPrompt")])

screen ON_ConsumePrompt(inventoryTarget):
    modal True
    zorder 300
    style_prefix "confirm"
    add Solid("#00000099")

    frame:
        xminimum 1000 yminimum 300
        xmaximum 1000 ymaximum 300

        label _("Use a " + player.inventory.items[inventoryTarget].name + "?"):
            style "confirm_prompt"
            xalign 0.5 yalign 0.1

        fixed:
            xalign 0.15 yalign 1.0
            xsize 324 ysize 81
            use ON_TextButton(text="Use",
                action=[SelectedIf(False), Hide("ON_ConsumePrompt"), Function(useInventoryItem, inventoryTarget=inventoryTarget)])
        fixed:
            xalign 0.85 yalign 1.0
            xsize 324 ysize 81
            use ON_TextButton(text="Cancel",
                action=[SelectedIf(False), Hide("ON_ConsumePrompt")])

screen ON_EquipPrompt(promptEquipping, promptSlotType, equipmentSlot=0, equipmentTarget=None):
    modal True
    zorder 300
    style_prefix "confirm"
    add Solid("#00000099")

    default TargetEquippedItem = Item("Empty", "Rune", "0")
    default equipPromptText = ""

    frame:
        if promptSlotType == "Rune" and promptEquipping == True:
            xminimum 750 yminimum 600
            xmaximum 750 ymaximum 600
        else:
            xminimum 1000 yminimum 300
            xmaximum 1000 ymaximum 300

        label _("[equipPromptText]"):
            style "confirm_prompt"
            xalign 0.5 yalign 0.1

        if promptEquipping:
            $ equipPromptText = "Equip " + player.inventory.items[equipmentTarget].name + "?"
            if promptSlotType == "Rune":
                $ equipPromptText += " Where?"
                fixed:
                    xalign 0.5 yalign 0.30
                    xsize 324 ysize 81
                    vbox:
                        spacing 15
                        use ON_TextButton(text="Slot 1", action=[SelectedIf(False), Hide("ON_EquipPrompt"),
                            Function(EquipItem, promptEquipping=True, equipmentSlot=1,equipmentTarget=equipmentTarget)])
                        use ON_TextButton(text="Slot 2", action=[SelectedIf(False), Hide("ON_EquipPrompt"),
                            Function(EquipItem, promptEquipping=True, equipmentSlot=2, equipmentTarget=equipmentTarget)])
                        use ON_TextButton(text="Slot 3", action=[SelectedIf(False), Hide("ON_EquipPrompt"),
                            Function(EquipItem, promptEquipping=True, equipmentSlot=3, equipmentTarget=equipmentTarget)])
                        use ON_TextButton(text="Cancel", action=[SelectedIf(False), Hide("ON_EquipPrompt")])
            else:
                fixed:
                    xalign 0.15 yalign 1.0
                    xsize 324 ysize 81
                    use ON_TextButton(text="Equip", action=[
                        SelectedIf(False), Hide("ON_EquipPrompt"), Function(EquipItem, promptEquipping=True, equipmentSlot=4, equipmentTarget=equipmentTarget)])
                fixed:
                    xalign 0.85 yalign 1.0
                    xsize 324 ysize 81
                    use ON_TextButton(text="Cancel", action=[SelectedIf(False), Hide("ON_EquipPrompt")])
        else:
            if equipmentSlot == 1:
                $ TargetEquippedItem = player.inventory.RuneSlotOne
            elif equipmentSlot == 2:
                $ TargetEquippedItem = player.inventory.RuneSlotTwo
            elif equipmentSlot == 3:
                $ TargetEquippedItem = player.inventory.RuneSlotThree
            elif equipmentSlot == 4:
                $ TargetEquippedItem = player.inventory.AccessorySlot

            $ equipPromptText = "Unequip " + TargetEquippedItem.name + "?"

            fixed:
                xalign 0.15 yalign 1.0
                xsize 324 ysize 81
                use ON_TextButton(text="Unequip", action=[
                    SelectedIf(False), Hide("ON_EquipPrompt"), Function(EquipItem, promptEquipping=False, equipmentSlot=equipmentSlot, equipmentTarget=equipmentTarget)])
            fixed:
                xalign 0.85 yalign 1.0
                xsize 324 ysize 81
                use ON_TextButton(text="Cancel", action=[Hide("ON_EquipPrompt")])

screen ON_EquipSlot(itemSlot, slotType, slotID):
    hbox:
        xmaximum 500
        if slotType == "Rune":
            textbutton slotType + " Slot [slotID] - ":
                text_color "#fff"
                text_size on_listTextSize
                ysize on_listEntryHeight
        else:
            textbutton slotType + " - ":
                text_color "#fff"
                text_size on_listTextSize
                ysize on_listEntryHeight

        if itemSlot.name == "Empty":
            textbutton "Empty":
                text_color "#fff"
                text_size on_listTextSize

        else:
            textbutton itemSlot.name:
                tooltip itemSlot.descrips + " Value: " + str(itemSlot.cost) + " eros."
                unhovered [SetVariable("characterMenuCanHover", True)]
                if slotType == "Rune":
                    alt "Rune Slot " + str(slotID) + ", " + itemSlot.name + " \n\n" + itemSlot.descrips + " Value: " + str(itemSlot.cost) + " eros."
                else:
                    alt "Accessory, " + itemSlot.name + " \n\n" + itemSlot.descrips + " Value: " + str(itemSlot.cost) + " eros."
                action [SelectedIf(False), SensitiveIf(InventoryAvailable), Show("ON_EquipPrompt", promptEquipping=False, promptSlotType=slotType, equipmentSlot=slotID)]
                text_insensitive_color "#fff"
                text_size on_listTextSize
                text_textalign 0.0
                text_layout "greedy"

screen ON_SingleFetishDisplay(fetish, value, tempFetishLevel, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight

        $ name = str(fetish.name + ":")

        $ tooltipDisplay = fetish.toolTip

        $ theFetishToolTip = ""
        $ highestValue = -1
        for each in fetish.levelText: #make sure order doesnt matter and it takes the highest u potat
            if value >= each[0] and each[0] >= highestValue:
                $ theFetishToolTip = each[1]
                $ highestValue = each[0]
        $ tooltipDisplay += theFetishToolTip
        
        if tempFetishLevel >= 2:
            $ tooltipDisplay += ("\n\n(Cleanse " + str(tempFetishLevel) + " levels at the church.)")
        elif tempFetishLevel == 1:
            $ tooltipDisplay += ("\n\n(Cleanse " + str(tempFetishLevel) + " level at the church.)")
        $ value = "Lvl " + str(value)

        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            tooltip tooltipDisplay
            unhovered [SetVariable("characterMenuCanHover", True)]
            alt name + " \n" + tooltipDisplay
            if tooltipDisplay != "":
                if renpy.variant("touch") or renpy.variant("mobile"):
                    action SetVariable("charSticky", tooltipDisplay)
                else:
                    action NullAction()
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleDisplay(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight
        if duration >= 0:
            $ tooltipDisplay = perkDurationDisplay( tooltipDisplay, duration, timeType)
        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            tooltip tooltipDisplay
            unhovered [SetVariable("characterMenuCanHover", True)]
            alt name + " \n" + tooltipDisplay
            if tooltipDisplay != "":
                if renpy.variant("touch") or renpy.variant("mobile"):
                    action SetVariable("charSticky", tooltipDisplay)
                else:
                    action NullAction()
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleStatDisplay(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight

        if "Virility: ":
            $ Virility = getVirility(player)

        if "Initiative: ":
            $ InititiveBonus = getInitStats(player)

        if "Reduction: ":
            $ damageReduction = "{:.2f}".format((getDamageReduction(player, 100) -100)*-1).rstrip('0').rstrip('.')

        if "Evade: ":
            $ InStanceEvade = "{:.2f}".format(getBaseEvade(player, 10, 1))
            $ OutOfStanceEvade = "{:.2f}".format(getBaseEvade(player, 0, 1))
        if "Acc: ":
            $ AccuracyBonus = "{:.2f}".format(getBaseAccuracy(player, 0))
            $ InStanceAccuracyBonus = "{:.2f}".format(getBaseAccuracy(player, 10))

        if "Effect Duration: ":
            $ statusDuration = "{:.2f}".format(statusEffectBaseDuration(player))
        if "Effect Chance: ":
            $ statusAccuracyBonus = "{:.2f}".format(getStatusEffectBaseAccuracy(player))
        if "Status Res: ":
            $ statusEvadeBonus = "{:.2f}".format(getStatusEffectEvade(player))

        if "Allure Bonus:  ":
            $ allureFlatScaling = 0.10
            python:
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):
                        if perk.PerkType[p] == "BaselineAllureFlatBuff":
                            allureFlatScaling += perk.EffectPower[p]*0.01
                        p += 1
            $ flatAllureBonus = "{:.2f}".format((player.stats.Allure-5)*allureFlatScaling).rstrip('0').rstrip('.')
        if "Allure Bonus%:  ":
            $ allureFlatPercentBoost = 0
            python:
                for perk in player.perks:
                    p = 0
                    while  p < len(perk.PerkType):

                        if perk.PerkType[p] == "BaselineAllureFlatPercentBoost":
                            allureFlatPercentBoost += perk.EffectPower[p]*0.01
                        p += 1
            $ percentAllureBonus = "{:.2f}".format(100.0 * ((player.stats.Allure - 5) * 0.002 + allureFlatPercentBoost)).rstrip('0').rstrip('.')

        if name == "Crit Chance: " or name == "Crit Damage: ":
            $ critChance = "{:.2f}".format(getCritChance(player))
            $ critDamage = "{:.2f}".format(getCritDamage(player))

        if name == "Crit Reduction: ":
            $ critReduction = "{:.2f}".format(getCritReduction(player))

        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            tooltip tooltipDisplay
            unhovered [SetVariable("characterMenuCanHover", True)]
            alt name + " \n" + value + " \n" + tooltipDisplay
            if tooltipDisplay != "":
                if renpy.variant("touch") or renpy.variant("mobile"):
                    action SetVariable("charSticky", tooltipDisplay)
                else:
                    action NullAction()
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SingleStatDisplayNoVar(name, value, tooltipDisplay="", color="#fff", duration=0, timeType=""):
    fixed:
        ysize on_listEntryHeight
        textbutton name:
            text_size on_listTextSize
            ysize on_listEntryHeight
            tooltip tooltipDisplay
            unhovered [SetVariable("characterMenuCanHover", True)]
            alt name + " \n" + value + " \n\n" + tooltipDisplay
            if tooltipDisplay != "":
                if renpy.variant("touch") or renpy.variant("mobile"):
                    action SetVariable("charSticky", tooltipDisplay)
                else:
                    action NullAction()
            else:
                text_color color

        textbutton value text_size on_listTextSize text_color color ysize on_listEntryHeight xalign 1.0

screen ON_SinglePerkDisplay(perk, spaceNextOne=0):
    $ theTimeType = ""
    for y in perk.PerkType:
        if y == "TimeDuration" or y == "TurnDuration":
            $ theTimeType = y
    use ON_SingleDisplay(perk.name, "", tooltipDisplay=perk.description, duration=perk.duration, timeType=theTimeType)

#CODEMOD: Added "forceInSens" optimal parameter, so that items can be forced to be unclickable regardless of type
screen ON_SingleItemDisplay(item, spaceNextOne=0, forceInSens=False):
    $ invIndex =  getFromName(item.name, getItemsOrStash())
    $ display = item.name

    if getItemsOrStash()[invIndex].NumberHeld > 1:
        $ display += " (" + str(getItemsOrStash()[invIndex].NumberHeld) + ")"

    $ twolayered = 0

    if spaceNextOne == 1:
        #$ twolayered += 15
        $ spaceNext = 0

    if len(display) > 28:
        $ twolayered += 24
        $ spaceNextOne = 1

    if item.itemType != "Key":
        $ itemsToolTip = item.descrips + " Value: " + str(item.cost) + " eros."
    else:
        $ itemsToolTip = item.descrips
    if item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable"  or item.itemType == "CombatConsumable":
        if len(item.skills) > 0:
            $ fetchSkill = getFromName(item.skills[0], SkillsDatabase)
            $ skillToCheck = copy.deepcopy(SkillsDatabase[fetchSkill])
            $ skillToCheck.isSkill = item.itemType
            $ itemsToolTip = getSkillToolTip(skillToCheck, player, itemsToolTip)

    button:
        ysize on_listEntryHeight + twolayered
        tooltip itemsToolTip
        unhovered [SetVariable("characterMenuCanHover", True)]
        hovered [SetVariable("itemEnergyAmount", item.ep), SetVariable("itemArousalAmount", item.hp), SetVariable("itemSpiritAmount", item.sp)]
        alt display + " \n\n" +  itemsToolTip
        text display:
            size on_listTextSize
            #xsize 700
            #CODEMOD: Allows for correct coloring if the item has been forced to be insensivtive
            if item.itemType == "Loot" or item.itemType == "CombatConsumable" or forceInSens:
                idle_color gui.insensitive_color
                hover_color gui.insensitive_color
                insensitive_color gui.insensitive_color
            else:
                idle_color gui.idle_color
                hover_color gui.hover_color
                insensitive_color gui.insensitive_color
        if manualSort == "Items":
            #CODEMOD
            action [Function(SetItemOrder, getFromName(item.name, getItemsOrStash()))]
        else:
            #CODEMOD:Prevents item from being used if item has been forced to be insensitive
            if forceInSens:
                action [SelectedIf(False), NullAction()] # make hoverable
            else:
                if (item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "NotCombatConsumable"):
                    action [SelectedIf(False), Show("ON_ConsumePrompt", inventoryTarget=invIndex)]
                elif item.itemType == "Rune":
                    action [SelectedIf(False), Show("ON_EquipPrompt", promptEquipping=True, promptSlotType="Rune", equipmentTarget=invIndex)]
                elif item.itemType == "Accessory":
                    action [SelectedIf(False), Show("ON_EquipPrompt", promptEquipping=True, promptSlotType="Accessory",  equipmentTarget=invIndex)]
                else:
                    action [SelectedIf(False), NullAction()] # make hoverable

screen ON_StatsListDisplay(showMainStats=False):
    $ damageBoost = 0
    use ON_Scrollbox("Stats"):

        #if showMainStats:
        use ON_SingleStatDisplayNoVar("Arousal:","[player.stats.hp]/[player.stats.max_true_hp]", color="#FB97A3", tooltipDisplay="The amount of sexual stimulation you can take! When it hits its max, you lose spirit.")
        use ON_SingleStatDisplayNoVar("Energy:", "[player.stats.ep]/[player.stats.max_true_ep]", color="#BCC9F0", tooltipDisplay="Your personal reserves of energy, or 'mana' as some like to call it, it's used for skills and magic!")
        use ON_SingleStatDisplayNoVar("Spirit:", "[player.stats.sp]/[player.stats.max_true_sp]", tooltipDisplay="Your life energy! If this runs out, you won't be able to fight back. You lose at least one per orgasm, so really, it's just a measurement of how many times you can cum normally.")
        textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5


        use ON_SingleStatDisplayNoVar("Power:", "[player.stats.Power]", tooltipDisplay="Escape restraints, 'punish' your foes, maintain or get out of sexual positions, and deal increased critical arousal! Every 5 points naturally gained increases your max arousal by 10. Boosts how much damage you do with core skills!\nYou have [powerDisplay] base power out of 100. Power skills deal [powerBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [powerPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Technique:", "[player.stats.Tech]", tooltipDisplay="Used for evading, acting faster, running away, and sexual finesse! It also helps you get out of stances and restraints, but it is not as effective as power. Boosts how much damage you do with core skills!\nYou have [techDisplay] base technique out of 100. Tech skills deal [techBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [techPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Intelligence:", "[player.stats.Int]", tooltipDisplay="Cast magic, resist some temptations, increase your chance to apply status effects, and increase the duration of your status effect! Every 5 points gained naturally increases your max energy by 10. Boosts how much damage you do with core skills!\nYou have [intDisplay] base intelligence out of 100. Intelligence skills deal [intBoost] extra arousal based on the (square root of the stat*4)-5. Said skills also get an increase of [intPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Allure:", "[player.stats.Allure]", tooltipDisplay="Seduce and charm your foes! It increases how much arousal you deal with all skills, including increased critical arousal, and boosts how much damage you do with core skills! Also increases the recoil damage your opponent takes, from sex skills for example!\nYou have [allureDisplay] base allure out of 100. Allure skills deal [allureBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [allurePerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Willpower:", "[player.stats.Willpower]", tooltipDisplay="Greatly resist temptation, status effects, and reduces how much arousal you take! Every 5 points increases your max arousal and max energy by 5.\nYou have [willDisplay] base willpower out of 100. Willpower skills deal [willBoost] extra arousal based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [willPerBoost]% to their base power!")
        use ON_SingleStatDisplayNoVar("Luck:", "[player.stats.Luck]", tooltipDisplay="Helps a little bit across the board. Such as acting before others, getting out of restraints, running away, hitting or dodging attacks, and improves your critical chance! It even gives you the stat check auto passing Goddess Favor at a rate of base Luck/20! But best of all it helps you find more treasure!\nYou have [luckDisplay] base luck out of 100. Luck skills(?) deal [luckBoost] more arousal, based on the (square root of the stat*4)-5.\nSaid skills also get an increase of [luckPerBoost]% to their base power!")

        use ON_MoreStatsListDisplay

screen ON_MoreStatsListDisplay():
        textbutton "---More Stats---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5

        use ON_SingleStatDisplay("Core Skills Bonus", "", tooltipDisplay="Your core skills deal [flatCore] bonus arousal and a bonus of [percentCore]% to the base power of core skills!\nCore skills are based on 50% of your highest stat out of Power, Tech, Int, and Allure, plus the average of the four stats added together. Then the (square root of that times 3)-5 is your flat bonus.")
        use ON_SingleStatDisplay("Initiative: ", "[InititiveBonus]", tooltipDisplay="Initiative determines combatant turn order, with the highest acting first. All combatants add a d100 roll to their base Initiative to determine their total Initiative that turn. Turn order then proceeds from highest total Initiative to lowest.\nYou gain a +75 bonus to Initiative when attempting to use an item.\nInitiative is equal to your Tech + Int/2 + Luck/2 + possible bonuses from perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Crit Chance: ", "[critChance]%", tooltipDisplay="Your percent chance to land a critical hit when attacking.\nIt is equal to your Tech*0.10 + Luck*0.25 + 3.25 + possible bonuses from perks.")
        use ON_SingleStatDisplay("Crit Damage: ", "[critDamage]x", tooltipDisplay="Your arousal modifier when you land a critical!\nIt is equal to your (Power*0.525-2.5) +  (Allure*0.525-2.5) + 200% + possible bonuses from perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        #use ON_SingleStatDisplay("Crit Reduction: ", "[critReduction]%", tooltipDisplay="How much you reduce your opponent's chance to critted you! If it's negative, it's increasing your chance to be crit.\nIt is equal to your Luck*0.2 + perks - 1. When you would be crit and your crit chance reduction saves you 'Passion Endured' will be displayed.")
        use ON_SingleStatDisplay("Evade: ", "[OutOfStanceEvade]%/"+ "[InStanceEvade]%", tooltipDisplay="Chance to Evade attacks out of stance/Chance to evade in stance. Out of stance evade is based on tech-5(0.3% per point) + luck-5(0.15% per point), while In stance evade is based on power-5(0.3% per point) + tech-5(0.15% per point). Both are effected by any respective perks. Defending increases your total evade chance by 50%.\nFetishes, status effects, and attacker accuracy make it harder to evade.")
        use ON_SingleStatDisplay("Acc: ", "[AccuracyBonus]%/"+ "[InStanceAccuracyBonus]%", tooltipDisplay="Attack accuracy bonus out of stances/Accuracy bonus in stance. Out of stance accuracy is based on tech-5(0.3% per point) + luck-5(0.15% per point), while In stance accuracy is based on power-5(0.3% per point) + tech-5(0.15% per point) + 10. Both are effected by any respective perks and get a random roll(d100) added, that are added together to decide if the skill hits vs the targets evade.")
        use ON_SingleStatDisplay("Reduction: ", "[damageReduction]%", tooltipDisplay="Your % damage reduction to arousal, calculated from your willpower and relevant perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Effect Duration: ", "[statusDuration]%", tooltipDisplay="The bonus duration of your own status effects, base duration of a skill is increased by this percentage. Which is calculated by (int*0.5)% + perks. So at 100 int, skills would last 50% longer. Keep in mind skills that last 1 turn will be increased to 2, as all effects also last the turn they are cast. The turn count is always rounded down.")
        use ON_SingleStatDisplay("Effect Chance: ", "[statusAccuracyBonus]%", tooltipDisplay="Your base status effect accuracy is derived by the the individual skills stat used, its base chance, and this stat. Which is calculated from int-5(0.25% per point) + luck-5(0.1% per point) + perks. There's also a random roll(d100) added, that are then all added together to decide if the skill applies its status effect.")
        use ON_SingleStatDisplay("Status Res: ", "[statusEvadeBonus]%", tooltipDisplay="Your base status effect resistance based on your stats, this isn't counting any res to specific effects you might have, or any of the multiple other factors in combat that can increase your chance to be effected, such as being restrained, the attacks innate res stat, or its fetishes. This is calculated via will-5(0.25% per point) + luck-5(0.1% per point) + perks.")
        textbutton "" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
        use ON_SingleStatDisplay("Allure Bonus: ", "[flatAllureBonus]", tooltipDisplay="The flat boost to arousal dealt gained from your allure. Calculated by 10% of (Your total allure - 5), the 10% scaling can be increased by perks.")
        use ON_SingleStatDisplay("Allure Bonus%: ", "[percentAllureBonus]%", tooltipDisplay="The percentage here is the bonus arousal that will be added to your skill's base power from your allure. (Your Allure-5)*0.002*(multiplied by 100 to show the percent increase. Normally base skill power.) + Perk Bonus.")

screen ON_SensitivityListDisplay():
    use ON_Scrollbox("Sensitivity"):
        if TempSensitivity.getRes("Sex") <= 1:
            use ON_SingleDisplay("Cock: ", "[player.BodySensitivity.Sex]%", tooltipDisplay="How sensitive your penis is.")
        else:
            use ON_SingleDisplay("Cock: ", "[player.BodySensitivity.Sex]%", tooltipDisplay="How sensitive your penis is.\n\n(Cleanse [PlayerTempSensSex] at the church.)")

        if TempSensitivity.getRes("Ass") <= 1:
            use ON_SingleDisplay("Ass: ", "[player.BodySensitivity.Ass]%", tooltipDisplay="How sensitive your ass is. But I'm sure no monsters will actually go for your ass... R-Right?")
        else:
            use ON_SingleDisplay("Ass: ", "[player.BodySensitivity.Ass]%", tooltipDisplay="How sensitive your ass is. But I'm sure no monsters will actually go for your ass... R-Right?\n\n(Cleanse [PlayerTempSensAss] at the church.")

        if TempSensitivity.getRes("Nipples") <= 1:
            use ON_SingleDisplay("Nipples: ", "[player.BodySensitivity.Breasts]%", tooltipDisplay="How sensitive your nipples are! Bit of an odd thing for a guy to think about isn't it?")
        else:
            use ON_SingleDisplay("Nipples: ", "[player.BodySensitivity.Breasts]%", tooltipDisplay="How sensitive your nipples are! Bit of an odd thing for a guy to think about isn't it?\n\n(Cleanse [PlayerTempSensNipples] at the church.")

        if TempSensitivity.getRes("Mouth") <= 1:
            use ON_SingleDisplay("Mouth: ", "[player.BodySensitivity.Mouth]%", tooltipDisplay="Are romantic kisses your weakness? Or maybe having a girl sit on your face?")
        else:
            use ON_SingleDisplay("Mouth: ", "[player.BodySensitivity.Mouth]%", tooltipDisplay="Are romantic kisses your weakness? Or maybe having a girl sit on your face?\n\n(Cleanse [PlayerTempSensMouth] at the church.")

        if TempSensitivity.getRes("Seduction") <= 1:
            use ON_SingleDisplay("Seduction: ", "[player.BodySensitivity.Seduction]%", tooltipDisplay="Try not to stare too much at erotic displays, listen to honeyed words, okay?")
        else:
            use ON_SingleDisplay("Seduction: ", "[player.BodySensitivity.Seduction]%", tooltipDisplay="Try not to stare too much at erotic displays, listen to honeyed words, okay?\n\n(Cleanse [PlayerTempSensSeduction] at the church.")

        if TempSensitivity.getRes("Magic") <= 1:
            use ON_SingleDisplay("Magic: ", "[player.BodySensitivity.Magic]%", tooltipDisplay="Your body's innate ability to resist magical attacks!")
        else:
            use ON_SingleDisplay("Magic: ", "[player.BodySensitivity.Magic]%", tooltipDisplay="Your body's innate ability to resist magical attacks!\n\n(Cleanse [PlayerTempSensMagic] at the church.")

        if TempSensitivity.getRes("Pain") <= 1:
            use ON_SingleDisplay("Pain: ", "[player.BodySensitivity.Pain]%", tooltipDisplay="Do you like getting punished?")
        else:
            use ON_SingleDisplay("Pain: ", "[player.BodySensitivity.Pain]%", tooltipDisplay="Do you like getting punished?\n\n(Cleanse [PlayerTempSensPain] at the church.")

screen ON_FetishListDisplay():
    use ON_Scrollbox("Fetishes"):
        for fetish, tempFetish in zip(player.FetishList, TempFetishes):
            if fetish.Type == "Fetish":
                use ON_SingleFetishDisplay(fetish, fetish.Level, tempFetish.Level)

screen ON_PerkListDisplay():
    use ON_Scrollbox("Perks"):
        for perk in player.perks:
            if perk.PlayerCanPurchase != "HiddenCompletelyFromPlayer":
                $ theTimeType = ""
                for y in perk.PerkType:
                    if y == "TimeDuration" or y == "TurnDuration":
                        $ theTimeType = y
                use ON_SingleDisplay(perk.name, "", tooltipDisplay=perk.description, duration=perk.duration, timeType=theTimeType)

        if len(player.perks) == 0:
            use ON_SingleDisplay("None... yet!", "")

screen ON_PerkDisplay(perkTab, columns=1):
    $ perkDisplayItems = []
    $ spaceNext = 0
    for perk in player.perks:
        if (perkTab == 1 and perk.PlayerCanPurchase == "Yes" or
            perkTab == 2 and perk.PlayerCanPurchase == "No"):
            $ perkDisplayItems.append(perk)

    use ON_Scrollbox(""):
        fixed ysize 4 # spacing
        grid columns 1:
            xfill True
            for c in range(0, columns):
                vbox:
                    xfill True
                    for i in range(c, len(perkDisplayItems), columns):
                        use ON_SinglePerkDisplay(perkDisplayItems[i], spaceNext)
                    if len(player.perks) == 0:
                        use ON_SingleDisplay("None... yet!", "")

    for c in range(0, columns-1):
        $ pct = (1.0+c)/columns
        add "gui/framedivider211partial.png" xalign pct

screen ON_ResistanceListDisplay():
    use ON_Scrollbox("Resistances"):
        use ON_SingleStatDisplay("Stun:", "[player.resistancesStatusEffects.Stun]%", tooltipDisplay="Your resistance chance to being stunned.")
        use ON_SingleStatDisplay("Charm:", "[player.resistancesStatusEffects.Charm]%", tooltipDisplay="Your resistance chance to being charmed.")
        use ON_SingleStatDisplay("Aphrodisiac:", "[player.resistancesStatusEffects.Aphrodisiac]%", tooltipDisplay="Your resistance chance to being afflicted by aphrodisiacs and further increases to its potency.")
        use ON_SingleStatDisplay("Restraints:", "[player.resistancesStatusEffects.Restraints]%", tooltipDisplay="Your resistance chance to being restrained.")
        use ON_SingleStatDisplay("Sleep:", "[player.resistancesStatusEffects.Sleep]%", tooltipDisplay="Your resistance chance to being afflicted by drowzy.")
        use ON_SingleStatDisplay("Trance:", "[player.resistancesStatusEffects.Trance]%", tooltipDisplay="Your resistance chance to entering and falling deeper into a trance state.")
        use ON_SingleStatDisplay("Paralysis:", "[player.resistancesStatusEffects.Paralysis]%", tooltipDisplay="Your resistance chance to being afflicted by paralysis and further increases to its potency.")
        use ON_SingleStatDisplay("Debuff:", "[player.resistancesStatusEffects.Debuff]%", tooltipDisplay="Your resistance chance to being afflicted by general debuffs. Not including the other resistance types!")

screen ON_InventoryDisplay(inventoryType, columns=1):
    $ items = []
    $ spaceNext = 0
    #CODEMOD: Items should be added from stash if inventoryType is "Consumables" and MainOrStash is "Stash"
    $ usingStash = isInStashInventoryTab()
    if usingStash:
        for item in player.inventory.stash:
            if StashInventory.isConsumable(item):
                $ items.append(item)
    else:
        for item in player.inventory.items:
            if (inventoryType == "Consumables" and (item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable" or item.itemType == "NotCombatConsumable")
                or inventoryType == "RuneOrAccessory" and (item.itemType == "Rune" and RuneOrAccessory == "Rune")
                or inventoryType == "RuneOrAccessory" and (item.itemType == "Accessory"  and RuneOrAccessory == "Accessory")
                or inventoryType == "KeyItems" and (item.itemType == "Key")
                or inventoryType == "Loot" and (item.itemType == "Loot")):
                    $ items.append(item)
    use ON_Scrollbox(""):
        fixed ysize 4 # spacing
        grid columns 1:
            xfill True
            for c in range(0, columns):
                vbox:
                    xfill True
                    for i in range(c, len(items), columns):
                        use ON_SingleItemDisplay(items[i], spaceNext, usingStash)

    for c in range(0, columns-1):
        $ pct = (1.0+c)/columns
        add "gui/framedivider211partial.png" xalign pct

init python:
    inventoryTab = "Consumables"
    perkTab = 1
    characterMenuCanHover = True
    charSticky = ""

screen ON_CharacterDisplayScreen(TabToUse="Stats"):
    $ _game_menu_screen = "ON_CharacterDisplayScreen"

    tag menu

    $ tt = GetTooltip()
    default stickyDone = True

    default characterMenuTab = TabToUse

    $ relatedStat = player.stats.getStat("Power")
    $ powerBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ powerPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
    $ relatedStat = player.stats.getStat("Intelligence")
    $ intBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ intPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
    $ relatedStat = player.stats.getStat("Technique")
    $ techBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ techPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
    $ relatedStat = player.stats.getStat("Allure")
    $ allureBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ allurePerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
    $ relatedStat = player.stats.getStat("Willpower")
    $ willBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ willPerBoost = float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))
    $ relatedStat = player.stats.getStat("Luck")
    $ luckBoost = float("{0:.2f}".format(getStatFlatBonus(relatedStat)))
    $ luckPerBoost =  float("{0:.2f}".format(getStatPercentBonus(relatedStat, 100)))

    $ powerDisplay = player.stats.Power-player.getStatBonusReduction("Power")
    $ techDisplay = player.stats.Tech-player.getStatBonusReduction("Technique")
    $ intDisplay = player.stats.Int-player.getStatBonusReduction("Intelligence")
    $ allureDisplay = player.stats.Allure-player.getStatBonusReduction("Allure")
    $ willDisplay = player.stats.Willpower-player.getStatBonusReduction("Willpower")
    $ luckDisplay = player.stats.Luck-player.getStatBonusReduction("Luck")

    $ coreStatsList = []
    $ coreStatsList.append(player.stats.Power)
    $ coreStatsList.append(player.stats.Tech)
    $ coreStatsList.append(player.stats.Allure)
    $ coreStatsList.append(player.stats.Int)
    $ biggestStat = max(coreStatsList)*0.5
    $ statDamMod = biggestStat + (player.stats.Allure + player.stats.Tech + player.stats.Int +  player.stats.Power)/4

    $ flatCore = float("{0:.2f}".format(getCoreStatFlatBonus(statDamMod)))
    $ percentCore = float("{0:.2f}".format(getCoreStatPercentBonus(statDamMod, 100)))

    use game_menu(_("Character")):
        frame:
            xpos 0 ypos 40
            xsize 1440 ysize 222
            xpadding 102
            vbox:
                yalign 0.5
                text "[player.name]" size fontsize xoffset -2
                $ showLevelUp = InventoryAvailable and respeccing == 0 and (player.perkPoints >= 1 or player.SensitivityPoints >=1 or player.statPoints >= 1)
                textbutton "Level [player.stats.lvl]" text_size 24 text_color "#fff" xoffset -3
                fixed:
                    xsize 225 ysize 28
                    bar:
                        style "bar" 
                        xsize 225 ysize 28
                        value player.stats.Exp
                        range player.stats.ExpNeeded
                        alt ""
                    textbutton "XP: [player.stats.Exp]/[player.stats.ExpNeeded]" text_size 24 text_color "#fff":
                        alt "[player.stats.ExpNeeded - player.stats.Exp] XP needed to level up."
                    textbutton "                            " text_size 24: # If Renpy allows for either SetVariable or has working tooltip for bar in future, proceed to do the normal thing.
                        tooltip "[player.stats.ExpNeeded - player.stats.Exp] XP needed to level up."
                        alt ""
                        action NullAction()
                textbutton _("Virility: {color=#fff}[PlayerVirility]%{/color}") text_size 24 yalign 0.5:
                    tooltip "Measures the fertility of a man, as well as his semen's thickness, flavor, and nutritional value to monster girls. Increases the effectiveness of holy skills, and increases the effectiveness of monster girls energy draining and semen eating abilities on you. Equal to your (level-1)*0.5 + spirit*5 + 10 + any perks you have!"
                    alt "Virility: [PlayerVirility]%" + "\n\nMeasures the fertility of a man, as well as his semen's thickness, flavor, and nutritional value to monster girls. Increases the effectiveness of holy skills, and increases the effectiveness of monster girls energy draining and semen eating abilities on you. Equal to your (level-1)*0.5 + spirit*5 + 10 + any perks you have!"
                    action NullAction()
                if showLevelUp:
                    textbutton "Spend Unused stat points!":
                        text_size 26
                        action Jump("spendLvlUpPoints")

            vbox:
                xpos 430
                yalign 0.83
                textbutton _("Goddess' Favor: {color=#fff}[favorPool]/[PlayerFavor]{/color}") text_size 24 yalign 0.5:
                        if difficulty == "Hard":
                            tooltip "Whether or not you're actually blessed, Goddess' Favor allows you to automatically pass a number of failed checks per rest! Your pool of Goddess' Favor is equal to Luck/20, plus any extras from Perks. When you run out, you can still spend Energy to pass, but with increasing energy costs."
                        else:
                            tooltip "Whether or not you're actually blessed, Goddess' Favor allows you to automatically pass a number of failed checks per rest! Your pool of Goddess' Favor is equal to 1 + Luck/20, plus any extras from Perks. When you run out, you can still spend Energy to pass, but with increasing energy costs."
                        action NullAction()
                textbutton _("Strain: {color=#fff}[favorStrain]%{/color}") text_size 24 yalign 0.5:
                    tooltip "Increases Energy costs for surpassing stat checks. Resets to 0 on a rest."
                    action NullAction()

            vbox:
                yalign 0.0
                xpos 860 yoffset 38
                use ON_EquipSlot(player.inventory.RuneSlotOne, "Rune", 1)
                use ON_EquipSlot(player.inventory.RuneSlotTwo, "Rune", 2)
                use ON_EquipSlot(player.inventory.RuneSlotThree, "Rune", 3)
                use ON_EquipSlot(player.inventory.AccessorySlot, "Accessory", 4)
        # Health & Difficulty Overlay
        fixed:
            xpos 0 ypos 40
            fixed:
                xpos 720 ypos -68
                use ON_HealthDisplayInner(True, xOffset=0, menuCall=1)
            fixed xpos 1200 ypos -43:
                hbox:
                    textbutton "Difficulty: ":
                        text_size 24
                        style "button"
                        tooltip "Game difficulty. [PlayersInput] for difficulty information."
                        alt "Difficulty, [difficulty]. Select for difficulty information."
                        action [Show("difficulty_info")]
                    text "[difficulty]" size 24
        # Tab Buttons
        hbox:
            xpos 0 ypos 285
            fixed:
                xsize 240 ysize 45
                imagebutton:
                    default_focus True
                    idle "gui/tab_idle.png"
                    hover "gui/tab_hover.png"
                    selected_idle "gui/tab_selected.png" selected_hover "gui/tab_selected.png"
                    action [SetScreenVariable("characterMenuTab", "Stats")]
                    alt "Stats"
                text "Stats" xalign 0.5 yalign 0.5
            fixed:
                xsize 240 ysize 45
                imagebutton:
                    idle "gui/tab_idle.png"
                    hover "gui/tab_hover.png"
                    selected_idle "gui/tab_selected.png" selected_hover "gui/tab_selected.png"
                    action [SetScreenVariable("characterMenuTab", "Perks")]
                    alt "Perks"
                text "Perks" xalign 0.5 yalign 0.5

            fixed:
                xsize 240 ysize 45
                imagebutton:
                    idle "gui/tab_idle.png"
                    hover "gui/tab_hover.png"
                    selected_idle "gui/tab_selected.png" selected_hover "gui/tab_selected.png"
                    insensitive "gui/tab_insensitive.png"
                    action [SensitiveIf(InventoryAvailable == True), SetScreenVariable("characterMenuTab", "Skills")]
                    alt "Skills"
                text "Skills" xalign 0.5 yalign 0.5
            fixed:
                xsize 240 ysize 45
                imagebutton:
                    idle "gui/tab_idle.png"
                    hover "gui/tab_hover.png"
                    selected_idle "gui/tab_selected.png" selected_hover "gui/tab_selected.png"
                    insensitive "gui/tab_insensitive.png"
                    action [SensitiveIf(InventoryAvailable == True), SelectedIf(characterMenuTab == "Inventory"),
                    SetScreenVariable("characterMenuTab", "Inventory"), SetScreenVariable("theInventoryTab", "Consumables"), SetVariable("inventoryTab", "Consumables")]
                    alt "Inventory"
                text "Inventory" xalign 0.5 yalign 0.5

            fixed:
                frame:
                    xsize 275 ysize 51
                    xalign 1.0
                    xoffset -50
                    text "  Eros: ξ [player.inventory.money]" size on_listTitleSize yalign 0.5 xalign 0.25
        # Tab Frame
        frame:
            xsize 1440 ysize 367
            ypos 330

            if characterMenuTab == "Stats":
                use stats_tab
            elif characterMenuTab == "Perks":
                use perks_tab
            elif characterMenuTab == "Skills" and InventoryAvailable:
                use skills_tab
            elif characterMenuTab == "Inventory" and InventoryAvailable:
                use inventory_tab
            else:
                $ characterMenuTab = "Stats"
                use stats_tab
        # Dialogue Box
        frame:
            xsize 1440 ysize 262
            xpadding 12 ypadding 10
            ypos 705
            if characterMenuCanHover:
                if tt:
                    text "[tt!i]" size 30
                    if not renpy.variant("touch"):
                        timer 0.1 action SetVariable("charSticky", None)
                elif charSticky:
                    text "[charSticky!i]" size 30
                else:
                    text "" size 30
            else:
                if not tt:
                    timer 0.5 action SetVariable("characterMenuCanHover", True)
                text "[charSticky!i]" size 30


## CharacterMenuTab Screens ######################################################################
screen stats_tab():
    hbox:
        #if name == "Allure:" or name == "Technique:" or name == "Power:" or name == "Luck:" or name == "Willpower:":
        if renpy.variant("touch"):
            fixed:
                xsize 357 - gui.scrollbar_size
                ysize 352
                use ON_StatsListDisplay(True)
        else:
            fixed:
                xsize 357 - gui.scrollbar_size
                ysize 352
                use ON_StatsListDisplay(True)

        if renpy.variant("touch"):
            fixed xsize gui.scrollbar_size
            add Solid("#ef75c3") xsize 3 ysize 360
        else:
            fixed xsize gui.scrollbar_size
            add Solid("#ef75c3") xsize 3 ysize 360


        if renpy.variant("touch"):
            fixed:
                xsize 357 ysize 352
                use ON_SensitivityListDisplay
        else:
            fixed:
                xsize 357 ysize 352
                use ON_SensitivityListDisplay

        if renpy.variant("touch"):
            add Solid("#ef75c3") xsize 3 ysize 360
        else:
            add Solid("#ef75c3") xsize 3 ysize 360

        if renpy.variant("touch"):
            fixed:
                xsize 357 ysize 352
                use ON_FetishListDisplay
        else:
            fixed:
                xsize 357 ysize 352
                use ON_FetishListDisplay

        if renpy.variant("touch"):
            add Solid("#ef75c3") xsize 3 ysize 360
        else:
            add Solid("#ef75c3") xsize 3 ysize 360


        if renpy.variant("touch"):
            fixed:
                ysize 352
                use ON_ResistanceListDisplay
        else:
            fixed:
                ysize 352
                use ON_ResistanceListDisplay

screen perks_tab():
    hbox:
        vbox:
            hbox:
                fixed xsize 6 ysize 24 # spacing
                fixed:
                    xsize 192 ysize 36
                    imagebutton:
                        idle "gui/smalltab_idle.png"
                        hover "gui/smalltab_hover.png"
                        insensitive "gui/smalltab_selected.png"
                        action [SensitiveIf(perkTab != 1), SetVariable ("perkTab", 1)]
                        alt "Level Up Perks"
                    text "Level Up" xalign 0.5 yalign 0.5 size 22
                fixed:
                    xsize 192 ysize 36
                    imagebutton:
                        idle "gui/smalltab_idle.png"
                        hover "gui/smalltab_hover.png"
                        insensitive "gui/smalltab_selected.png"
                        action [SensitiveIf(perkTab != 2), SetVariable ("perkTab", 2)]
                        alt "Other Perks"
                    text "Other" xalign 0.5 yalign 0.5 size 22

            add Solid("#ef75c3") xsize 1080 ysize 3

            if renpy.variant("touch"):
                fixed:
                    xsize 1080 - gui.scrollbar_size
                    ysize 320
                    if len(player.perks) == 0:
                        use ON_PerkDisplay(perkTab, 1)
                    else:
                        use ON_PerkDisplay(perkTab, 2)
            else:
                fixed:
                    xsize 1080 - gui.scrollbar_size
                    ysize 320
                    if len(player.perks) == 0:
                        use ON_PerkDisplay(perkTab, 1)
                    else:
                        use ON_PerkDisplay(perkTab, 2)

        add Solid("#ef75c3") xsize 3 ysize 360

        vbox:
            xoffset 34
            text "Sort Options" xalign 0.5
            textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
            textbutton "Alphabetical" text_size on_listTextSize action [SortList(player.perks, lambda x: x.name)] xalign 0.5
            textbutton "Reverse Alphabetical" text_size on_listTextSize action [SortList(player.perks, lambda x: x.name, reverse=True)] xalign 0.5
            if perkTab == 1:
                textbutton "Highest Level Req" text_size on_listTextSize action [SortList(player.perks, lambda x: (x.StatReqAmount, x.LevelReq), reverse=True)] xalign 0.5
            if perkTab == 1:
                textbutton "Lowest Level Req" text_size on_listTextSize action [SortList(player.perks, lambda x: (x.StatReqAmount, x.LevelReq))] xalign 0.5

screen skills_tab():
    hbox:
        fixed:
            xsize 1080
            if renpy.variant("touch"):
                use ON_MenuSkillsList(height=357, xoff=5)
            else:
                use ON_MenuSkillsList(height=357)
        add Solid("#ef75c3") xsize 3 ysize 360
        vbox:
            xoffset 34
            text "Sort Options" xalign 0.5
            textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
            textbutton "Alphabetical" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.name)] xalign 0.5
            textbutton "Reverse Alphabetical" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.name, reverse=True)] xalign 0.5
            textbutton "Lowest Energy Cost" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.cost)] xalign 0.5
            textbutton "Highest Energy Cost" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.cost, reverse=True)] xalign 0.5
            textbutton "Lowest Damage" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.power + (player.stats.getStat(x.statType)-5)*0.3)] xalign 0.5
            textbutton "Highest Damage" text_size on_listTextSize action [SortList(player.skillList, lambda x: x.power + (player.stats.getStat(x.statType)-5)*0.3, reverse=True)] xalign 0.5
            if manualSort != "Skills":
                textbutton "Manual Sorting" text_size on_listTextSize action [Function(ActivateManualSorting, "Skills")] xalign 0.5
            else:
                textbutton "End Manual Sorting" text_size on_listTextSize action [Function(DeactivateManualSorting)] xalign 0.5
                if swappingSkill != -1:
                    $ showText = player.skillList[swappingSkill].name
                    textbutton "[showText]" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5

#CODEMOD
init python:
    MainOrStash = "Main"

screen inventory_tab():
    default theInventoryTab = "Consumables"
    hbox:
        vbox:
            hbox:
                fixed:
                    xsize 0 ysize 36
                #CODEMOD: Add functionality for Selecting between main and stash inventory when out of town
                textbutton _("Consumables"):
                    style "tab" text_style "text_tab" text_size 23 xminimum 192
                    action [SelectedIf(SetScreenVariable("theInventoryTab", "Consumables")), SetVariable("inventoryTab", "Consumables"), SetVariable("MainOrStash", "Main")]
                textbutton _("Equipment"):
                    style "tab" text_style "text_tab" text_size 23 xminimum 192
                    action [SelectedIf(SetScreenVariable("theInventoryTab", "Equipment")), SetVariable("inventoryTab", "RuneOrAccessory"), SetVariable("RuneOrAccessory", "Rune")]
                textbutton _("Key Items"):
                    style "tab" text_style "text_tab" text_size 23 xminimum 192
                    action [SelectedIf(SetScreenVariable("theInventoryTab", "Key Items")), SetVariable("inventoryTab", "KeyItems")]
                textbutton _("Loot"):
                    style "tab" text_style "text_tab" text_size 23
                    action [SelectedIf(SetScreenVariable("theInventoryTab", "Loot")), SetVariable("inventoryTab", "Loot")]
                if inventoryTab == "RuneOrAccessory":
                    fixed:
                        xsize 162 ysize 36
                        xoffset 30
                        imagebutton:
                            idle "gui/smallertab_idle_outline.png"
                            hover "gui/smallertab_hover_outline.png"
                            insensitive "gui/smallertab_selected.png"
                            action [SensitiveIf(RuneOrAccessory != "Rune"), SetVariable ("RuneOrAccessory", "Rune")]
                            alt "Runes"
                        text "Runes" xalign 0.5 yalign 0.5 size 22
                    fixed:
                        xsize 162 ysize 36
                        xoffset 30
                        imagebutton:
                            idle "gui/smallertab_idle_outline.png"
                            hover "gui/smallertab_hover_outline.png"
                            insensitive "gui/smallertab_selected.png"
                            action [SensitiveIf(RuneOrAccessory != "Accessory"), SetVariable ("RuneOrAccessory", "Accessory")]
                            alt "Accessories"
                        text "Accessories" xalign 0.5 yalign 0.5 size 22
                #CODEMOD: Stash Inventory options
                elif type(player.inventory) is StashInventory and player.inventory.stashActive and inventoryTab == "Consumables":
                    fixed:
                        xsize 162 ysize 36
                        xoffset 30
                        imagebutton:
                            idle "gui/smallertab_idle_outline.png"
                            hover "gui/smallertab_hover_outline.png"
                            insensitive "gui/smallertab_selected.png"
                            action [SensitiveIf(MainOrStash != "Main"), SetVariable ("MainOrStash", "Main")]
                            alt "Main"
                        text "Main" xalign 0.5 yalign 0.5 size 22
                    fixed:
                        xsize 162 ysize 36
                        xoffset 30
                        imagebutton:
                            idle "gui/smallertab_idle_outline.png"
                            hover "gui/smallertab_hover_outline.png"
                            insensitive "gui/smallertab_selected.png"
                            action [SensitiveIf(MainOrStash != "Stash"), SetVariable ("MainOrStash", "Stash")]
                            alt "Stash"
                        text "Stash" xalign 0.5 yalign 0.5 size 22

            add Solid("#ef75c3") xsize 1080 ysize 3

            if renpy.variant("touch"):
                fixed:
                    xsize 1080 - gui.scrollbar_size
                    ysize 320
                    use ON_InventoryDisplay(inventoryTab, 2)
            else:
                fixed:
                    xsize 1080 - gui.scrollbar_size
                    ysize 320
                    use ON_InventoryDisplay(inventoryTab, 2)

        add Solid("#ef75c3") xsize 3 ysize 360
        vbox:
            xoffset 34
            text "Sort Options" xalign 0.5
            textbutton "---" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5
            #CODEMOD: Added functionality for displaying stash items when neccessary
            textbutton "Alphabetical" text_size on_listTextSize action [SortList(getItemsOrStash(), lambda x: x.name, sortingItems=inventoryTab, runeOrAccessory=RuneOrAccessory, mainOrStash=MainOrStash)] xalign 0.5
            textbutton "Reverse Alphabetical" text_size on_listTextSize action [SortList(getItemsOrStash(), lambda x: x.name, reverse=True, sortingItems=inventoryTab, runeOrAccessory=RuneOrAccessory, mainOrStash=MainOrStash)] xalign 0.5
            if inventoryTab != "KeyItems":
                textbutton "Highest Value" text_size on_listTextSize action [SortList(getItemsOrStash(), lambda x: x.cost, reverse=True, sortingItems=inventoryTab, runeOrAccessory=RuneOrAccessory, mainOrStash=MainOrStash)] xalign 0.5
                textbutton "Lowest Value" text_size on_listTextSize action [SortList(getItemsOrStash(), lambda x: x.cost, sortingItems=inventoryTab, runeOrAccessory=RuneOrAccessory, mainOrStash=MainOrStash)] xalign 0.5
            if manualSort != "Items":
                textbutton "Manual Sorting" text_size on_listTextSize action [Function(ActivateManualSorting, "Items")] xalign 0.5
            else:
                textbutton "End Manual Sorting" text_size on_listTextSize action [Function(DeactivateManualSorting)] xalign 0.5
                if swappingItem != -1:
                    $ showText = player.inventory.items[swappingItem].name
                    textbutton "[showText]" text_size on_listTextSize text_color "#fff" ysize on_listTextSize xalign 0.5

## Perk Sorting ######################################################################
init python:

    class SortList(Action):

        def __init__(self, listToSort, sortKey, reverse=False, sortingItems=None, runeOrAccessory=None, mainOrStash=None):
            self.listToSort = listToSort
            self.sortKey = sortKey
            self.reverse = reverse
            self.sortingItems = sortingItems
            self.runeOrAccessory = runeOrAccessory
            #CODEMOD
            self.mainOrStash = mainOrStash 

        def __call__(self):
            if self.sortingItems == None:
                self.listToSort.sort(key=self.sortKey, reverse=self.reverse)
                cmenu_refreshSwapMenu()
            else:
                sorted_itemType = []
                unsorted_itemType = []
                for item in self.listToSort:
                    if self.sortingItems == "Consumables" and item.itemType in ["Consumable", "CombatConsumable", "NotCombatConsumable", "DissonantConsumable"]:
                        sorted_itemType.append(item)
                    elif self.sortingItems == "KeyItems" and item.itemType == "Key":
                        sorted_itemType.append(item)
                    elif self.sortingItems == "Loot" and item.itemType == "Loot":
                        sorted_itemType.append(item)
                    elif self.sortingItems == "RuneOrAccessory" and item.itemType in ["Accessory"] and self.runeOrAccessory == "Accessory":
                        sorted_itemType.append(item)
                    elif self.sortingItems == "RuneOrAccessory" and item.itemType in ["Rune"] and self.runeOrAccessory == "Rune":
                        sorted_itemType.append(item)
                    else:
                        unsorted_itemType.append(item)
                sorted_itemType.sort(key=self.sortKey, reverse=self.reverse)
                sorted_itemType.extend(unsorted_itemType)
                self.listToSort[:] = sorted_itemType

            renpy.restart_interaction()

    def ActivateManualSorting(typeofSort):
        global manualSort
        manualSort = str(typeofSort)

        cmenu_refreshSwapMenu()

    def DeactivateManualSorting():
        global manualSort
        manualSort = ""

        cmenu_refreshSwapMenu()

    def SetItemOrder(itemTarget):
        global swappingItem
        renpy.retain_after_load()
        if swappingItem == -1:
            swappingItem = itemTarget
        else:
            swapping = copy.copy(player.inventory.items[swappingItem])
            targeting = copy.copy(player.inventory.items[itemTarget])

            player.inventory.items[swappingItem] = targeting
            player.inventory.items[itemTarget] = swapping
            swappingItem = -1

    def SetSkillOrder():
        global swappingSkill
        renpy.retain_after_load()
        if swappingSkill == -1:
            swappingSkill = skillTarget
        else:
            xS = copy.copy(player.skillList[swappingSkill])
            yS = copy.copy(player.skillList[skillTarget])

            player.skillList[swappingSkill] = yS
            player.skillList[skillTarget] = xS
            cmenu_refreshSwapMenu()
            swappingSkill = -1

## Use ######################################################################
    def EquipItem(promptEquipping, equipmentSlot, equipmentTarget):
        renpy.retain_after_load()

        global itemChoice
        if equipmentTarget == None:
            pass
        else:
            itemChoice = player.inventory.items[equipmentTarget]

        if promptEquipping:
            if itemChoice.itemType == "Rune":
                if equipmentSlot == 1:
                    if player.inventory.RuneSlotOne.name != "Empty":
                        player.inventory.give(player.inventory.RuneSlotOne.name, 1)
                    player.inventory.equip(1, player, -1)
                    player.inventory.RuneSlotOne = itemChoice
                    player.inventory.equip(1, player, 1)
                if equipmentSlot == 2:
                    if player.inventory.RuneSlotTwo.name != "Empty":
                        player.inventory.give(player.inventory.RuneSlotTwo.name, 1)
                    player.inventory.equip(2, player, -1)
                    player.inventory.RuneSlotTwo = itemChoice
                    player.inventory.equip(2, player, 1)
                if equipmentSlot == 3:
                    if player.inventory.RuneSlotThree.name != "Empty":
                        player.inventory.give(player.inventory.RuneSlotThree.name, 1)
                    player.inventory.equip(3, player, -1)
                    player.inventory.RuneSlotThree = itemChoice
                    player.inventory.equip(3, player, 1)
            elif itemChoice.itemType == "Accessory":
                if player.inventory.AccessorySlot.name != "Empty":
                    player.inventory.give(player.inventory.AccessorySlot.name, 1)
                player.inventory.equip(4, player, -1)
                player.inventory.AccessorySlot = itemChoice
                player.inventory.equip(4, player, 1)

            if equipmentSlot == 1:
                player.inventory.useItem(player.inventory.RuneSlotOne.name)
            elif equipmentSlot == 2:
                player.inventory.useItem(player.inventory.RuneSlotTwo.name)
            elif equipmentSlot == 3:
                player.inventory.useItem(player.inventory.RuneSlotThree.name)
            elif equipmentSlot == 4:
                player.inventory.useItem(player.inventory.AccessorySlot.name)
        else:
            if equipmentSlot == 1:
                player.inventory.give(player.inventory.RuneSlotOne.name, 1)
                player.inventory.equip(1, player, -1)
                player.inventory.RuneSlotOne = Item("Empty", "Rune", "0")
            elif equipmentSlot == 2:
                player.inventory.give(player.inventory.RuneSlotTwo.name, 1)
                player.inventory.equip(2, player, -1)
                player.inventory.RuneSlotTwo = Item("Empty", "Rune", "0")
            elif equipmentSlot == 3:
                player.inventory.give(player.inventory.RuneSlotThree.name, 1)
                player.inventory.equip(3, player, -1)
                player.inventory.RuneSlotThree = Item("Empty", "Rune", "0")
            elif equipmentSlot == 4:
                player.inventory.give(player.inventory.AccessorySlot.name, 1)
                player.inventory.equip(4, player, -1)
                player.inventory.AccessorySlot = Item("Empty", "Accessory", "0")


        player.CalculateStatBoost()
        if player.stats.hp <= 0:
            player.stats.hp = 0
        if player.stats.ep >= player.stats.max_true_ep:
            player.stats.ep = player.stats.max_true_ep
        if player.stats.ep <= 0:
            player.stats.ep = 0
        if player.stats.sp >= player.stats.max_true_sp:
            player.stats.sp = player.stats.max_true_sp
        if player.stats.sp <= 0:
            player.stats.sp = 0
        
        global favorPool
        if favorPool > CalcGoddessFavor(player):
            favorPool = CalcGoddessFavor(player)

    def useInventoryItem(inventoryTarget):
        renpy.retain_after_load()

        global itemChoice
        itemChoice = player.inventory.items[copy.copy(inventoryTarget)]

        global attackerName ; attackerName = player.name
        global attackerHeOrShe ; attackerHeOrShe = getHeOrShe(player)
        global attackerHisOrHer ; attackerHisOrHer = getHisOrHer(player)
        global attackerHimOrHer ; attackerHimOrHer = getHimOrHer(player)
        global attackerYouOrMonsterName ; attackerYouOrMonsterName = getYouOrMonsterName(player)
        global characterMenuCanHover
        global displayingScene
        try:
            displayingScene.theScene
        except:
            displayingScene = Dialogue()


        global display ; display = ""
        global fetchSkill
        global menuItemChoice
        global holder
        global player
        global itemEvent
        global charSticky
        if len(itemChoice.skills) > 0 and itemChoice.itemType != "DissonantConsumable":
            player.inventory.useItem(itemChoice.name)
            fetchSkill = getFromName(itemChoice.skills[0], SkillsDatabase)
            menuItemChoice = copy.deepcopy(SkillsDatabase[fetchSkill])
            menuItemChoice.isSkill = itemChoice.itemType

            holder = HealCalc(player, menuItemChoice)
            player = holder[0]
            display += holder[1]

            characterMenuCanHover = False
            charSticky = display
            renpy.restart_interaction()

            if player.stats.Exp >= player.stats.ExpNeeded:

                global culmitiveLeveling ; culmitiveLeveling = 0
                global hpIncreases ; hpIncreases = 0
                global statPointIncreases ; statPointIncreases = 0
                global sensitivityIncreases ; sensitivityIncreases = 0
                global perkIncreases ; perkIncreases = 0
                renpy.jump("levelUpSpot")

        elif lineOfScene < len(displayingScene.theScene):
            display = "You can't use that right now."
            ttInput = display
            characterMenuCanHover = False
            charSticky = display
            renpy.restart_interaction()
        else:
            #renpy.curry(renpy.end_interaction)(True) # thought this might be able to close the menu before instigating an event to make shit work better. But it either crashes, or does nothing, seems to only work with a button, even if it did, im pretty sure it'd end the event before it started.
            player.inventory.useItem(itemChoice.name)
            display = itemChoice.useOutcome
            config.keymap['game_menu'].remove('mouseup_3')
            config.keymap['game_menu'].remove('K_ESCAPE')
            config.keymap['game_menu'].remove('K_MENU')
            renpy.clear_keymap_cache()
            itemEvent = 1
            renpy.jump("itemEventHandler")

    def useSkillFromMenu(useSkillTarget):
        renpy.retain_after_load()
        itemChoice = Item("Blank", "Null", 0)
        global display ; display = ""
        global finalDamage ; finalDamage = 0
        global skillChoice ; skillChoice = player.skillList[useSkillTarget]

        global attackerName ; attackerName = player.name
        global attackerHeOrShe ; attackerHeOrShe = getHeOrShe(player)
        global attackerHisOrHer ; attackerHisOrHer = getHisOrHer(player)
        global attackerHimOrHer ; attackerHimOrHer = getHimOrHer(player)
        global attackerYouOrMonsterName ; attackerYouOrMonsterName = getYouOrMonsterName(player)

        global holder ; holder = HealCalc(player, skillChoice)
        global player ; player = holder[0]

        global charSticky

        display += holder[1]

        if skillChoice.costType == "ep":
            player.stats.ep -= int(math.floor(skillChoice.cost*GetParalEnergyChange(player)+GetParalFlatEnergyChange(player)))
        elif skillChoice.costType == "hp":
            actualCost = skillChoice.cost + (player.stats.max_true_hp-100)*0.15
            actualCost = math.floor(actualCost)
            actualCost = int(actualCost)
            player.stats.hp += actualCost
        elif skillChoice.costType == "sp":
            player.stats.sp -= skillChoice.cost

        global characterMenuCanHover ; characterMenuCanHover = False
        charSticky = display
    
    #CODEMOD: Returns either the player's Inventory or Stash depending on whether the stash is being displayed
    def isInStashInventoryTab():
        global inventoryTab
        global MainOrStash
        return type(player.inventory) is StashInventory and inventoryTab == "Consumables" and MainOrStash == "Stash"

    def getItemsOrStash():
        if isInStashInventoryTab():
            return player.inventory.stash
        else:
            return player.inventory.items 

label itemEventHandler():
    call read() from _call_read_1
    $ itemEvent = 0
    $ config.keymap['game_menu'].append('mouseup_3')
    $ config.keymap['game_menu'].append('K_ESCAPE')
    $ config.keymap['game_menu'].append('K_MENU')
    $ renpy.clear_keymap_cache()
