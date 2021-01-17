#Module importing:

import os   

#Function declaration:

def getDirs(path):
    '''
    Finds the directories in the same folder and selects the current working directory from user input.

    Given the path of the current working directory, this function will seek all avaliable directories
    in that path if they have not been visited yet. Then based on user selection, it will change the 
    current working directory to match that selection.

    Parameters:
        - path: (str) path that the module is in.
    
    Returns:
        - dirCount: (int) How many directories are in the folder that the module is in (does not include visited directories).
        - currentDir: (str) The string that contains the path to the current working directory. 

    '''
    directories = [name for name in os.listdir(path) if os.path.isdir(name)] #Lists all directories in path

    #Handles multiple runs of main(), updates the directories list if the program has already visited a given folder
    global visitedDirs
    if len(visitedDirs) > 0:
        tempDirectories = [item for item in directories not in visitedDirs]
        directories = tempDirectories
    
    #This block serves as a control for the user to select the working directory depending on the number of directories
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
        return (0,"")

    return (dirCount,currentDir)

def getInfoFromFolders(filePath, separator = "_", infoTemplate=[], mode = "Retrieve Info", usefulInfoPosDict = {}, extraParams = None):
    '''
    Function responsble for creating the template for the naming convention, and retrieving the information from the folders.

    This function behaves differently depending on the mode paramete. If the mode is set to "Make template", it will take the
    filePath, and call splitString() to get the "tags" used in renaming the files, it will then prompt the user to name them
    and decide which ones will be used on the file template. If the mode is set to "Retrieve Info", given the infoTemplate it
    will return the string that will be the name of the file by calling splitString() and joining the necessary tags.

    Parameters:
        - filePath: (str) Contains the path to the file to be renamed.
        - separator: (str) Contains the separator that the user is using, if any.(Default: "_")
        - infoTemplate: (list) Contains the names of the tags used in file renaming. Empty on the first calling, but populated afterward.(Default: [])
        - mode: (str) Mode that the function will run as. (Default: "Retrieve Info")
        - usefulInfoPosDict: (dict) Dictionary containing the position in the splited file path for the given tag.(Default = {})
        - extraParams: (tuple) Additional parameters that the fucntion can use depending on the situation.(Default: None)

    Returns:
        - infoList: (list) Filtered and ordered list of information used in renaming the file, based on filePath and infoTemplate.
        - infoTemplate: (list) Contains the names of the tags used in file renaming. Empty on the first calling, but populated afterward.
        - fileExtension: (str) File extension of the given file.
        - usefulInfoPosDict: (dict) Dictionary containing the position in the splited file path for the given tag.

    '''

    #Local Variable setup:

    infoList = []
    separator = separator
    infoTemplate = infoTemplate
    fileExtension = ""
    usefulInfoPosDict = usefulInfoPosDict

    #Nested Function Declaration:

    def splitString(string, separator = "_", extraParams = None):
        '''
        Given the file path, this function will return a list of information obtained from splitting the path using the sparator if provided.

        This function will take the file path from "string", and if extraParams is set to "Use Separator", it will take the separator from
        "separator" if any is provided and return information obtained from splitting the file path using the system separator and the
        separator. Otherwise, it will just split the file path using the system separator.

        Parameters:
            - string: (str) String that is to be splitted by the function, usually a file path.
            - separator: (str) Separator to be used in splitting the string.(Default: "_")
            - extraParams: (str) Additional parameters that the fucntion can use depending on the situation.(Default: None)
        
        Returns:
            - splitString: (list) List that contains all of the items obtained from spliting the file path with the system separator and separator.
            - fileName: (str) Name of the current file, does not include the extension.
            - fileExtension: (str) Extension of the current file.
            - usefulInfoPosDict: (dict) Dictionary containing the position in the splited file path for the given tag.

        '''
        separator = separator
        topDir = currentDir.split(os.sep)[-1]
        topDirPos = filePath.find(topDir)

        folderInfoString = filePath[topDirPos:]

        tempList = folderInfoString.split(os.sep)
        fileName = tempList[-1]
        fileExtension = "." + fileName.split(".")[-1]

        folderInfoList = tempList[:-1] + [tempList[-1].replace(fileExtension,"")]

        global currentDirectoryDepth
        if fileCounter == 0:
            currentDirectoryDepth = len(folderInfoList)
        
        newLength = len(folderInfoList)

        if newLength > currentDirectoryDepth:
            print( 3*"\n" + f"{newLength-currentDirectoryDepth} new tag(s) were found!\n")
            newUsefulInfo = (folderInfoList,folderInfoList[:currentDirectoryDepth] )

            nonlocal infoTemplate
            if separatorFlag:
                _infoList, infoTemplate,_fileExtension, usefulInfoPosDict = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template", usefulInfoPosDict= usefulInfoPosDict, extraParams=("Update Template",newUsefulInfo,"Use Separator"))
            else:
               _infoList, infoTemplate, _fileExtension, usefulInfoPosDict = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template", usefulInfoPosDict= usefulInfoPosDict, extraParams=("Update Template",newUsefulInfo))

            currentDirectoryDepth = newLength

        if extraParams != None and ("Use Separator" in extraParams) :
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
        
        return (splitString,fileName,fileExtension,usefulInfoPosDict)   

    #Function Body:
    
    if mode == "Make Template": #Proceeds if mode is set to "Make Template".
        usefulInfoPosDict = {}

        previousInfoList = []
        
        if extraParams != None and "Update Template" in extraParams: #Runs only if extraParams is set to "Update Template." Branch only runs if called from within splitString().
            #Updates usefulInfoList
            usefulInfoList = extraParams[1]
            previousInfoList = usefulInfoPosDict.keys()
        else:
            if separatorFlag:
                usefulInfoList, _fileName, _fileExtension, usefulInfoPosDict = splitString(filePath,separator,extraParams="Use Separator")
            else:
                usefulInfoList, _fileName, _fileExtension, usefulInfoPosDict = splitString(filePath)
            print(3*"\n"+"These are an example the following tags found in the folder names.\nYou will be asked to name them for convenience, then choose the tags wou wish to keep in the file name.\nIf any new tags are found you will be prompted if you wish to add them to the naming convention.\nWARNING: Consider what the tag represents rather than the actual tag when deciding the namimg convention. This prompt will show up only once.")
            
        for tag in usefulInfoList:
            if tag not in previousInfoList:
                tagName = input(f"What does the tag \"{tag}\" represent?\n")
                if tagName != "quit":
                    usefulInfoPosDict[tagName] = usefulInfoList.index(tag)
                else:
                    return
        
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
                        
                    correctSelection = input("\nIs this correct?[Y/N]\n")

                infoTemplate = tempList2

                for i in tempDict.values():
                    usefulInfoPosDictList = list(usefulInfoPosDict.keys())
                    if i not in tempList2:
                        if (i+" (Unused)") not in usefulInfoPosDictList:
                            usefulInfoPosDict = { (value+" (Unused)" if value == i else value):key for (key,value) in tempDict.items() }
                    elif i in tempList2:
                        if  i in usefulInfoPosDictList and " (Unused)" in i:
                            iIndex = list(tempDict.keys())[list(tempDict.values()).index(i)]
                            d1 = {iIndex:i.replace(" (Unused)","")}
                            tempDict.update(d1)
                            usefulInfoPosDict = { (i.replace(" (Unused)","") if value == i else value):key for (key,value) in tempDict.items() }

            else:
                print("Ignoring new entries.")

    elif mode == "Get Info":
        if separatorFlag:
            allInfoList,_fileName,fileExtension, usefulInfoPosDict = splitString(filePath,separator,extraParams="Use Separator")
        else:
            allInfoList,_fileName,fileExtension, usefulInfoPosDict = splitString(filePath,separator)
        for item in infoTemplate:
            try:
                infoPos = usefulInfoPosDict[item]
                infoList.append(allInfoList[infoPos])

            except IndexError:
                infoList.append("")

    return (infoList, infoTemplate,fileExtension,usefulInfoPosDict)

