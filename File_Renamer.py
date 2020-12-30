import os
from collections import defaultdict

#TEMP: Remove afterward
os.chdir(r"C:\Users\Bruno\Dropbox\ImageProcessing_Bruno")

def getDirs(path):
    
    directories = [name for name in os.listdir(currentPath) if os.path.isdir(name)]

    global visitedDirs
    if len(visitedDirs) > 0:
        tempDirectories = [item for item in directories not in visitedDirs]
        directories = tempDirectories
    
    dirCount = len(directories)
    if dirCount>1:
        print("Multiple directories found, Select Working Directory:")
        for i in range(dirCount):
            print(f"{i+1}. {directories[i]}")
            currentDir = int(input())

            
            visitedDirs.append(directories[currentDir-1])

            os.chdir(directories[currentDir-1])
            currentDir = os.getcwd()

    elif dirCount == 1:   
        if (currentDir := input(f"The directory found is \"{directories[0]}\" is this the desired directory? [Y/N].\nIf this is not the desired directory, insert the path for the new directory or move this module to that location: \n")) not in ["Y",'y']:
            currentDir = currentDir.lstrip("N ")
            try:
                os.chdir(currentDir)
            except FileNotFoundError:
                currentDir = input("The inserted path is not valid, please verify it and insert the correct path:\n")
                os.chdir(currentDir)
        else:
            os.chdir(directories[0])
            currentDir = os.getcwd()

            visitedDirs.append(directories[0])
    else:
        print("No direcories left to rename.")
        return ([],-1,"")

    return (directories,dirCount,currentDir)

def getInfoFromFolders(filePath,separator = "_",infoTemplate=[],mode = "Retrieve Info",extraParams = None):
    
    infoList = []
    separator = separator
    infoTemplate = infoTemplate
    fileExtension = ""

    def splitString(string, separator = "_", extraParams = None):
        separator = separator
        topDir = currentDir.split("\\")[-1]
        topDirPos = filePath.find(topDir)

        folderInfoString = filePath[topDirPos:]

        tempList = folderInfoString.split("\\")
        fileName = tempList[-1]
        fileExtension = "." + fileName.split(".")[-1]

        folderInfoList = tempList[:-1]

        global currentDirectoryDepth
        if fileCounter == 0:
            currentDirectoryDepth = len(folderInfoList)
        
        newLength = len(folderInfoList)

        if newLength > currentDirectoryDepth:
            print( 3*"\n" + f"{newLength-currentDirectoryDepth} new tag(s) were found!\n")
            newUsefulInfo = folderInfoList[currentDirectoryDepth:]

            nonlocal infoTemplate
            if separatorFlag:
                infoTemplate = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template",extraParams=("Update Template",newUsefulInfo,"Use Separator"))[1]
            else:
                infoTemplate = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template",extraParams=("Update Template",newUsefulInfo))[1]

            currentDirectoryDepth = newLength

        if extraParams != None and "Use Separator" in extraParams:
            tempSplitString = []
            for item in folderInfoList:
                if separator in item:
                    for tag in item.split(separator):
                        tempSplitString.append(tag)
                else:
                    tempSplitString.append(item)

            splitString = tempSplitString
        
        else:
            splitString = folderInfoList
        
        return splitString,fileName,fileExtension   

    global usefulInfoPosDict
    if mode == "Make Template":

        if extraParams != None and "Update Template" in extraParams:
            usefulInfoList = extraParams[1]
        else:
            if separatorFlag:
                usefulInfoList = splitString(filePath,separator,extraParams="Use Separator")[0]
            else:
                usefulInfoList = splitString(filePath)[0]
            print(3*"\n"+"These are an example the following tags found in the folder names.\nYou will be asked to name them for convenience, then choose the tags wou wish to keep in the file name.\nIf any new tags are found you will be prompted if you wish to add them to the naming convention.\nWARNING: Consider what the tag represents rather than the actual tag when deciding the namimg convention. This prompt will show up only once.")
            
        for tag in usefulInfoList:
            tagName = input(f"What does the tag \"{tag}\" represent?\n")
            
            usefulInfoPosDict[tagName] = usefulInfoList.index(tag)
        
        if infoTemplate == []:
            correctSelection = "N"
            tempDict = {}
            while correctSelection not in ["Y","y"]:
                print(3*"\n"+"These are the tags you named earlier:")
                for i, item in enumerate(usefulInfoPosDict.keys()):
                    print(f"{i}. {item}")
                    tempDict[i] = item

                infoTemplateString = input("Using the numbers, choose which,\nand in what order the information should be coppied to the file name separated by spaces (unused numbers will be ignored):\n")
                
                infoTemplateString = infoTemplateString.replace(".","").strip(" ")

                tempList2 = []
                print("Your selection was:")
                for i in infoTemplateString.split(" "):
                    print(tempDict[int(i)],end="_")
                    tempList2.append(tempDict[int(i)])
                    
                correctSelection = input("\nIs this correct?[Y/N]\n")

            infoTemplate = tempList2

            usefulInfoPosDict = {(value if value in tempList2 else value+" (Unused)"):key for (key,value) in tempDict.items()}

        else:
            changePattern = input("New Tags were added since last selection, do you wish to update naming pattern? [Y/N]\n")
            
            if changePattern in ["Y","y"]:
                correctSelection = ""
                tempDict = {}
                while correctSelection not in ["Y","y"]:
                    print(3*"\n"+"This is the updated list of tags:")
                    for i, item in enumerate(usefulInfoPosDict.keys()):
                        print(f"{i}. {item}")
                        tempDict[i] = item

                    infoTemplateString = input("Using the numbers, choose which, and in what order the information should be coppied to the file name separated by spaces (unused numbers will be ignored):\n\n")

                    tempList2 = []
                    print("Your selection was:")
                    for i in infoTemplateString.split(" "):
                        print(tempDict[int(i)],end="_")
                        tempList2.append(tempDict[int(i)])
                        
                    correctSelection = input("Is this correct?[Y/N]\n")

                infoTemplate = tempList2

                #FIXME: Whatever mess is happeing with the adding of new tags into the dictionary/infotemplate exception, see previous implementation.

                for i in tempDict.values():
                    if i not in tempList2:
                        if "(Unused)" not in usefulInfoPosDict[i]:
                            usefulInfoPosDict[i] = usefulInfoPosDict[i] + " (Unused)"
                    elif i in tempList2 and ("(Unused)" in usefulInfoPosDict[i]):
                        usefulInfoPosDict[i] = usefulInfoPosDict[i].replace(" (Unused)","")
            else:
                print("Ignoring new entries.")

    elif mode == "Get Info":
        if separatorFlag:
            allInfoList,_fileName,fileExtension = splitString(filePath,separator,extraParams="Use Separator")
        else:
            allInfoList,_fileName,fileExtension = splitString(filePath,separator)
        for item in infoTemplate:
            try:
                infoPos = usefulInfoPosDict[item]
                infoList.append(allInfoList[infoPos])

            except IndexError:
                infoList.append("")

    
    return (infoList, infoTemplate,fileExtension)

