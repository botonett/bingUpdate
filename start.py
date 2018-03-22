import os
import shutil
import fileinput
import time
from shutil import copyfile
from shutil import move
import pip
import platform
import xml.etree.ElementTree
from unipath import Path
import sys
import requests
from bs4 import BeautifulSoup
current_user = os.getlogin()
current_working_dir, filename = os.path.split(os.path.abspath(__file__))
home = Path(current_working_dir).parent
sys.path.append(home)
os.chdir(current_working_dir)

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
            os.system('cd "{}"'.format(home))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format(home+"\\BingGUI"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/BingGUI"))
            time.sleep(5)
            os.system("move " + current_working_dir+"\\BingGUI " + home)
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
            os.system('cd "{}"'.format(home))
            time.sleep(1)
            os.system('rmdir /S /Q "{}"'.format(home+"\\bingAuto"))
            time.sleep(1)
            os.system('git clone "{}"'.format("https://github.com/botonett/bingAuto"))
            time.sleep(1)
            updateCurrentVersion2(serverVersion)
            time.sleep(5)
            os.system("move " + current_working_dir+"\\bingAuto " + home)
            time.sleep(1)
            return "Update bingAUTO Sucessful"
        else:
            return "No bingAUTO Update Available"
    except Exception as e:
        print("update failed: " + str(e))     
        return "An Error Has Occured While Attempting Update."

def getCurrentVersion():
    currentVersion = 0
    with open(home+"\\data\\start-tracker.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion

def getCurrentVersion2():
    currentVersion = 0
    with open(home+"\\data\\version.dat",'r') as curVer:
        for line in curVer:
            currentVersion = int(line.strip())
        curVer.close()
    return currentVersion
def updateCurrentVersion2(version):
    with open(home+"\\data\\version.dat",'w') as curVer:
        curVer.write(str(version))
        curVer.close()
        
def updateCurrentVersion(version):
    with open(home+"\\data\\start-tracker.dat",'w') as curVer:
        curVer.write(str(version))
        curVer.close()
    
def getAccount():
    profile = []
    with open(home+"\\data\\gitAccount.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    return profile[0],profile[1]

def getMailAccount():
    profile = []
    with open(home+"\\data\\reportEngine.dat", 'r') as pf:
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
    os.system("xcopy " + home +"\\bingUpdate\\favicon.ico " + "C:\\Users\\"+current_user+"\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\appJar\\resources\\icons /Y")
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
    with open(home+"\\data\\profile.dat", 'r') as pf:
            for line in pf:
                 profile.append(line.strip())
    with open(home+"\\data\\shutdown.dat", 'r') as pf:
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
    print("Current Windows 10 Build: " + str(currentSystem))
    if(currentSystem in supportedSystems):
        cdir = home+"\\bingUpdate\\edgeDrivers\\"
        src = cdir + str(currentSystem) + '.exe'
        dst = home+"\\bingAuto"
        with open("copyEdge.bat",'w') as copyEdge:
            copyEdge.write("xcopy " + src + " " + dst + " "+ "/Y")
            copyEdge.close()
        os.system("copyEdge.bat")
        #os.system("deleteEdge.bat")
        os.system("del "+ home +"\\bingAuto\\MicrosoftWebDriver.exe /Q")
        with open("renameEdge.bat",'w') as rename:
            rename.write("rename " + dst + "\\" + str(currentSystem) + '.exe' + " " + "MicrosoftWebDriver.exe")
            rename.close()
        os.system("renameEdge.bat")
        return "Done setting up Edge Driver"
    else:
        print("updating edge driver!")
        subject = Host + " " + VM + " updated edge driver"
        body = Account + " " + "is attempting to update edge driver"
        send_email(user, pwd, Report, subject, body)
        edgeUpdate = getEdgeBuild()
        for item in edgeUpdate:
            if(item[0] == currentSystem):
                download  = download_file(item[1])
                temp = item[0]+".exe"
                move(home+"\\bingUpdate\\"+download,home+"\\bingUpdate\\"+temp)
                move(home+"\\bingUpdate\\"+temp,home+"\\bingUpdate\\edgeDrivers")
                stat = updateEdgeConfig(item[0])
                if(stat != "failed"):
                    setEdgeDriver()
        return "Not supported windows version"
def chromeVer():
    try:
        data = []
        with open(home+"\\bingUpdate\\suppportedChromeVersion.dat", 'r') as pf:
            for line in pf:
                data.append(line.strip())
        return data[0].split("-")[0]
    except:
        return "failed"
    
def setChromeDriver():
    e = xml.etree.ElementTree.parse('C:\\Program Files (x86)\\Google\Chrome\\Application\\chrome.VisualElementsManifest.xml').getroot()
    currentChromeVer = e[0].get('Square150x150Logo').split("\\")[0].split(".")[0]
    profile = get_profile()
    Account = profile[0]
    VM = profile[1].split("=")[1]
    Host = profile[2].split("=")[1]
    Report = profile[3].split("=")[1]
    PCSeach = int(profile[4].split("=")[1])
    MobileSearch = int(profile[5].split("=")[1])
    user, pwd = getAccount()
    try:
        currentChromeVer = int(currentChromeVer)
    except:
        subject = Host + " " + VM + " Unable to get current chrome version"
        body = Account + " unable to get current chromeversion"
        send_email(user, pwd, Report, subject, body)
        return "Unable to get current chromeversion."
    supportedSystems = []
    with open("suppportedChromeVersion.dat", 'r') as pf:
            for line in pf:
                 supportedSystems.append(line.strip())
    for version in supportedSystems:
        cdir = home+"\\bingUpdate\\chromeDrivers\\"
        dst = home+"\\bingAuto"
        ver = version.split("-")
        r = range(int(ver[1]),int(ver[2])+1)
        if(currentChromeVer in r):
            os.system("xcopy " + cdir + ver[0]+ "\\" + "chromedriver.exe" + " " + dst + " " + "/Y")
            return "Done"
            break
    subject = Host + " " + VM + " An unsupported version of chrome is running"
    body = Account + " is searching on an unsupported chrome version"
    send_email(user, pwd, Report, subject, body)
    return "An unsupported version of chrome is running"
def updatePip():
    os.system("pip install --upgrade pip")
    return "Done"

def lastestChromeVer():
    import requests
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    data = (requests.get(url)).text.strip()
    url2 = "https://chromedriver.storage.googleapis.com/"+data+"/notes.txt"
    data2 = (requests.get(url2)).text.strip()
    data2ver = data2.split("\n")[0].strip("-").split(" ")[1].strip("v")
    data2support = data2.split("\n")[1].split(" ")[2].strip("v")
    if(data == data2ver):
        return data2ver, data2support
    else:
        return "error while checking lastest chrome version."
def downloadChrome(ver):
    try:
        import requests, zipfile, io
        zip_file_url = "https://chromedriver.storage.googleapis.com/"+ ver +"/chromedriver_win32.zip"
        r = requests.get(zip_file_url)
        if(r.ok):
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(current_working_dir)
        if not os.path.exists(current_working_dir+ "\\"+ "chromeDrivers\\"+ver):
            try:
                os.makedirs(current_working_dir+ "\\"+ "chromeDrivers\\"+ver)
                move(current_working_dir+"\\chromedriver.exe",current_working_dir+"\\chromeDrivers\\"+ver)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            except Exception as E:
                print(str(E))
                os.remove(current_working_dir+"\\chromedriver.exe")
        return "done"
    except Exception as E:
        print("failed to download lastest chrome driver verion with error: " + str(E))
        return "failed"

def updateChromeConfig(ver,sup):
    try:
        newLine = ver+"-"+sup+"\n"
        data = []
        data.append(newLine)
        with open(home+"\\bingUpdate\\suppportedChromeVersion.dat", 'r') as pf:
            for line in pf:
                data.append(line)
        with open(home+"\\bingUpdate\\suppportedChromeVersion.dat", 'w') as ud:
            for line in data:
                ud.write(line)
        return "done"
    except Exception as E:
        print("failed to update chome config with error: " + str(E))
        return "failed"

def updateEdgeConfig(ver):
    try:
        newLine = ver+"\n"
        data = []
        data.append(newLine)
        with open(home+"\\bingUpdate\\supportedSystems.dat", 'r') as pf:
            for line in pf:
                data.append(line)
        with open(home+"\\bingUpdate\\supportedSystems.dat", 'w') as ud:
            for line in data:
                ud.write(line)
        return "done"
    except Exception as E:
        print("failed to update edge config with error: " + str(E))
        return "failed"
    
def download_file(url):
    try:
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(home+"\\bingUpdate\\"+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        return local_filename
    except Exception as E:
        print("failed to download requested file with error: " + str(E))
        return "failed"

def getEdgeBuild():
    try:
        url = "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
        data = (requests.get(url)).text
        soup = BeautifulSoup(data, 'html.parser')
        mydivs = soup.findAll("ul", {"class": "bare subsection__body driver-downloads"})
        data = []
        for ul in mydivs:
            for li in ul.findAll('li'):
                temp = li.a.get('aria-label').split(" ")[-1]+ " " + str(li.a.get('href'))
                if(temp.split(" ")[0]!= "Insiders"):
                    data.append(temp.split(" "))
        return data
    except Exception as E:
        print("failed to get latest edge build with error: " + str(E))
        return "failed"


if __name__ == "__main__":
    updatePip = updatePip()
    while(True):
        if(updatePip == "Done"):
            break
        else:
             time.sleep(1)
    print("Done with pip")

    ver,sup =lastestChromeVer()
    curChromeVer = chromeVer()
    if(curChromeVer != "failed"):
        if(ver != curChromeVer):
            stat = downloadChrome(ver)
            updateChromeConfig(ver,sup)
    else:
        print("failed to update chrome driver")
    print("Done setting up chrome driver.")
    setChromeDriver = setChromeDriver()
    while(True):
        if((setChromeDriver == "Unable to get current chromeversion.") or (setChromeDriver == "Done") or (setChromeDriver == "An unsupported version of chrome is running")):
            break
        else:
            time.sleep(1)
    print(setChromeDriver)  
    setEdgeDriver = setEdgeDriver()
    while(True):
        if((setEdgeDriver == "Done setting up Edge Driver") or (setEdgeDriver == "Not supported windows version")):
            break
        else:
            time.sleep(1)
    print(setEdgeDriver)     
    """
    updatePackage = update()
    while(True):
        if((updatePackage == "Done") or (updatePackage == "Failed!")):
            break
        else:
             time.sleep(1)
    print(updatePackage)
    """
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
    #set run2.bat to current dir
    with open("run2.bat",'w') as setcur:
            setcur.write("ping 127.0.0.1 -n 5 > nul")
            setcur.write("\n")
            setcur.write("cd " + home + "\\bingUpdate")
            setcur.write("\n")
            setcur.write("python start.py")
            setcur.close()
    from subprocess import call
    call(["CScript.exe", "script.vbs"])
    #C:\Users\bing\AppData\Local\Programs\Python\Python35\Lib\site-packages\appJar\resources\icons
    #os.system("run.bat")
    exit(0)
    


