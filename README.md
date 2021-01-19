# File_Renamer

 This module has the capability of renaming files in batch by extracting information from a series of folders and using it, according to user input, rename a series of files automatically. It is the first part of a two program series used for spheroid detection and classification.  
 Python does not use *Programs*, instead it uses *Modules*, this is the naming convention that will be used througout this document.

## REQUIREMENTS:  
- Python 3.8 or greater.  

## INSTRUCTIONS:  
    
1.	Download the File_Renamer.py module and copy it to the same level as the outermost folder you want to be renamed.  
      Example:  
        *C:/.../Generic_Folder*    
           *------>Folder_To_Be_Renamed1*   
           *------>Folder_To_Be_Renamed2*  
           *------>Folder_To_Be_Renamed3*  
           *------>Insert __File_Renamer.py__ Here.* 
        
2.	Run the module, either by double-clicking it, or by running it from the terminal, and follow the on-screen instructions carefully.  

3. After each run it will ask if you want to continue renaming folders, so long as there are folders left to be renamed, but you can always choose to exit at any point.  

4. With the exception of the step that asks the user to name the "tags", if at any point you wish to exit the module, entering "quit" (without the quotes) in most input fields will terminate the module at its current state.  

## IMPORTANT NOTES AND DISCLAIMERS:
  
 **This program _WILL RENAME FILES IN YOUR SYSTEM_, make sure that you wish to do so and have a backup copy of your data, the program is really smart in trying its best to prevent any information from being lost, but it is not flawless! _If you tell it to rename using a convention that you regret afterward, or a mistake was made in any step there is no going back!_ You have been warned!  
 I do not take responsibility for any damage to your files as a result of you running this program. Use it at your own risk!**

 If you are using separators to store information within your folder names, you can if you choose to let the program know and it will track each information separedly. This is not necessary, and if you feel that doing so might disrupt your naming convention you are more than welcome to not do so.  
   Example using "\_" as a separator:  
     *Information1*\_*Information2*\_*Information3*(Name of the folder)  
    
 If you tell the program to use \"\_\" as a separator, it will treat *Information1*, *Information2*, and *Information3* separately because there is the separator \"\_\" in between each of those. However, if you tell it to ignore the separator by telling the module you are not using separators, it will treat *Information1\_Information2\_Information3* as a single *tag*.
    
 When the program asks you to give a name to a “*tag*”, if it asks for the same information twice it is because it shows up more than once in the order of folders it has looked through if you want to keep only one of those *tags*, either name both of them the exact same thing, or just don’t select that second tag when the program prompts you to.  

 This program does not read the content of the “*tags*” themselves. Instead, it looks for information in each layer of folders it walks through:  
      *C:/.../Generic_Folder  
          ----->File_Renamer.py  
          ----->Folder_To_Be_Renamed(layer 0)  
            ----->SubFolder1(layer 1)  
                ----->SubSubFolder2(layer 2)  
                    *.............*  
                    *File_To_Be_Renamed.extension(layer n)*

 As you can see, the module also treats the file name as a layer of its own, allowing it to get information from there as well.
 
 Each layer gets a *tag* of its own that represents it (unless you use a separator within your folder names, in which case each information in the same “folder layer” gets a *tag* of its own), and the program stores the position of each *tag* in the file path(the address of each file in your system). So if you want to store information from SubFolder2, but you do not want to store information from Subfolder1, you will have to add the *tag* to the naming convention because the program cannot make that distinction.  
  (...)  
    *SubFolder1Information(layer x)*  
      *SubSubFolders.......*  
    *SubFolder2Information(layer x)*  

 Both SubFolder1 and SubFolder2 are on the same layer, so to keep information from the one you must keep information from the other, it is just a limitation of the program. So beware when you choose to remove information, because it might affect other files.
 
 This program generates a file named \"reportInformation.pkl\". It contains information that is used in the other half of this project(Spheroid_Detection) to generate a report after running it. If you do not intend on using the other module, just delete this file. Otherwise, keep this file in the same folder that you run Spheroid_Detection from.
