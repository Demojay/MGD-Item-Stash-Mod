init python:
    def PrintException(fileName):
        exc_type, exc_obj, tb = sys.exc_info()
        raise renpy.error('EXCEPTION IN ({}): \n{}'.format(fileName, exc_obj))
    def AdditionCheck(databaseType, nameValue):
        try:
            if currentData["Addition"] == "Yes":
                additionLocation = getFromName(currentData[nameValue], databaseType)
                return additionLocation
            else:
                additionError = str(currentData["Addition"])
                renpy.error('Addition key was given an invalid value: %s \nValid values: "Yes"'%additionError)
        except KeyError:
            pass
    def EnsureAttrList(attr):
        if isinstance(attr, (str, unicode)):
            return [attr]
        return attr
    def PurgeAttrList(attrList):
        evilRenpyIsIstanceNoWork = attrList + []
        index = 0
        while index < len(attrList):
            if attrList[index] in ["Any", "None", ""]:
                attrList.pop(index)
            else:
                index += 1
        return attrList

    def StanceConditionCheck():
        global SkillsDatabase
        for skillJson in SkillsDatabase:
            for condition in skillJson.stanceConditions:
                if "theStance" in condition:
                    stance = condition["theStance"]
                    for skillKey, skills in condition["addingToSkills"].items():
                        for eachSkill in skills:
                            if validateJsons and not loadingDatabaseType:
                                validator.validateIDname(eachSkill, skillJson.name, "Skills", "Skills", "stanceCondition", jsonType="Skills")
                            for skillData in SkillsDatabase:
                                if skillData.name == eachSkill:
                                    try:
                                        currentValue = PurgeAttrList(getattr(skillData, skillKey))
                                        currentValue.append(stance)
                                    except TypeError:
                                        if getattr(skillData, skillKey) not in ["Any", "None", ""]:
                                            currentValue = [getattr(skillData, skillKey), stance]
                                        else:
                                            currentValue = stance
                                    if skillKey == "unusableIfStance":
                                        skillData.unusableIfStance = currentValue
                                    elif skillKey == "requiresStance":
                                        skillData.requiresStance = currentValue
                                    elif skillKey == "unusableIfTarget":
                                        skillData.unusableIfTarget = currentValue
                                    elif skillKey == "requiresTargetStance":
                                        skillData.requiresTargetStance = currentValue
                elif "theStanceSet" in condition:
                    stanceSet = condition["theStanceSet"]
                    for skill in condition["unusableIfTargetHasTheseSets"]:
                        for skillData in SkillsDatabase:
                            if skillData.name == skill:
                                try:
                                    currentValue = PurgeAttrList(getattr(skillData, skillKey), stanceSet)
                                    currentValue.append(stance)
                                except TypeError:
                                    if getattr(skillData, skillKey) not in ["Any", "None", ""]:
                                        currentValue = [getattr(skillData, skillKey), stance]
                                    else:
                                        currentValue = stance
                                skillData.unusableIfTargetHasTheseSets = currentValue

