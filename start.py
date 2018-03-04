import os
import shutil
import fileinput
import time
from shutil import copyfile
import pip
import platform

def primaryUpdate():
    from github import Github
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
            time.sleep(5)
            os.system("moveGUI.bat")
            time.sleep(1)
            updateCurrentVersion(serverVersion)
            return "Update GUI Sucessful"
        else:
            return "No GUI Update Available"
    except Exception as e:
       
        return "An Error Has Occured While Attempting Update."

def secondaryUpdate():
    from github import Github
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
            time.sleep(5)
            os.system("moveAuto.bat")
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

def getMailAccount():
    profile = []
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\reportEngine.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile[0],profile[1]

def update():
    try:
        with open("packages.txt",'r') as curVer:
            for line in curVer:
                pip.main(['install', line.strip()])
            curVer.close()
        return "Done"
    except Exception as E:
        print(str(E))
        return "Failed!"
def setIcon():
    os.system("setIcon.bat")
    return "Done"

#send email function
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = 'Report Engine'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the report mail')
    except:
        print("failed to send mail")
def get_profile():
    profile = []
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\profile.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    with open("C:\\Users\\bing\\Desktop\\Bing2.0\\data\\shutdown.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile      

def setEdgeDriver():
    profile = get_profile()
    Account = profile[0]
    VM = profile[1].split("=")[1]
    Host = profile[2].split("=")[1]
    Report = profile[3].split("=")[1]
    PCSeach = int(profile[4].split("=")[1])
    MobileSearch = int(profile[5].split("=")[1])
    user, pwd = getAccount()
    supportedSystems = []
    with open("supportedSystems.dat", 'r') as pf:
            for line in pf:
                 supportedSystems.append(line.strip())
    currentSystem = platform.version().split(".")[2]
    if(currentSystem in supportedSystems):
        cdir = "C:\\Users\\bing\\Desktop\\Bing2.0\\bingUpdate\\"
        src = cdir + str(currentSystem) + '.exe'
        dst = "C:\\Users\\bing\\Desktop\\Bing2.0\\bingAuto"
        with open("copyEdge.bat",'w') as copyEdge:
            copyEdge.write("xcopy " + src + " " + dst + " "+ "/Y")
            copyEdge.close()
        os.system("copyEdge.bat")
        os.system("deleteEdge.bat")
        with open("renameEdge.bat",'w') as rename:
            rename.write("rename " + dst + "\\" + str(currentSystem) + '.exe' + " " + "MicrosoftWebDriver.exe")
            rename.close()
        os.system("renameEdge.bat")
        return "Done setting up Edge Driver"
    else:
        subject = Host + " " + VM + " Is currently running unsupported windows 10 version."
        body = Account + " is currently unable to search due to unsupported edge driver version."
        send_email(user, pwd, Report, subject, body)
        return "Not supported windows version"

if __name__ == "__main__":
    setEdgeDriver = setEdgeDriver()
    while(True):
        if((setEdgeDriver == "Done setting up Edge Driver") or (setEdgeDriver == "Not supported windows version")):
            break
        else:
            time.sleep(1)
    print(setEdgeDriver)     
    updatePackage = update()
    while(True):
        if((updatePackage == "Done") or (updatePackage == "Failed!")):
            break
        else:
             time.sleep(1)
    print(updatePackage)
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
    #testGUI
    setIcon = setIcon()
    while(True):
        if(setIcon == "Done"):
            break
        else:
             time.sleep(1)
    from subprocess import call
    call(["CScript.exe", "script.vbs"])
    #C:\Users\bing\AppData\Local\Programs\Python\Python35\Lib\site-packages\appJar\resources\icons
    #os.system("run.bat")
    exit(0)
    


