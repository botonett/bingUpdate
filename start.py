from github import Github
from appJar import gui
import os
import shutil
import fileinput
import time
from shutil import copyfile

def primaryUpdate():
    try:
        account,password = getAccount() 
        #create a Github instance:
        serverVersion = 0
        g = Github(account, password)
        for repo in g.get_user().get_repos():
            if repo.name == "BingGUI":
                temp =  repo.get_stats_contributors()
                while(temp == None):
                    time.sleep(2)
                    temp =  repo.get_stats_contributors()
                serverVersion =temp[0].total
        if(serverVersion != getCurrentVersion()):  
            #os.system('rmdir /S /Q "{}"'.format(directory))
            os.system('cd "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0"))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0\\BingGUI"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/BingGUI"))
            time.sleep(1)
            updateCurrentVersion(serverVersion)
            return "Update GUI Sucessful"
        else:
            return "No GUI Update Available"
    except Exception as e:
       
        return "An Error Has Occured While Attempting Update."

def secondaryUpdate():
    try:
        account,password = getAccount()
        #create a Github instance:
        serverVersion = 0
        g = Github(account, password)
       
        for repo in g.get_user().get_repos():
            if repo.name == "bingAuto":
                temp =  repo.get_stats_contributors()
                while(temp == None):
                    time.sleep(2)
                    temp =  repo.get_stats_contributors()
                serverVersion =temp[0].total
        if(serverVersion != getCurrentVersion2()):  
            #os.system('rmdir /S /Q "{}"'.format(directory))
            os.system('cd "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0"))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format("C:\\Users\\bing\\Desktop\\Bing2.0\\bingAuto"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/bingAuto"))
            time.sleep(1)
            updateCurrentVersion2(serverVersion)
            time.sleep(1)
            return "Update bingAUTO Sucessful"
        else:
            return "No bingAUTO Update Available"
    except Exception as e:
        print("update failed: " + str(e))     
        return "An Error Has Occured While Attempting Update."

def getCurrentVersion():
    currentVersion = 0
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\start-tracker.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion

def getCurrentVersion2():
    currentVersion = 0
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\version.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion
def updateCurrentVersion2(version):
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\version.dat",'w') as curVer:
        curVer.write(str(version))
        curVer.close()
        
def updateCurrentVersion(version):
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\start-tracker.dat",'w') as curVer:
        curVer.write(str(version))
        curVer.close()
    
def getAccount():
    profile = []
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\gitAccount.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile[0],profile[1]

if __name__ == "__main__":
    guiUpdate = primaryUpdate()
    while(True):
        if((guiUpdate != "Update GUI Sucessful") or (guiUpdate != "No GUI Update Available") or (guiUpdate != "An Error Has Occured While Attempting Update.")):
            break
        else:
            time.sleep(1)
    print(guiUpdate)
    autoUpdate = secondaryUpdate()
    while(True):
        if((autoUpdate != "Update bingAUTO Sucessful") or (autoUpdate != "No bingAUTO Update Available") or (autoUpdate != "An Error Has Occured While Attempting Update.")):
            break
        else:
            time.sleep(1)
    print(autoUpdate)
    from subprocess import call
    #call(["CScript.exe", "C:\\Users\\bing\\Desktop\\Bing2.0\\script.vbs"])
    os.system("run.bat")
    