label loadDatabase:
    python:
        # To enable json validation, toggle below value from False to True.
        validateJsons = False
        if persistent.validatorAtStartup or persistent.validatorAtReload:
            validateJsons = True
            validator = LoadValidator()
        # Follow these comments to benchmark processing loops. View from either terminal or log.txt
        # You can uncomment any '#print(each)' to get the file names next to the timings. Affects timings. Side note, time.clock() is deprecated in python 3.3
        # benchstart = time.perf_counter()
        # ...at the end of the loop/process you're benchmarking... (Python 3)
        # benchtime = time.perf_counter()
        # print("Section Name Here:", benchtime - benchstart)
        ###############################FETISH LIST###############################
        if loadingDatabaseType == 0:
            for each in dynamic_loader(".*/Fetishes/.*"):
                #print(each)
                with renpy.file(each) as file:
                    fileName = file.read().decode("utf-8")
                try:
                    currentData = json.loads(fileName)
                except:
                    PrintException(fileName)

                for FL in currentData['FetishList']:
                    newFetish = Fetish()

                    newFetish.name = FL["Name"]
                    newFetish.Level = int(FL["BaseLevel"])
                    newFetish.Type = FL["Type"]
                    newFetish.CreationOn = FL["CreationOn"]
                    newFetish.CreationOff = FL["CreationOff"]
                    newFetish.toolTip = (FL.get("ToolTip", ""))
                    newFetish.levelText = [[int(fet[0]), fet[1]] for fet in FL.get("LevelText", [])]
                    FetishList.append(newFetish)

                    if validateJsons and not loadingDatabaseType:
                        validator.addIDToDatabase(newFetish.name, "Fetishes")

    ############################### LOAD SKILLS ###############################
        if loadingDatabaseType == 0:
            for each in dynamic_loader(".*/Skills/.*"):
                #print(each)
                with renpy.file(each) as file:
                    fileName = file.read().decode("utf-8")
                try:
                    currentData = json.loads(fileName)
                except:
                    PrintException(fileName)

                additionLocation = AdditionCheck(SkillsDatabase, "name")

                statusScale = int(currentData.get("statusEffectScaling", 100))
                withStatusScale = currentData.get("scalesWithStatusEffect", "")
                powerSFScaling = int(currentData.get("flatDamageSF-FlatScaling", 0))
                flatSFScaling = float(currentData.get("flatDamageSF-PercentScaling", 0.0))
                totalSFScaling = int(currentData.get("totalDamageSF-PercentScaling", 0))
                statusStacks = int(currentData.get("statusStacks", 0))

                try:
                    unusableSets = []
                    for each in currentData["unusableIfTargetHasTheseSets"]:
                        unusableSet = []
                        for array in each:
                            unusableSet.append(array)
                        unusableSets.append(unusableSet)
                except:
                    unusableSets = []

                critChance = int(currentData.get("critChance", 0))
                critDamage = int(currentData.get("critDamage", 0))
                accuracy = int(currentData.get("accuracy", 0))
                initiative = int(currentData.get("initiative", 0))

                requiresStatusEffectSelf = currentData.get("requiresStatusEffectSelf", "None")
                requiresStatusPotencySelf = int(currentData.get("requiresStatusPotencySelf", 0))
                unusableIfStatusEffectSelf = currentData.get("unusableIfStatusEffectSelf", ["None"])

                unusableIfStatusPotency = currentData.get("unusableIfStatusPotency", ["0"])

                requiresPerk = currentData.get("requiresPerk", [])
                requiresOnePerk = currentData.get("requiresOnePerk", [])
                unusableIfPerk = currentData.get("unusableIfPerk", [])
                requiresPerkSelf = currentData.get("requiresPerkSelf", [])
                requiresOnePerkSelf = currentData.get("requiresOnePerkSelf", [])
                unusableIfPerkSelf = currentData.get("unusableIfPerkSelf", [])

                restraintStruggle = EnsureAttrList(currentData["restraintStruggle"])
                restraintStruggleCharmed = EnsureAttrList(currentData["restraintStruggleCharmed"])
                restraintEscaped = EnsureAttrList(currentData["restraintEscaped"])
                restraintEscapedFail = EnsureAttrList(currentData["restraintEscapedFail"])
                restraintOnLoss = EnsureAttrList(currentData.get("restraintOnLoss", [""]))
                startsStance = EnsureAttrList(currentData["startsStance"])
                removeStance = EnsureAttrList(currentData["removesStance"])

                if additionLocation != None:
                    for each in currentData["fetishTags"]:
                        if each != "":
                            if SkillsDatabase[additionLocation].fetishTags[0] == "":
                                SkillsDatabase[additionLocation].fetishTags[0] = each
                            else:
                                SkillsDatabase[additionLocation].fetishTags.append(each)
                    for each in startsStance:
                        if each != "":
                            if SkillsDatabase[additionLocation].startsStance[0] == "":
                                SkillsDatabase[additionLocation].startsStance[0] = each
                            else:
                                SkillsDatabase[additionLocation].startsStance.append(each)

                    for each in currentData["unusableIfStance"]:
                        if each != "":
                            if SkillsDatabase[additionLocation].unusableIfStance[0] == "":
                                SkillsDatabase[additionLocation].unusableIfStance[0] = each
                            else:
                                SkillsDatabase[additionLocation].unusableIfStance.append(each)
                    for each in currentData["requiresTargetStance"]:
                        if each != "":
                            if SkillsDatabase[additionLocation].requiresTargetStance[0] == "":
                                SkillsDatabase[additionLocation].requiresTargetStance[0] = each
                            else:
                                SkillsDatabase[additionLocation].requiresTargetStance.append(each)
                    for each in currentData["unusableIfTarget"]:
                        if each != "":
                            if SkillsDatabase[additionLocation].unusableIfTarget[0] == "":
                                SkillsDatabase[additionLocation].unusableIfTarget[0] = each
                            else:
                                SkillsDatabase[additionLocation].unusableIfTarget.append(each)
                    for each in removeStance:
                        if each != "":
                            if SkillsDatabase[additionLocation].removesStance[0] == "":
                                SkillsDatabase[additionLocation].removesStance[0] = each
                            else:
                                SkillsDatabase[additionLocation].removesStance.append(each)


                if additionLocation == None:
                    blankSkill = Skill(
                    currentData["name"],
                    currentData["cost"],
                    currentData["costType"],
                    currentData["skillType"],
                    currentData["statType"],
                    currentData["skillTags"],
                    currentData["fetishTags"],
                    startsStance,
                    currentData.get("requiresStance", [""]),
                    currentData.get("unusableIfStance", [""]),
                    currentData.get("requiresTargetStance", [""]),
                    currentData.get("unusableIfTarget", [""]),
                    removeStance,
                    currentData["requiresStatusEffect"],
                    int(currentData["requiresStatusPotency"]),
                    currentData["unusableIfStatusEffect"],
                    unusableIfStatusPotency,
                    requiresStatusEffectSelf,
                    requiresStatusPotencySelf,
                    unusableIfStatusEffectSelf,
                    requiresPerk,
                    requiresOnePerk,
                    unusableIfPerk,
                    requiresPerkSelf,
                    requiresOnePerkSelf,
                    unusableIfPerkSelf,
                    int(currentData["power"]),
                    float(currentData["minRange"]),
                    float(currentData["maxRange"]),
                    int(currentData["recoil"]),
                    critChance,
                    critDamage,
                    currentData["targetType"],
                    accuracy,
                    initiative,
                    currentData["statusEffect"],
                    int(currentData["statusChance"]),
                    int(currentData["statusDuration"]),
                    float(currentData["statusPotency"]),
                    currentData["statusResistedBy"],
                    currentData["statusText"],
                    currentData["descrip"],
                    currentData["outcome"],
                    currentData["miss"],
                    currentData["statusOutcome"],
                    currentData["statusMiss"],
                    restraintStruggle,
                    restraintStruggleCharmed,
                    restraintEscaped,
                    restraintEscapedFail,
                    restraintOnLoss,
                    int(currentData["learningCost"]),
                    int(currentData["requiredStat"]),
                    int(currentData["requiredLevel"]),
                    statusScale,
                    withStatusScale,
                    powerSFScaling,
                    flatSFScaling,
                    totalSFScaling,
                    unusableSets,
                    currentData.get("stanceConditions", []),
                    statusStacks)

                    if validateJsons and not loadingDatabaseType:
                        validate_skill_arrays = [
                            blankSkill.outcome,
                            blankSkill.miss,
                            blankSkill.statusOutcome,
                            blankSkill.statusMiss,
                            blankSkill.restraintStruggle,
                            blankSkill.restraintStruggleCharmed,
                            blankSkill.restraintEscaped,
                            blankSkill.restraintEscapedFail,
                            blankSkill.restraintOnLoss,
                        ]

                        validator.addIDToDatabase(blankSkill.name, "Skills")

                        for skill_value in validate_skill_arrays:
                            if isinstance(skill_value, list):
                                for string in skill_value:
                                    validator.checkCombatLine(string, fileName)
                            else:
                                validator.checkCombatLine(skill_value, fileName)


                    if loadingDatabaseType == 0:
                        SkillsDatabase.append(blankSkill)    #add to list

            StanceConditionCheck()


    ################################ LOAD PERKS ###############################
        emergencyPerkUpdate = 0
        if loadingDatabaseType == 1:
            if len(PerkDatabase) != perkLenCheck:

                emergencyPerkUpdate = 1
                PerkDatabase = []

        if loadingDatabaseType == 0 or emergencyPerkUpdate == 1:
            perkListData = []
            for perks in dynamic_loader(".*/Perks/.*"):
                #print(each)
                with renpy.file(perks) as file:
                    fileName = file.read().decode("utf-8")
                try:
                    currentData = json.loads(fileName)
                except:
                    PrintException(fileName)

                newStatReq = []
                for each in currentData["StatReqAmount"]:
                    newStatReq.append(int(each))

                newEffectPower = []
                for each in currentData["EffectPower"]:
                    try:
                        newEffectPower.append(int(each))
                    except:
                        newEffectPower.append(each)

                blankPerk = Perk(
                currentData["name"],
                currentData["description"],
                int(currentData["LevelReq"]),
                currentData["PerkReq"],
                currentData["StatReq"],
                newStatReq,
                currentData["PerkType"],
                newEffectPower,
                currentData["PlayerCanPurchase"])


                for p in range(len(blankPerk.PerkType)):
                    if blankPerk.PerkType[p] == "TimeDuration" or blankPerk.PerkType[p] == "TurnDuration":
                        blankPerk.duration = copy.deepcopy(blankPerk.EffectPower[p])

                PerkDatabase.append(copy.deepcopy(blankPerk))    #add to list

                if validateJsons and not loadingDatabaseType:
                    validator.addIDToDatabase(blankPerk.name, "Perks")

            LocatePerkOrder = renpy.file("Json/Perks/_LevelUpPerkOrder.json").read().decode("utf-8")
            PerkOrderFile = json.loads(LocatePerkOrder)
            LevelingPerkDatabase = []
            for orderedPerk in PerkOrderFile["Order"]:
                for perk in PerkDatabase:
                    if perk.name == orderedPerk:
                        LevelingPerkDatabase.append(perk)
                        break
            PerkDatabaseLVLDisplay = copy.copy(LevelingPerkDatabase)

            AdditionalLevelPerks = [perk for perk in PerkDatabase if perk.PlayerCanPurchase == "Yes" and perk not in LevelingPerkDatabase]
            LevelingPerkDatabase.extend(AdditionalLevelPerks)

            if loadingDatabaseType == 0:
                perkLenCheck = copy.deepcopy(len(PerkDatabase))

    ############################### LOAD ITEMS ################################
        if loadingDatabaseType == 0:
            for each in dynamic_loader(".*/Items/.*"):
                #print(each)
                with renpy.file(each) as file:
                    fileName = file.read().decode("utf-8")
                try:
                    currentData = json.loads(fileName)
                except:
                    PrintException(fileName)
                
                #CODEMOD: Add ability to set "consumableLimit" for existing and new items
                additionLocation = AdditionCheck(ItemDatabase, "name")

                if additionLocation != None:
                    ItemDatabase[additionLocation].consumableLimit = currentData.get("consumableLimit", -1)
                else:
                    NewItemBodySensitivity = BodySensitivity()
                    NewItemStatusEffectsRes = ResistancesStatusEffects()

                    NewItemBodySensitivity.Sex = int(currentData["BodySensitivity"]["Sex"])
                    NewItemBodySensitivity.Ass = int(currentData["BodySensitivity"]["Ass"])
                    NewItemBodySensitivity.Breasts = int(currentData["BodySensitivity"]["Breasts"])
                    NewItemBodySensitivity.Mouth = int(currentData["BodySensitivity"]["Mouth"])
                    NewItemBodySensitivity.Seduction = int(currentData["BodySensitivity"]["Seduction"])
                    NewItemBodySensitivity.Magic = int(currentData["BodySensitivity"]["Magic"])
                    NewItemBodySensitivity.Pain = int(currentData["BodySensitivity"]["Pain"])
                    NewItemBodySensitivity.Holy = int(currentData["BodySensitivity"]["Holy"])
                    NewItemBodySensitivity.Unholy = int(currentData["BodySensitivity"]["Unholy"])

                    NewItemStatusEffectsRes.Stun = int(currentData["resistancesStatusEffects"]["Stun"])
                    NewItemStatusEffectsRes.Charm = int(currentData["resistancesStatusEffects"]["Charm"])
                    NewItemStatusEffectsRes.Aphrodisiac = int(currentData["resistancesStatusEffects"]["Aphrodisiac"])
                    NewItemStatusEffectsRes.Restraints = int(currentData["resistancesStatusEffects"]["Restraints"])
                    NewItemStatusEffectsRes.Sleep = int(currentData["resistancesStatusEffects"]["Sleep"])
                    NewItemStatusEffectsRes.Trance = int(currentData["resistancesStatusEffects"]["Trance"])
                    NewItemStatusEffectsRes.Paralysis = int(currentData["resistancesStatusEffects"]["Paralysis"])

                    NewItemStatusEffectsRes.Debuff = int(currentData["resistancesStatusEffects"].get("Debuff", 0))

                    itemSkills = currentData.get("skills", [])
                    onEquip = currentData.get("onEquip", "")
                    onUnequip = currentData.get("onUnequip", "")

                    requirementList = []
                    try:
                        for each in currentData["requiresEvent"]:
                            newRequirement=Requirements()
                            newRequirement.NameOfEvent = each["NameOfEvent"]
                            newRequirement.Progress = int(each["Progress"])
                            newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                            newRequirement.Choice = each["Choice"]

                            requirementList.append(copy.deepcopy(newRequirement))
                    except:
                        requirementList = [Requirements()]
                    
                    #CODEMOD
                    newConsumableLimit = currentData.get("consumableLimit", -1)

                    if loadingDatabaseType == 0:
                        blankItem = Item(
                        currentData["name"],
                        currentData["itemType"],
                        int(currentData["cost"]),
                        currentData.get("tags", []),
                        currentData["requires"],
                        requirementList,
                        int(currentData["hp"]),
                        int(currentData["ep"]),
                        int(currentData["sp"]),
                        int(currentData["Exp"]),
                        int(currentData["Power"]),
                        int(currentData["Technique"]),
                        int(currentData["Intelligence"]),
                        int(currentData["Allure"]),
                        int(currentData["Willpower"]),
                        int(currentData["Luck"]),
                        currentData["statusEffect"],
                        float(currentData["statusChance"]),
                        float(currentData["statusPotency"]),
                        currentData["descrip"],
                        currentData["useOutcome"],
                        currentData["useMiss"],
                        NewItemBodySensitivity,
                        NewItemStatusEffectsRes,
                        currentData["perks"],
                        itemSkills,
                        "False",
                        newConsumableLimit)

                        ItemDatabase.append(blankItem)    #add to list

                        if validateJsons and not loadingDatabaseType:
                            validate_item_arrays = [
                                blankItem.useOutcome,
                                blankItem.useMiss,
                            ]

                            validator.addIDToDatabase(blankItem.name, "Items")

                            for item_value in validate_item_arrays:
                                if isinstance(item_value, list):
                                    for string in item_value:
                                        validator.checkCombatLine(string, fileName)
                                else:
                                    validator.checkCombatLine(item_value, fileName)



    ############################### LOAD MONSTERS #############################
        for each in dynamic_loader(".*/Monsters/.*"):
            #print(each)
            with renpy.file(each) as file:
                fileName = file.read().decode("utf-8")
            try:
                currentData = json.loads(fileName)
            except:
                PrintException(fileName)
            NewMonSkillList = []
            NewMonPerks = []
            NewMonStats = Stats()
            newLossScenes = []
            newVictoryScenes = []
            newDialogue = []
            newDropList = []
            NewMonBodySensitivity = BodySensitivity()
            NewMonsStatusEffectsRes = ResistancesStatusEffects()
            startupLoading = 0

            additionLocation = AdditionCheck(MonsterDatabase, "IDname")

            requirementList = []
            try:
                for each in currentData["requiresEvent"]:
                    newRequirement=Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    requirementList.append(copy.deepcopy(newRequirement))
            except:
                requirementList = [Requirements()]


            for each in currentData["skillList"]:
                if each != "":
                    dataTarget = getFromName(each, SkillsDatabase)
                    blankSkill = SkillsDatabase[dataTarget]

                    if validateJsons and not loadingDatabaseType:
                        validator.validateIDname(each, currentData["IDname"], "Skills", "Monsters", "skillList", jsonType="Monsters")

                    if additionLocation != None:
                        if loadingDatabaseType == 0:
                            MonsterDatabase[additionLocation].skillList.append(blankSkill)
                    else:
                        NewMonSkillList.append(blankSkill)

            if additionLocation != None:
                for each in currentData["perks"]:
                    if each != "":
                        if loadingDatabaseType == 0:
                            MonsterDatabase[additionLocation].giveOrTakePerk(each, 1)

            if validateJsons and not loadingDatabaseType:
                for each in currentData["perks"]:
                    validator.validateIDname(each, currentData["IDname"], "Perks", "Monsters", "perks", jsonType="Monsters")

            for each in currentData["ItemDropList"]:
                blankItemDrop = ItemDrop()
                blankItemDrop.name = each["name"]
                blankItemDrop.dropChance = int(each["dropChance"])
                if validateJsons and not loadingDatabaseType:
                    validator.validateIDname(each["name"], currentData["IDname"], "Items", "Monsters", "ItemDropList", jsonType="Monsters")
                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        MonsterDatabase[additionLocation].ItemDropList.append(blankItemDrop)
                else:
                    newDropList.append(blankItemDrop)


            if additionLocation == None:
                NewMonStats.lvl = int(currentData["stats"]["lvl"])
                NewMonStats.Exp = int(currentData["stats"]["Exp"])
                NewMonStats.max_hp = int(currentData["stats"]["max_hp"])
                NewMonStats.max_ep = int(currentData["stats"]["max_ep"])
                NewMonStats.max_sp = int(currentData["stats"]["max_sp"])
                NewMonStats.Power = int(currentData["stats"]["Power"])
                NewMonStats.Tech = int(currentData["stats"]["Technique"])
                NewMonStats.Int = int(currentData["stats"]["Intelligence"])
                NewMonStats.Allure = int(currentData["stats"]["Allure"])
                NewMonStats.Willpower = int(currentData["stats"]["Willpower"])
                NewMonStats.Luck = int(currentData["stats"]["Luck"])
                NewMonStats.max_true_hp = NewMonStats.max_hp
                NewMonStats.max_true_ep = NewMonStats.max_ep
                NewMonStats.max_true_sp = NewMonStats.max_sp
                NewMonStats.ep = NewMonStats.max_ep
                NewMonStats.sp = NewMonStats.max_sp

                NewMonBodySensitivity.Sex = int(currentData["BodySensitivity"]["Sex"])
                NewMonBodySensitivity.Ass = int(currentData["BodySensitivity"]["Ass"])
                NewMonBodySensitivity.Breasts = int(currentData["BodySensitivity"]["Breasts"])
                NewMonBodySensitivity.Mouth = int(currentData["BodySensitivity"]["Mouth"])
                NewMonBodySensitivity.Seduction = int(currentData["BodySensitivity"]["Seduction"])
                NewMonBodySensitivity.Magic = int(currentData["BodySensitivity"]["Magic"])
                NewMonBodySensitivity.Pain = int(currentData["BodySensitivity"]["Pain"])
                NewMonBodySensitivity.Holy = int(currentData["BodySensitivity"]["Holy"])
                NewMonBodySensitivity.Unholy = int(currentData["BodySensitivity"]["Unholy"])

                NewMonsStatusEffectsRes.Stun = int(currentData["resistancesStatusEffects"]["Stun"])
                NewMonsStatusEffectsRes.Charm = int(currentData["resistancesStatusEffects"]["Charm"])
                NewMonsStatusEffectsRes.Aphrodisiac = int(currentData["resistancesStatusEffects"]["Aphrodisiac"])
                NewMonsStatusEffectsRes.Restraints = int(currentData["resistancesStatusEffects"]["Restraints"])
                NewMonsStatusEffectsRes.Sleep = int(currentData["resistancesStatusEffects"]["Sleep"])
                NewMonsStatusEffectsRes.Trance = int(currentData["resistancesStatusEffects"]["Trance"])
                NewMonsStatusEffectsRes.Paralysis = int(currentData["resistancesStatusEffects"]["Paralysis"])

                NewMonsStatusEffectsRes.Debuff = int(currentData["resistancesStatusEffects"].get("Debuff", 0))

                monFetishList = copy.deepcopy(FetishList)
                for each in currentData["Fetishes"]:
                    for fetish in monFetishList:
                        fetishSplit = each.partition("|/|")
                        if fetish.name == fetishSplit[0]:
                            fetish.Level += int(fetishSplit[2])
                        if validateJsons and not loadingDatabaseType:
                            validator.validateIDname(fetishSplit[0], currentData["IDname"], "Fetishes", "Monsters", "Fetishes", jsonType="Monsters")


            for each in currentData["lossScenes"]:
                blankScene = LossScene()

                blankScene.NameOfScene = each["NameOfScene"]
                blankScene.move = each["move"]
                blankScene.stance = each["stance"]

                blankScene.includes = each["includes"]

                blankScene.theScene = each["theScene"]

                blankScene.picture = each["picture"]
                if validateJsons and not loadingDatabaseType:
                    validator.checkEventText(currentData["IDname"], blankScene, fileName, jsonType="Monsters")
                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        MonsterDatabase[additionLocation].lossScenes.append(blankScene)
                else:
                    newLossScenes.append(blankScene)


            for each in currentData["victoryScenes"]:
                blankScene = LossScene()

                blankScene.NameOfScene = each["NameOfScene"]
                blankScene.move = each["move"]
                blankScene.stance = each["stance"]

                blankScene.includes = each["includes"]

                blankScene.theScene = each["theScene"]

                blankScene.picture = each["picture"]
                if validateJsons and not loadingDatabaseType:
                    validator.checkEventText(currentData["IDname"], blankScene, fileName, jsonType="Monsters")
                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        MonsterDatabase[additionLocation].victoryScenes.append(blankScene)
                else:
                    newVictoryScenes.append(blankScene)

            for each in currentData["combatDialogue"]:
                blankDia = CombatDialogue()

                blankDia.lineTrigger = each["lineTrigger"]
                if isinstance(each["move"], (str, unicode)):
                    blankDia.move = [each["move"]]
                else:
                    blankDia.move = each["move"]
                try:
                    blankDia.triggersOnce = each["triggersOnce"]
                except:
                    pass

                blankDia.theText = each["theText"]

                if validateJsons and not loadingDatabaseType:
                    for line in blankDia.theText:
                        validator.checkCombatLine(line, fileName)
                    # Awaiting stances implementation.
                    # try:
                    #     evilRenpyIsIstanceNoWork = each["move"] + []
                    #     for move in each["move"]:
                    #         validator.validateIDname(move, currentData["IDname"], "Skills", "Monsters", "combatDialogue", jsonType="Monsters")
                    # except TypeError:
                    #     validator.validateIDname(each["move"], currentData["IDname"], "Skills", "Monsters", "combatDialogue", jsonType="Monsters")

                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        existCheck = -1
                        countT = 0
                        for checkIt in MonsterDatabase[additionLocation].combatDialogue:
                            if checkIt.lineTrigger == blankDia.lineTrigger and checkIt.move == blankDia.move:
                                existCheck = copy.deepcopy(countT)
                            countT += 1

                        if existCheck != -1:
                            MonsterDatabase[additionLocation].combatDialogue[existCheck] = blankDia
                            #del MonsterDatabase[additionLocation].combatDialogue[existCheck]
                            #MonsterDatabase[additionLocation].combatDialogue.append(blankDia)
                        else:
                            MonsterDatabase[additionLocation].combatDialogue.append(blankDia)
                else:
                    newDialogue.append(blankDia)

            inSet = 0
            FullSet = []
            try:
                for each in currentData["pictures"]:
                    hasSets = 1
                    newSet = []
                    tempSet = PictureSet()
                    tempSet.ImageSet = []
                    tempSet.Roles = []
                    newRoles = []

                    try:
                        each["Set"]
                        tempSet.name = each["Name"]
                        for setContents in each["Set"]:
                                newSet.append(setContents)

                        setInserted = -1
                        if additionLocation != None:
                            l = 0
                            for layers in MonsterDatabase[additionLocation].ImageSets:
                                if each["Name"] == layers.name:
                                    setInserted = l
                                    break
                                l += 1
                    except:
                        setInserted = 0
                        tempSet.name = "Base"
                        newSet = currentData["pictures"]
                        hasSets = 0


                    for contents in newSet:

                        blankLayer = ImageLayer()
                        blankLayer.Images = []


                        blankRole = CGRole()
                        blankRole.Translators = []
                        blankRole.ToggledOnPartsWhenReqMet = []

                        CheckRole = ""

                        CheckRole = contents.get("Role", "")

                        if CheckRole == "":
                            layerInserted = -1
                            if additionLocation != None:
                                l = 0
                                for layers in MonsterDatabase[additionLocation].ImageSets[setInserted].ImageSet:
                                    if contents["Name"] == layers.name:
                                        layerInserted = l
                                        break
                                    l += 1
                            if layerInserted == -1 or setInserted == -1:
                                blankLayer.name = contents["Name"]
                                blankLayer.StartOn = int(contents["StartOn"])
                                blankLayer.AlwaysOn = int(contents["AlwaysOn"])
                                blankLayer.IsScene = int(contents["IsScene"])
                                blankLayer.TheBody = int(contents["TheBody"])
                                blankLayer.Overlay = contents["Overlay"]
                                blankLayer.setXalign = float(contents["setXalign"])
                                blankLayer.setYalign = float(contents["setYalign"])
                                try:
                                    blankLayer.player = contents["Player"]
                                except:
                                    blankLayer.player = "No"

                                blankPicture = Picture()
                                blankLayer.Images.append(copy.deepcopy(blankPicture))

                            for images in contents["Images"]:
                                blankPicture = Picture()
                                blankPicture.name = images["Name"]
                                blankPicture.file = images["File"]
                                blankPicture.setXalign = float(images["setXalign"])
                                blankPicture.setYalign = float(images["setYalign"])

                                if additionLocation != None and layerInserted != -1 and setInserted != -1:
                                    if loadingDatabaseType == 0:
                                        MonsterDatabase[additionLocation].ImageSets[setInserted].ImageSet[layerInserted].Images.append(copy.deepcopy(blankPicture))
                                else:
                                    blankLayer.Images.append(copy.deepcopy(blankPicture))

                            if additionLocation != None and layerInserted == -1 and setInserted != -1:
                                if loadingDatabaseType == 0:
                                    MonsterDatabase[additionLocation].ImageSets[setInserted].ImageSet.append(copy.deepcopy(blankLayer))
                            else:
                                tempSet.ImageSet.append(copy.deepcopy(blankLayer))

                            inSet += 1
                        else:
                            blankRole.name = contents["Role"]
                            blankRole.StanceReq = contents["StanceRequired"]
                            blankRole.MonsterReq = contents["MonsterRequired"]

                            for images in contents["CGTranslator"]:
                                blankCGTranslator = CGTranslator()
                                blankCGTranslator.In = str(images["In"])
                                blankCGTranslator.Out = str(images["Out"])
                                blankRole.Translators.append(copy.deepcopy(blankCGTranslator))

                            for images in contents["TogglesLayers"]:
                                blankRole.ToggledOnPartsWhenReqMet.append(str(images))

                            blankRole.NeedOne=contents["ActiveRequirment"]

                            blankRole.SpecificUIPlacementX = float(contents.get("SpecificUIPlacementX", 0.0))
                            blankRole.SpecificUIPlacementY = float(contents.get("SpecificUIPlacementY", 0.0))

                            tempSet.Roles.append(copy.deepcopy(blankRole))


                    if additionLocation != None and setInserted == -1:
                        if loadingDatabaseType == 0:
                            MonsterDatabase[additionLocation].ImageSets.append(copy.deepcopy(tempSet))
                    else:
                        FullSet.append(copy.deepcopy(tempSet))



                    if hasSets == 0:

                        break
            except:
                pass


            if additionLocation == None:
                if loadingDatabaseType == 0:
                    blankMonster = Monster(
                    NewMonStats,
                    int(currentData['moneyDropped']),
                    currentData["name"],
                    currentData["IDname"],
                    currentData["species"],
                    currentData["gender"],
                    currentData["description"],
                    currentData["encyclopedia"],
                    currentData["tags"],
                    NewMonSkillList,
                    [],
                    newLossScenes,
                    newVictoryScenes,
                    newDialogue,
                    NewMonBodySensitivity,
                    newDropList,
                    NewMonsStatusEffectsRes,
                    currentData["requires"],
                    requirementList,
                    currentData["generic"],
                    monFetishList,
                    FullSet)

                    for each in currentData["perks"]:
                        if each != "":
                            blankMonster.giveOrTakePerk(each, 1)


                    MonsterDatabase.append(copy.copy(blankMonster))    #add to list

                    if validateJsons and not loadingDatabaseType:
                        validator.addIDToDatabase(blankMonster.IDname, "Monsters")

    ############################### LOAD EVENTS ###############################
        for each in dynamic_loader(".*/Events/.*"):
            #print(each)
            try:
                with renpy.file(each) as file:
                    fileName = file.read().decode("utf-8")
            except IOError as e:
                if 'Json/Events/CombatEvents/AlrauneTestEvent.json' in str(e):
                    renpy.error("Save file is likely broken! There is no way to recover it. Try a different save, or start a new game.")
                else:
                    renpy.error(e)
            try:
                currentData = json.loads(fileName)
            except:
                PrintException(fileName)

            additionLocation = AdditionCheck(EventDatabase, "name")

            requirementList = []
            try:
                for each in currentData["requiresEvent"]:
                    newRequirement = Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    requirementList.append(copy.deepcopy(newRequirement))
            except:
                requirementList = [Requirements()]


            newSpeakerList = []
            for each in currentData["Speakers"]:
                blankSpeaker = theSpeaker()
                blankSpeaker.name = each["name"]
                blankSpeaker.postName = each["postName"]
                blankSpeaker.SpeakerType = each["SpeakerType"]

                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        EventDatabase[additionLocation].Speakers.append(blankSpeaker)
                else:
                    newSpeakerList.append(blankSpeaker)

            newDialogue = []
            for count in currentData["EventText"]:
                blankDia = Dialogue()
                try:
                    blankDia.NameOfScene = count["NameOfScene"]
                except:
                    PrintException(count["NameOfScene"])

                blankDia.theScene = count["theScene"]
                if validateJsons and not loadingDatabaseType:
                    if len(blankDia.theScene) > 0:
                        if blankDia.theScene[0] != "MenuAddition":
                            validator.checkEventText(currentData["name"], blankDia, fileName, jsonType="Events")
                    else:
                        validator.checkEventText(currentData["name"], blankDia, fileName, jsonType="Events")


                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        if blankDia.theScene[0] not in ["MenuAddition", "ShopAddition", "SkillShopAddition", "PrependScene", "AppendScene"]:
                            replaced = False
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene and replaced == False:
                                    EventDatabase[additionLocation].theEvents[replace] = blankDia
                                    replaced = True
                            if replaced == False:
                                EventDatabase[additionLocation].theEvents.append(blankDia)
                        elif blankDia.theScene[0] == "MenuAddition":
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene:
                                    start_index = checking.theScene.index("Menu")
                                    for offset_index in range(start_index + 1, len(checking.theScene)):
                                        if checking.theScene[offset_index] == "EndLoop":
                                            end_index = offset_index
                                            break
                                    EventDatabase[additionLocation].theEvents[replace].theScene = copy.copy(checking.theScene[:end_index] + blankDia.theScene[1:-1] + checking.theScene[end_index:])
                                    break
                        elif blankDia.theScene[0] == "ShopAddition":
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene:
                                    start_index = checking.theScene.index("ShoppingMenu")
                                    for offset_index in range(start_index + 1, len(checking.theScene)):
                                        if checking.theScene[offset_index] == "EndLoop":
                                            end_index = offset_index
                                            break
                                    EventDatabase[additionLocation].theEvents[replace].theScene = copy.copy(checking.theScene[:end_index] + blankDia.theScene[1:-1] + checking.theScene[end_index:])
                                    break
                        elif blankDia.theScene[0] == "SkillShopAddition":
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene:
                                    start_index = checking.theScene.index("SkillShoppingMenu")
                                    for offset_index in range(start_index + 1, len(checking.theScene)):
                                        if checking.theScene[offset_index] == "EndLoop":
                                            end_index = offset_index
                                            break
                                    EventDatabase[additionLocation].theEvents[replace].theScene = copy.copy(checking.theScene[:end_index] + blankDia.theScene[1:-1] + checking.theScene[end_index:])
                                    break
                        elif blankDia.theScene[0] == "PrependScene":
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene:
                                    EventDatabase[additionLocation].theEvents[replace].theScene = blankDia.theScene[1:] + checking.theScene
                                    break
                        elif blankDia.theScene[0] == "AppendScene":
                            for replace, checking in enumerate(EventDatabase[additionLocation].theEvents):
                                if checking.NameOfScene == blankDia.NameOfScene:
                                    EventDatabase[additionLocation].theEvents[replace].theScene = checking.theScene + blankDia.theScene[1:]
                                    break
                else:
                    newDialogue.append(blankDia)


            BaseTime = 0
            BaseLastChoice = ""
            BaseProgress = 0
            BaseChoices = []
            BaseComplete = 0
            if loadingDatabaseType == 1 and getFromName(currentData["name"], eventProgHolder) != -1:
                BaseTime = eventProgHolder[getFromName(currentData["name"], eventProgHolder)].timesSeen
                BaseLastChoice = eventProgHolder[getFromName(currentData["name"], eventProgHolder)].lastChoice
                BaseProgress = eventProgHolder[getFromName(currentData["name"], eventProgHolder)].eventProgress
                BaseChoices = eventProgHolder[getFromName(currentData["name"], eventProgHolder)].choices
                BaseComplete = eventProgHolder[getFromName(currentData["name"], eventProgHolder)].questComplete

                if currentData["name"] == "Toxic Matango Sign":
                    BaseComplete = 0


            if additionLocation == None:
                if loadingDatabaseType == 0:
                    blankEvent = Event(
                    currentData["name"],
                    currentData["Description"],
                    currentData["CardType"],
                    int(currentData["CardLimit"]),
                    newSpeakerList,
                    newDialogue,
                    BaseTime,
                    BaseLastChoice,
                    BaseProgress,
                    BaseChoices,
                    currentData["requires"],
                    requirementList,
                    BaseComplete)
                    EventDatabase.append(copy.copy(blankEvent))    #add to list

                    if validateJsons and not loadingDatabaseType:
                        validator.addIDToDatabase(blankEvent.name, "Events")

                if loadingDatabaseType == 1:
                    progEvent = Event(
                    currentData["name"],
                    "",
                    "",
                    0,
                    [],
                    [],
                    BaseTime,
                    BaseLastChoice,
                    BaseProgress,
                    BaseChoices,
                    [""],
                    [],
                    BaseComplete)
                    ProgressEvent.append(copy.copy(progEvent))

            if validateJsons and not loadingDatabaseType and "IgnoredDebugChoices" in currentData:
                if currentData["name"] not in validator.ignoredChoices:
                    validator.ignoredChoices[currentData["name"]] = {}
                for choice in currentData["IgnoredDebugChoices"]:
                    try:
                        choiceNumber, choiceValues = next(iter(choice.items()))
                        choiceNumber = str(choiceNumber)
                        validator.ignoredChoices[currentData["name"]][choiceNumber] = choiceValues
                    except:
                        validator.ignoredChoices[currentData["name"]][str(choice)] = []
        if loadingDatabaseType == 1:
            for each in eventProgHolder:
                if getFromName(each.name, ProgressEvent) == -1:

                    progEvent = Event(
                    each.name,
                    "",
                    "",
                    0,
                    [],
                    [],
                    each.timesSeen,
                    each.lastChoice,
                    each.eventProgress,
                    each.choices,
                    [""],
                    [],
                    each.questComplete)

                    ProgressEvent.append(progEvent)



    ############################### LOAD LOCATIONS ############################
        for each in dynamic_loader(".*/Locations/.*"):
            #print(each)
            with renpy.file(each) as file:
                fileName = file.read().decode("utf-8")
            try:
                currentData = json.loads(fileName)
            except:
                PrintException(fileName)
            newGroup = []
            miniGroup = []
            newTreasureList = []
            smolTreasureList = []
            erosDropList = []

            additionLocation = AdditionCheck(LocationDatabase, "name")

            MusicList = currentData.get("MusicList", [""])

            requirementList = []
            try:
                for each in currentData["requiresEvent"]:
                    newRequirement=Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    requirementList.append(copy.deepcopy(newRequirement))
            except:
                requirementList = [Requirements()]


            unlockList = []
            try:
                for each in currentData["FullyUnlockedByEvent"]:
                    newRequirement=Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    unlockList.append(copy.deepcopy(newRequirement))
            except:
                unlockList = [Requirements()]

            unlockExplore = currentData.get("ExplorationUnlockedBy", [""])

            unlockExploreList = []
            try:
                for each in currentData["ExplorationUnlockedByEvent"]:
                    newRequirement=Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    unlockExploreList.append(copy.deepcopy(newRequirement))
            except:
                unlockExploreList = [Requirements()]

            expNightmare = (int(currentData.get("Nightmare", 0)))

            blankGroup = []
            for countT in range(len(currentData["MonsterGroups"])):
                miniGroup = []
                for count in range(len(currentData["MonsterGroups"][countT]["Group"])):
                    if currentData["MonsterGroups"][countT]["Group"][count] != "":
                        miniGroup.append(currentData["MonsterGroups"][countT]["Group"][count])

                if additionLocation != None:
                    if len(miniGroup) > 0:
                        LocationDatabase[additionLocation].MonsterGroups.append(miniGroup)
                else:
                    blankGroup.append(miniGroup)


            smolTreasureList = []
            for count in range(len(currentData["Treasure"][0]["Common"])):
                if additionLocation != None:
                    if currentData["Treasure"][0]["Common"][count] != "":
                        LocationDatabase[additionLocation].Treasure[0].append(currentData["Treasure"][0]["Common"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][0]["Common"][count])
            if additionLocation == None:
                newTreasureList.append(smolTreasureList)

            smolTreasureList = []
            for count in range(len(currentData["Treasure"][1]["Uncommon"])):
                if additionLocation != None:
                    if currentData["Treasure"][1]["Uncommon"][count] != "":
                        LocationDatabase[additionLocation].Treasure[1].append(currentData["Treasure"][1]["Uncommon"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][1]["Uncommon"][count])
            if additionLocation == None:
                newTreasureList.append(smolTreasureList)

            smolTreasureList = []
            for count in range(len(currentData["Treasure"][2]["Rare"])):
                if additionLocation != None:
                    if currentData["Treasure"][2]["Rare"][count] != "":
                        LocationDatabase[additionLocation].Treasure[2].append(currentData["Treasure"][2]["Rare"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][2]["Rare"][count])
            if additionLocation == None:
                newTreasureList.append(smolTreasureList)

            if additionLocation == None:
                erosDropList.append(int(currentData["Eros"][0]["Common"]))
                erosDropList.append(int(currentData["Eros"][1]["Uncommon"]))
                erosDropList.append(int(currentData["Eros"][2]["Rare"]))


            if loadingDatabaseType == 0:
                if additionLocation != None:
                    for each in currentData["Monsters"]:
                        if each != "":
                            if each not in LocationDatabase[additionLocation].Monsters:
                                LocationDatabase[additionLocation].Monsters.append(each)
                    for each in currentData["Events"]:
                        if each != "":
                            if each not in LocationDatabase[additionLocation].Events:
                                LocationDatabase[additionLocation].Events.append(each)
                    for each in currentData["Quests"]:
                        if each != "":
                            if each not in LocationDatabase[additionLocation].Quests:
                                LocationDatabase[additionLocation].Quests.append(each)
                    for each in currentData["Adventures"]:
                        if each != "":
                            if each not in LocationDatabase[additionLocation].Adventures:
                                LocationDatabase[additionLocation].Adventures.append(each)

                else:
                    try:
                        blankLocation = Location(
                        currentData["name"],
                        currentData["exploreTitle"],
                        currentData["mapIcon"],
                        currentData["mapIconXpos"],
                        currentData["mapIconYpos"],
                        currentData["mapIconZorder"],
                        currentData["mapClouds"],
                        currentData["mapCloudsXpos"],
                        currentData["mapCloudsYpos"],
                        currentData["Monsters"],
                        blankGroup,
                        currentData["Events"],
                        currentData["Quests"],
                        currentData["Adventures"],
                        newTreasureList,
                        erosDropList,
                        int(currentData["MinimumDeckSize"]),
                        int(currentData["MaximumMonsterDeck"]),
                        int(currentData["MaximumEventDeck"]),
                        currentData["picture"],
                        currentData["requires"],
                        requirementList,
                        currentData["FullyUnlockedBy"],
                        unlockList,
                        MusicList,
                        unlockExplore,
                        unlockExploreList,
                        expNightmare )

                        LocationDatabase.append(blankLocation)    #add to list

                    # Messy as fuck but it works - handle JSON data that doesn't include map icons
                    except KeyError:
                        blankLocation = Location(
                        currentData["name"],
                        currentData["exploreTitle"],
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        currentData["Monsters"],
                        blankGroup,
                        currentData["Events"],
                        currentData["Quests"],
                        currentData["Adventures"],
                        newTreasureList,
                        erosDropList,
                        int(currentData["MinimumDeckSize"]),
                        int(currentData["MaximumMonsterDeck"]),
                        int(currentData["MaximumEventDeck"]),
                        currentData["picture"],
                        currentData["requires"],
                        requirementList,
                        currentData["FullyUnlockedBy"],
                        unlockList,
                        MusicList,
                        unlockExplore,
                        unlockExploreList,
                        expNightmare)

                        LocationDatabase.append(blankLocation)    #add to list

                    if validateJsons and not loadingDatabaseType:
                        validator.addIDToDatabase(blankLocation.name, "Locations")


    ############################## LOAD ADVENTURES ############################
        for each in dynamic_loader(".*/Adventures/.*"):
            #print(each)
            with renpy.file(each) as file:
                fileName = file.read().decode("utf-8")
            try:
                currentData = json.loads(fileName)
            except:
                PrintException(fileName)
            newGroup = []
            miniGroup = []
            newTreasureList = []
            smolTreasureList = []
            erosDropList = []

            additionLocation = AdditionCheck(AdventureDatabase, "name")

            requirementList = []
            try:
                for each in currentData["requiresEvent"]:
                    newRequirement=Requirements()
                    newRequirement.NameOfEvent = each["NameOfEvent"]
                    newRequirement.Progress = int(each["Progress"])
                    newRequirement.ChoiceNumber = int(each["ChoiceNumber"])
                    newRequirement.Choice = each["Choice"]

                    requirementList.append(copy.deepcopy(newRequirement))
            except:
                requirementList = [Requirements()]


            blankGroup = []
            for countT in range(len(currentData["MonsterGroups"])):
                miniGroup = []
                for count in range(len(currentData["MonsterGroups"][countT]["Group"])):
                    miniGroup.append(currentData["MonsterGroups"][countT]["Group"][count])

                if additionLocation != None:
                    if loadingDatabaseType == 0:
                        AdventureDatabase[additionLocation].monsterGroups.append(miniGroup)
                else:
                    blankGroup.append(miniGroup)

            MusicList = currentData.get("MusicList", [""])

            smolTreasureList = []
            for count in range(len(currentData["Treasure"][0]["Common"])):
                if additionLocation != None:
                    AdventureDatabase[additionLocation].Treasure[0].append(currentData["Treasure"][0]["Common"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][0]["Common"][count])
            if additionLocation == None:
                newTreasureList.append(smolTreasureList)
            smolTreasureList = []
            for count in range(len(currentData["Treasure"][1]["Uncommon"])):
                if additionLocation != None:
                    AdventureDatabase[additionLocation].Treasure[1].append(currentData["Treasure"][1]["Uncommon"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][1]["Uncommon"][count])
            if additionLocation == None:
                newTreasureList.append(smolTreasureList)
            smolTreasureList = []
            for count in range(len(currentData["Treasure"][2]["Rare"])):
                if additionLocation != None:
                    AdventureDatabase[additionLocation].Treasure[2].append(currentData["Treasure"][2]["Uncommon"][count])
                else:
                    smolTreasureList.append(currentData["Treasure"][2]["Rare"][count])

            if additionLocation == None:
                newTreasureList.append(smolTreasureList)

                erosDropList.append(int(currentData["Eros"][0]["Common"]))
                erosDropList.append(int(currentData["Eros"][1]["Uncommon"]))
                erosDropList.append(int(currentData["Eros"][2]["Rare"]))

            BaseComplete = 0
            if loadingDatabaseType == 1 and getFromName(currentData["name"], advenProgHolder) != -1:
                BaseComplete = advenProgHolder[getFromName(currentData["name"], advenProgHolder)].questComplete

            if additionLocation != None:
                if currentData["Deck"][0] != "":
                    AdventureDatabase[additionLocation].deck = currentData["Deck"]
                for countT in range(len(currentData["RandomEvents"])):
                    if currentData["RandomEvents"][countT] != "":
                        AdventureDatabase[additionLocation].randomEvents.append(currentData["RandomEvents"][countT])
                for countT in range(len(currentData["RandomMonsters"])):
                    if currentData["RandomMonsters"][countT] != "":
                        AdventureDatabase[additionLocation].randomMonsters.append(currentData["RandomMonsters"][countT])

            if additionLocation == None:
                if loadingDatabaseType == 0:
                    blankAdventure = AdventuringDeck(
                    currentData["name"],
                    currentData["Description"],
                    currentData["requires"],
                    requirementList,
                    currentData["Deck"],
                    currentData["RandomEvents"],
                    currentData["RandomMonsters"],
                    blankGroup,
                    newTreasureList,
                    erosDropList,
                    BaseComplete)
                    AdventureDatabase.append(blankAdventure)    #add to list

                    if validateJsons and not loadingDatabaseType:
                        validator.addIDToDatabase(blankAdventure.name, "Adventures")

                if loadingDatabaseType == 1:
                    progAdventure = AdventuringDeck(
                    currentData["name"],
                    "",
                    "",
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    BaseComplete)
                    ProgressAdventure.append(progAdventure)    #add to list



    ############################## LOAD EXTRA #################################
        if loadingDatabaseType == 1:
            for each in advenProgHolder:
                if getFromName(each.name, ProgressAdventure) == -1:

                    progAdventure = AdventuringDeck(
                    each.name,
                    "",
                    "",
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    each.questComplete)
                    ProgressAdventure.append(progAdventure)    #add to list



        if loadingDatabaseType == 0:
            for place in EventDatabase:
                if place.CardType == "Church" or  place.CardType == "Inn" or place.CardType == "Guild" or place.CardType == "Shopping" or place.CardType == "TownSquare":
                    LocationList.append(copy.deepcopy(place))

                if place.CardType == "WaiterShift" or  place.description == "WaiterShift":
                    WaiterBrothel.append(copy.deepcopy(place))
                if place.CardType == "BarShift" or  place.description == "BarShift":
                    BarBrothel.append(copy.deepcopy(place))
                if place.CardType == "GloryHoleShift" or  place.description == "GloryHoleShift":
                    GloryHoleBrothel.append(copy.deepcopy(place))

                if place.CardType == "DayShift" or  place.description == "DayShift":
                    DayBrothel.append(copy.deepcopy(place))

                if place.CardType == "EndOfDay":
                    EndOfDayList.append(copy.deepcopy(place))
                elif place.CardType == "TimePassed":
                    TimePassedList.append(copy.deepcopy(place))
                elif place.CardType == "StepTaken":
                    StepTakenList.append(copy.deepcopy(place))
                elif place.CardType == "Dream":
                    DreamList.append(copy.deepcopy(place))

                elif place.CardType == "EndOfTurn":
                    EndOfTurnList.append(copy.deepcopy(place))
                elif place.CardType == "PlayerOrgasm":
                    OnPlayerClimaxList.append(copy.deepcopy(place))
                elif place.CardType == "EndOfCombat":
                    EndOfCombatList.append(copy.deepcopy(place))
                elif place.CardType == "StartOfCombat":
                    StartOfCombatList.append(copy.deepcopy(place))
                elif place.CardType == "StartOfTurn":
                    StartOfTurnList.append(copy.deepcopy(place))

        if validateJsons and not loadingDatabaseType:
            for monster in MonsterDatabase:
                # TODO: Stances implementation to get combatDialogue with its mixed use of move.
                for each in monster.requiresEvent:
                    validator.validateIDname(each.NameOfEvent, monster.IDname, "Events", "Monsters", "requiresEvent", jsonType="Monsters")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in monster.requires:
                    validator.validateIDname(each, monster.IDname, "Items", "Monsters", "requires", jsonType="Monsters")
                for each in monster.lossScenes:
                    validator.validateIDname(each.move, monster.IDname, "Skills", "Monsters", "lossScenes(move)", ["None", "Unavalible", "theScene", "OnlyJumpedTo"], jsonType="Monsters")
                    for includes in each.includes:
                        validator.validateIDname(includes, monster.IDname, "Monsters", "Monsters", "lossScenes(includes)", ["None", "OnlyJumpedTo"], jsonType="Monsters")
                for each in monster.victoryScenes:
                    validator.validateIDname(each.move, monster.IDname, "Skills", "Monsters", "victoryScenes(move)", ["None", "Unavalible", "theScene", "OnlyJumpedTo"], jsonType="Monsters")
                    for includes in each.includes:
                        validator.validateIDname(includes, monster.IDname, "Monsters", "Monsters", "victoryScenes(includes)", ["None", "OnlyJumpedTo"], jsonType="Monsters")
            for item in ItemDatabase:
                for each in item.requiresEvent:
                    validator.validateIDname(each.NameOfEvent, item.name, "Events", "Items", "requiresEvent", jsonType="Items")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in item.requires:
                    validator.validateIDname(each, item.name, "Items", "Items", "requires", jsonType="Items")

                for each in item.perks:
                    validator.validateIDname(each, item.name, "Perks", "Items", "perks", jsonType="Items")
                for each in item.skills:
                    validator.validateIDname(each, item.name, "Skills", "Items", "skills", jsonType="Items")
            for skill in SkillsDatabase:
                for each in skill.requiresPerk:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "requiresPerk", jsonType="Skills")
                for each in skill.requiresOnePerk:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "requiresOnePerk", jsonType="Skills")
                for each in skill.unusableIfPerk:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "unusableIfPerk", jsonType="Skills")
                for each in skill.requiresPerkSelf:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "requiresPerkSelf", jsonType="Skills")
                for each in skill.requiresOnePerkSelf:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "requiresOnePerkSelf", jsonType="Skills")
                for each in skill.unusableIfPerkSelf:
                    validator.validateIDname(each, skill.name, "Perks", "Skills", "unusableIfPerkSelf", jsonType="Skills")


                for each in skill.fetishTags:
                    validator.validateIDname(each, skill.name, "Fetishes", "Skills", "fetishTags", ["Foreplay", "Penetration", "Seduction", "Sex Toy", "Indulgent"], jsonType="Fetishes")
                # for each in skill.requiresEvent:
                #     validator.validateIDname(each.NameOfEvent, skill.name, "Events", "Skills", "requiresEvent", , jsonType="Fetishes")
            for event in EventDatabase:
                for each in event.Speakers:
                    if each.SpeakerType != "?":
                        validator.validateIDname(each.name, event.name, "Monsters", "Events", "Speakers", ["???", "??? 1", "??? 2", "??? 3", "??? 4", "??? 5", "??? 6", "??? 7", "??? 8", "??? 9", "??? 10", "??? 11", "??? 12", "character", "Venereae"], jsonType="Events")

                for each in event.requiresEvent:
                    validator.validateIDname(each.NameOfEvent, event.name, "Events", "Events", "requiresEvent", jsonType="Events")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in event.requires:
                    validator.validateIDname(each, event.name, "Items", "Events", "requires", jsonType="Events")
            for perk in PerkDatabase:
                for each in perk.PerkReq:
                    validator.validateIDname(each, perk.name, "Perks", "Perks", "PerkReq", jsonType="Perks")
                # for each in perk.requiresEvent:
                #     validator.validateIDname(each.NameOfEvent, perk.name, "Events", "Perks", "requiresEvent", jsonType="Perks")
            for adventure in AdventureDatabase:
                # TODO: Decks.
                for each in adventure.randomEvents:
                    validator.validateIDname(each, adventure.name, "Events", "Adventures", "RandomEvents", jsonType="Adventures")

                for each in adventure.monsterGroups:
                    for monster in each:
                        validator.validateIDname(monster, adventure.name, "Monsters", "Adventures", "MonsterGroups", jsonType="Adventures")
                for each in adventure.randomMonsters:
                    validator.validateIDname(each, adventure.name, "Monsters", "Adventures", "RandomMonsters", jsonType="Adventures")

                for index, each in enumerate(adventure.Treasure):
                    if index == 0:
                        for treasure in each:
                            validator.validateIDname(treasure, adventure.name, "Items", "Adventures", "Treasure(Common)", jsonType="Adventures")
                    if index == 1:
                        for treasure in each:
                            validator.validateIDname(treasure, adventure.name, "Items", "Adventures", "Treasure(Uncommon)", jsonType="Adventures")
                    if index == 2:
                        for treasure in each:
                            validator.validateIDname(treasure, adventure.name, "Items", "Adventures", "Treasure(Rare)", jsonType="Adventures")


                for each in adventure.requiresEvent:
                    validator.validateIDname(each.NameOfEvent, adventure.name, "Events", "Adventures", "requiresEvent", jsonType="Adventures")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in adventure.requires:
                    validator.validateIDname(each, adventure.name, "Items", "Adventures", "requires", jsonType="Adventures")

            for location in LocationDatabase:
                for each in location.ExplorationUnlockedByEvent:
                    validator.validateIDname(each.NameOfEvent, location.name, "Events", "Locations", "ExplorationUnlockedByEvent", jsonType="Locations")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in location.ExplorationUnlockedBy:
                    validator.validateIDname(each, location.name, "Items", "Locations", "ExplorationUnlockedBy", ["CantBeUnlocked"], jsonType="Locations")

                for each in location.FullyUnlockedByEvent:
                    validator.validateIDname(each.NameOfEvent, location.name, "Events", "Locations", "FullyUnlockedByEvent", jsonType="Locations")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in location.FullyUnlockedBy:
                    validator.validateIDname(each, location.name, "Items", "Locations", "FullyUnlockedBy", ["CantBeUnlocked"], jsonType="Locations")

                for each in location.requiresEvent:
                    validator.validateIDname(each.NameOfEvent, location.name, "Events", "Locations", "requiresEvent", jsonType="Locations")
                    validator.addChoiceSource(each.NameOfEvent, str(each.ChoiceNumber), each.Choice)
                for each in location.requires:
                    validator.validateIDname(each, location.name, "Items", "Locations", "requires", ["CantBeUnlocked"], jsonType="Locations")


                for index, each in enumerate(location.Treasure):
                    if index == 0:
                        for treasure in each:
                            validator.validateIDname(treasure, location.name, "Items", "Locations", "Treasure(Common)", jsonType="Locations")
                    if index == 1:
                        for treasure in each:
                            validator.validateIDname(treasure, location.name, "Items", "Locations", "Treasure(Uncommon)", jsonType="Locations")
                    if index == 2:
                        for treasure in each:
                            validator.validateIDname(treasure, location.name, "Items", "Locations", "Treasure(Rare)", jsonType="Locations")

                for each in location.MonsterGroups:
                    for monster in each:
                        validator.validateIDname(monster, location.name, "Monsters", "Locations", "MonsterGroups", jsonType="Locations")
                for each in location.Monsters:
                    validator.validateIDname(each, location.name, "Monsters", "Locations", "Monsters", jsonType="Locations")

                for each in location.Monsters:
                    validator.validateIDname(each, location.name, "Monsters", "Locations", "Monsters", jsonType="Locations")

                for each in location.Events:
                    validator.validateIDname(each, location.name, "Events", "Locations", "Events", jsonType="Locations")
                for each in location.Quests:
                    validator.validateIDname(each, location.name, "Events", "Locations", "Quests", jsonType="Locations")


    ############################ UPDATE SAVED PLAYER ##########################
        if loadingDatabaseType == 1:

            player.setNewPlayerVariables(Monster(Stats()))

            i = 0
            while  i < len(player.skillList):

                player.skillList[i].updateSkill()

                if player.skillList[i].name == "Glamour":
                    player.inventory.money += 500
                    del player.skillList[i]
                    i-=1
                if player.skillList[i].name == "Invigorate":
                    player.inventory.money += 500
                    del player.skillList[i]
                    i-=1

                try:
                    player.skillList[i].critChance
                except:
                    player.skillList[i].critChance = 0
                try:
                    player.skillList[i].critDamage
                except:
                    player.skillList[i].critDamage = 0
                try:
                    player.skillList[i].accuracy
                except:
                    player.skillList[i].accuracy = 0
                try:
                    player.skillList[i].initiative
                except:
                    player.skillList[i].initiative = 0
                try:
                    player.skillList[i].unusableIfStatusPotency
                except:
                    player.skillList[i].unusableIfStatusPotency = [0]
                if isinstance(player.skillList[i].unusableIfStatusPotency, (int)):
                    player.skillList[i].unusableIfStatusPotency = [player.skillList[i].unusableIfStatusPotency]
                try:
                    player.skillList[i].requiresStatusEffectSelf
                except:
                    player.skillList[i].requiresStatusEffectSelf = ""
                try:
                    player.skillList[i].requiresStatusPotencySelf
                except:
                    player.skillList[i].requiresStatusPotencySelf = 0
                try:
                    player.skillList[i].unusableIfStatusEffectSelf
                except:
                    player.skillList[i].unusableIfStatusEffectSelf = ["None"]
                try:
                    player.skillList[i].requiresPerk
                except:
                    player.skillList[i].requiresPerk = []
                try:
                    player.skillList[i].requiresOnePerk
                except:
                    player.skillList[i].requiresOnePerk = []
                try:
                    player.skillList[i].unusableIfPerk
                except:
                    player.skillList[i].unusableIfPerk = []
                try:
                    player.skillList[i].requiresPerkSelf
                except:
                    player.skillList[i].requiresPerkSelf = []
                try:
                    player.skillList[i].requiresOnePerkSelf
                except:
                    player.skillList[i].requiresOnePerkSelf = []
                try:
                    player.skillList[i].unusableIfPerkSelf
                except:
                    player.skillList[i].unusableIfPerkSelf = []

                try:
                    player.skillList[i].unusableIfTargetHasTheseSets = player.skillList[i].unusableIfTargetHasTheseSets
                except:
                    player.skillList[i].unusableIfTargetHasTheseSets = []

                if isinstance(player.skillList[i].restraintStruggle, (str, unicode)):
                    player.skillList[i].restraintStruggle = [player.skillList[i].restraintStruggle]

                if isinstance(player.skillList[i].restraintStruggleCharmed, (str, unicode)):
                    player.skillList[i].restraintStruggleCharmed = [player.skillList[i].restraintStruggleCharmed]

                if isinstance(player.skillList[i].restraintEscaped, (str, unicode)):
                    player.skillList[i].restraintEscaped = [player.skillList[i].restraintEscaped]

                if isinstance(player.skillList[i].restraintEscapedFail, (str, unicode)):
                    player.skillList[i].restraintEscapedFail = [player.skillList[i].restraintEscapedFail]

                try:
                    if isinstance(player.skillList[i].restraintOnLoss, (str, unicode)):
                        player.skillList[i].restraintOnLoss = [player.skillList[i].restraintOnLoss]
                except:
                    player.skillList[i].restraintOnLoss = [""]

                if isinstance(player.skillList[i].startsStance, (str, unicode)):
                    player.skillList[i].startsStance = [player.skillList[i].startsStance]

                if isinstance(player.skillList[i].removesStance, (str, unicode)):
                    player.skillList[i].removesStance = [player.skillList[i].removesStance]


                i+=1

            i = 0
            for eachNew in player.skillList:

                for each in SkillsDatabase:
                    if each.name == eachNew.name:
                        player.skillList[i] = copy.deepcopy(each)

                        try:
                            eachNew.statusStacks = eachNew.statusStacks
                        except:
                            eachNew.statusStacks = 0

                        try:
                            eachNew.scalesWithStatusScale = eachNew.scalesWithStatusScale
                        except:
                            eachNew.scalesWithStatusScale = ""                            
                        try:
                            eachNew.scalesWithStatusEffect = eachNew.scalesWithStatusEffect
                        except:
                            eachNew.scalesWithStatusEffect = ""
                        try:
                            eachNew.flatSFFlatScaling = eachNew.flatSFFlatScaling
                        except:
                            eachNew.flatSFFlatScaling = 0
                        try:
                            eachNew.flatSFPercentScaling = eachNew.flatSFPercentScaling
                        except:
                            eachNew.flatSFPercentScaling = 0
                        try:
                            eachNew.totalSFPercentScaling = eachNew.totalSFPercentScaling
                        except:
                            eachNew.totalSFPercentScaling = 0

                i+=1


            i = 0
            while  i < len(player.inventory.items):
                try:
                    player.inventory.items[i].Int
                except:
                    setattr(player.inventory.items[i], 'Int', 0)

                try:
                    player.inventory.items[i].skills
                except:
                    setattr(player.inventory.items[i], 'skills', [])

                try:
                    player.inventory.items[i].onEquip
                except:
                    setattr(player.inventory.items[i], 'onEquip', "")

                try:
                    player.inventory.items[i].onUnequip
                except:
                    setattr(player.inventory.items[i], 'onUnequip', "")

                try:
                    player.inventory.items[i].tags
                except:
                    setattr(player.inventory.items[i], 'tags', [])

                i += 1



            for eachNew in ItemDatabase:
                i = 0
                for each in player.inventory.items:
                    amount = copy.deepcopy(each.NumberHeld)

                    if player.inventory.RuneSlotOne.name == eachNew.name:
                        player.inventory.equip(1, player, -1)
                        player.inventory.RuneSlotOne = copy.deepcopy(eachNew)
                        player.inventory.equip(1, player, 1)
                    if player.inventory.RuneSlotTwo.name == eachNew.name:
                        player.inventory.equip(2, player, -1)
                        player.inventory.RuneSlotTwo = copy.deepcopy(eachNew)
                        player.inventory.equip(2, player, 1)
                    if player.inventory.RuneSlotThree.name == eachNew.name:
                        player.inventory.equip(3, player, -1)
                        player.inventory.RuneSlotThree = copy.deepcopy(eachNew)
                        player.inventory.equip(3, player, 1)
                    if player.inventory.AccessorySlot.name == eachNew.name:
                        player.inventory.equip(4, player, -1)
                        player.inventory.AccessorySlot = copy.deepcopy(eachNew)
                        player.inventory.equip(4, player, 1)

                    if each.name == eachNew.name:
                        player.inventory.items[i] = copy.deepcopy(eachNew)
                        player.inventory.items[i].NumberHeld = amount

                    requirementList = []
                    try:
                        player.inventory.items[i].requiresEvent
                    except:
                        player.inventory.items[i].requiresEvent = [Requirements()]
                    i+=1
                
                #CODEMOD:Rebuild player stash items
                if type(player.inventory) is StashInventory:
                    for i, each in enumerate(player.inventory.stash):

                        if each.name == eachNew.name:
                            amount = copy.deepcopy(each.NumberHeld)

                            player.inventory.stash[i] = copy.deepcopy(eachNew)
                            player.inventory.stash[i].NumberHeld = amount

            #Update inventory with updated consumable limits
            if type(player.inventory) is StashInventory and player.inventory.stashActive:
                for item in player.inventory.items:
                    player.inventory.limitItemCount(item)


            i = 0

            for eachNew in player.perks:
                if eachNew.name == "Caressing Dynamo":
                    player.giveOrTakePerk(each.name, -1)
                    player.giveOrTakePerk("Seductive Dynamo", 1)
                player.perks[i].Update()
                i +=1

            for each in PerkDatabase:
                for eachNew in player.perks:


                    if each.name == eachNew.name:

                        holdDruation = -1
                        try:
                            holdDruation = copy.deepcopy(eachNew.duration)
                        except:
                            holdDruation = -1
                        player.giveOrTakePerk(eachNew.name, -1)
                        player.giveOrTakePerk(eachNew.name, 1, holdDruation)

            for perk in player.perks:
                for p in range(len(perk.PerkType)):
                    if perk.PerkType[p] == "TimeDuration" or perk.PerkType[p] ==  "TurnDuration":
                        if perk.duration <= -1:
                            perk.duration = copy.deepcopy(PerkDatabase[ getFromName(perk.name, PerkDatabase)].duration)

            player.stats.BarMinMax()



            ###############################FETISH LIST###############################
            FetishList = []
            for each in dynamic_loader(".*/Fetishes/.*"):
                #print(each)
                with renpy.file(each) as file:
                    fileName = file.read().decode("utf-8")
                try:
                    currentData = json.loads(fileName)
                except:
                    PrintException(fileName)

                for FL in currentData['FetishList']:
                    newFetish = Fetish()

                    newFetish.name = FL["Name"]
                    newFetish.Level = int(FL["BaseLevel"])
                    newFetish.Type = FL["Type"]
                    newFetish.CreationOn = FL["CreationOn"]
                    newFetish.CreationOff = FL["CreationOff"]
                    try:
                        newFetish.toolTip = FL["ToolTip"]
                    except:
                        newFetish.toolTip = ""

                    try:
                        newFetish.levelText = []
                        for fet in FL["LevelText"]:
                            miniFetish = []
                            miniFetish.append(int(fet[0]))
                            miniFetish.append(fet[1])
                            newFetish.levelText.append(miniFetish)
                    except:
                        newFetish.levelText = []
                    FetishList.append(newFetish)


            tempFetishList = copy.deepcopy(player.FetishList)
            player.FetishList = FetishList
            i = 0
            for each in player.FetishList:
                for eachNew in tempFetishList:
                    if hasattr(eachNew, 'Name'):
                        if each.name == eachNew.Name:
                            player.FetishList[i].Level = eachNew.Level
                    else:
                        if each.name == eachNew.name:
                            player.FetishList[i].Level = eachNew.Level
                i+=1
        if renpy.windows or renpy.linux:
            if validateJsons and not loadingDatabaseType:
                persistent.validatorAtReload = False
                validator.writeToFiles()
        if not renpy.android and not renpy.emscripten:
            if countModList(genericCount=True) > 0:
                persistent.modsArePresent = True
            else:
                persistent.modsArePresent = False
        validator = None
        file = None
        fileName = None
        blankPicture = None
        blankScene = None
        blankSpeaker = None
        blankGroup = None
        needToUpdate = 0
        # benchtime = time.perf_counter()
        # print("Section Name Here:", benchtime - benchstart)
    if persistent.genModData == True:
            $ persistent.genModData = False
            $ loadingDatabaseType = 1
            # if persistent.modCount == None:
            #     $ persistent.modCount = 0
            # if persistent.modCount != 0:
            #     $ renpy.notify("[persistent.modCount] Mods loaded.")
            jump exitCombatFunction
