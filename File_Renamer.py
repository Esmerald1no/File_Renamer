import os
from collections import defaultdict

#TEMP: Current Directory not the same as working directory.
os.chdir(r"C:\Users\Bruno\Dropbox\ImageProcessing_Bruno")



def list_files(dir):
    r = []
    fileCounter = 0
    for root, dirs, files in os.walk(dir,topdown=True,followlinks=False):
        #print(dirs,files)
        for name in files:
            if name.endswith(".tif"):
                #print(name)
                r.append(os.path.join(root, name))
                filePathString = root + os.sep +name
                if fileCounter == 0:
                    infoTemplate = getInfoFromFolders(filePath=filePathString,mode=0)[1]
                else:
                    pass
                fileCounter += 1 
    return r

def getDirs(path):
    directories = [name for name in os.listdir(currentPath) if os.path.isdir(name)]
    dirCount = len(directories)
    if dirCount>1:
        print("Multiple Directories Found, Select Working Directory:")
        for i in range(dirCount):
            print(f"{i+1}. {directories[i]}")
            currentDir = int(input())
            os.chdir(directories[currentDir-1])
            currentDir = os.getcwd()
    else:   
        if (currentDir := input(f"The directory found is \"{directories[0]}\" is this the desired directory? [Y/N].\nIf this is not the desired directory, insert the path for the new directory or move this module to that location: \n")) != "Y":
            currentDir = currentDir.lstrip("N ")
            os.chdir(currentDir)
        else:
            os.chdir(directories[0])
            currentDir = os.getcwd()
    return (directories,dirCount,currentDir)

def getInfoFromFolders(filePath,separator = "_",infoTemplate=[],mode = 1):
    #TODO: #3 Figure out how to get information out of "filestring".
    infoList = []
    if mode == 0:
        topDir = currentDir.split("\\")[-1]
        topDirPos = filePath.find(topDir)
        print(topDirPos)
        usefulInfoString = filePath[topDirPos:]
        print(usefulInfoString)
        tempList = usefulInfoString.split("\\")
        fileName = tempList[-1]
        print(fileName)
        usefulInfoList = tempList[:-1]
        print(usefulInfoString)

        #TODO: #5 Add logic for user to decide which naming pattern they want.
        infoTemplate = []
    else:
        infoTemplate = infoTemplate
    
    return (infoList, infoTemplate)

def renameFile(filePath):
    #TODO:Write #2 renaming routine using information from getInfoFromFolders() and original name.
    pass

def main():
    global currentPath 
    currentPath = os.path.abspath(os.getcwd())
    global directories,dirCount,currentDir
    directories,dirCount,currentDir = getDirs(currentPath)

    #For Testing ONLY
    a = list_files(currentDir)
    with open(r"D:\Test.txt",'w') as f:
        for item in a:
            f.write(item+"\n")

directories,dirCount,currentDir,currentPath = [],0,"",""
usefulInfoDict = defaultdict(dict)
while 1:
    #TODO: #4 Define Looping condition.
    main()
    break