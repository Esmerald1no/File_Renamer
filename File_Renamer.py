import os

#TEMP: Current Directory not the same as working directory.
os.chdir(r"C:\Users\Bruno\Dropbox\ImageProcessing_Bruno")

directories = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir,topdown=True,followlinks=False):
        #print(dirs,files)
        for name in files:
            if name.endswith(".tif"):
               # print(name)
                r.append(os.path.join(root, name))

    return r


print(directories)
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

#For Testing ONLY
a = list_files(currentDir)
with open(r"D:\Test.txt",'w') as f:
    for item in a:
        f.write(item+"\n")