def renameFile(filePath,infoList=[],fileExtension="",separator = "_", failCounter = 0):
    '''
    short explanation

    in depth explanation

    Parameters:
        -
    
    Returns:
        -

    '''

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
    
def main(usefulInfoPosDictList = {}):
    '''
    Main function of the program.

    Parameters:
        - usefulInfoPosDict: (dict) Dictionary containing the position in the splited file path for the given tag.(Default = {})
    
    Returns:
        - exitFlag: (bool) Looping condition for the module. Always returns True.
        - usefulInfoPosDict: (dict) Dictionary containing the position in the splited file path for the given tag.(Default = {})

    '''
    
    currentPath = os.path.abspath(os.getcwd())

    global dirCount,currentDir
    dirCount,currentDir = getDirs(currentPath)
    if dirCount == -1: return False
    separator = "_"
    fileExtension = input("What is the file extension of the file(s) you are trying to rename?\n")

    if input(f"Please confirm that the desired file extension is ({fileExtension}) [Y/N]: ") not in ["Y","y"]:
        fileExtension = input("What is the desired file extension?: ")
    if "." not in fileExtension:
        fileExtension = "."+fileExtension
    
    
    separatorPrompt = input("Are you using separators to store information in the folder names?[Y/N]\nIf yes, please indicate it with a space in between: (Optional)") 
    if separatorPrompt == "quit": return True  
    if separatorPrompt != "N":
        separator = separatorPrompt.replace("Y ","").replace("y ","").replace("Y","").replace("Y","")
        global separatorFlag
        separatorFlag = True
        

    for root, _dirs, files in os.walk(currentDir,topdown=True,followlinks=False):
        for name in files:
            if name.endswith(fileExtension):
                filePathString = root + os.sep +name
                global fileCounter,infoTemplate
                if fileCounter == 0:                    
                    _infoList, infoTemplate, _fileExtension, usefulInfoPosDict = getInfoFromFolders(filePath=filePathString,separator=separator,mode="Make Template",usefulInfoPosDict= usefulInfoPosDict)
                    if _fileExtension == 'quit': return True,{}
                    infoList,_infoTemplate,fileExtension, usefulInfoPosDict = getInfoFromFolders(filePathString, separator=separator, infoTemplate = infoTemplate, mode="Get Info", usefulInfoPosDict=usefulInfoPosDict)
                    renameFile(filePathString,infoList,fileExtension,separator)

                else:
                    infoList, _infoTemplate, fileExtension, usefulInfoPosDict= getInfoFromFolders(filePathString, separator=separator, infoTemplate = infoTemplate, mode="Get Info", usefulInfoPosDict= usefulInfoPosDict)
                    renameFile(filePathString,infoList,fileExtension,separator)


                fileCounter += 1
                
    dirCount -=1

    return True, usefulInfoPosDict

#Initial variable setup:

exitFlag = False #Looping Condition.
visitedDirs = [] #List that contains the directories already visited by the module.
dirCount = 0 #Number of directories that are in the same folder as the module(does not include visited directoreis).
currentDir = "" #String that contains the path to the current working directory.
infoTemplate = [] #List that contains the tags that should be present in the file name.
usefulInfoPosDict = {} #Dictionary that contains the tag names and their position in the the splited file path.
fileCounter,currentDirectoryDepth = 0,0 # Number of files already renamed, and the order of the deepest folder already visited respectively.
separatorFlag = False #Flag that defines if the user is using a separator in their naming convention.


#Main Loop:

while not exitFlag:
    exitFlag,usefulInfoPosDict = main(usefulInfoPosDict)

    if dirCount > 0:
        if input(f"There are still {dirCount} directories remaining, do you wish to continue?[Y/N]:\n") not in ["Y","y"]:
            exitFlag = False
            if input("Do you wish to use the same configurations as last time?[Y/N]:\n") not in ["Y","y"]:
                global fileCounter
                fileCounter = 0