def renameFile(filePath,infoList=[],fileExtension="",separator = "_", failCounter = 0):
    failCounter = failCounter
    actualName = separator.join(infoList)
    if failCounter == 0:
        actualPath = filePath.split("\\")[:-1]
        actualPath = (os.sep).join(actualPath) + os.sep + actualName + fileExtension
    else:
        actualPath = (os.sep).join((filePath.split("\\")[:-1])) + os.sep + actualName + f"({str(failCounter)})" + fileExtension

    try:
        os.rename(filePath,actualPath)
    except FileExistsError:
        failCounter +=1
        renameFile(filePath,infoList,fileExtension,separator,failCounter)
    
def main():
    global currentPath 
    currentPath = os.path.abspath(os.getcwd())

    global directories,dirCount,currentDir
    directories,dirCount,currentDir = getDirs(currentPath)
    separator = "_"
    fileExtension = input("What is the file extension of the file(s) you are trying to rename?\n")
    if "." not in fileExtension:
        fileExtension = "."+fileExtension
    
    separatorPrompt = input("Are you using separators to store information in the folder names?[Y/N]\nIf yes, please indicate it: (Optional)") 
    if separatorPrompt != "N":
        separator = separatorPrompt.replace("Y ","").replace("y ","")
        global separatorFlag
        separatorFlag = True
        

    for root, _dirs, files in os.walk(currentDir,topdown=True,followlinks=False):
        for name in files:
            if name.endswith(fileExtension):
                filePathString = root + os.sep +name
                global fileCounter,infoTemplate
                if fileCounter == 0:                    
                    infoTemplate = getInfoFromFolders(filePath=filePathString,separator=separator,mode="Make Template")[1]
                    infoList,_infoTemplate,fileExtension = getInfoFromFolders(filePathString, separator=separator, infoTemplate = infoTemplate, mode="Get Info")
                    renameFile(filePathString,infoList,fileExtension,separator)

                else:
                    infoList,_infoTemplate,fileExtension = getInfoFromFolders(filePathString, separator=separator, infoTemplate = infoTemplate, mode="Get Info")
                    renameFile(filePathString,infoList,fileExtension,separator)


                fileCounter += 1 

exitFlag = False
directories,visitedDirs,dirCount,currentDir,currentPath = [],[],0,"",""
infoTemplate = []
usefulInfoPosDict = defaultdict(dict)
fileCounter,currentDirectoryDepth = 0,0
separatorFlag = False



while dirCount >= 0 or exitFlag == True:
    try:
        main()
    except Exception as exp:
        print(exp)

    if continueFlag := input(f"There are still {dirCount} directories remaining, do you wish to continue?[Y/N]:\n") not in ["Y","y"]:
        exitFlag = False