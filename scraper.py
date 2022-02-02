from bs4 import BeautifulSoup
import requests
from tkinter import *
import tk

def getEntry(Entry):
    res = Entry.get()
    print(res)
    return res

    


    

class FileNameAndLocation():
    def __init__(self):
        self.FileName = ""
        self.FileLocation = ""
        self.Path = ""

    def UpdateFileName(self,NewName):
        self.FileName = NewName
    def UpdateFileLocation(self, NewLocation):
        self.FileLocation = NewLocation

    def UpdatePath(self):
        self.Path = self.FileLocation + self.FileName + ".csv"
    def GetFileLocation(self):
        self.FileLocation = filedialog.askdirectory()
        self.UpdatePath()
        FileDirectory.delete(0, END)
        FileDirectory.insert(0, self.FileLocation)
    def GetPath(self):
        return self.Path

class HtmlPage():
    def __init__(self):
        self.HtmlContent = ""
        self.Title = ""
        self.UrlPage = ""
    def UpdateHtmlContent(self, NewContent):
        self.HtmlContent = NewContent


from bs4 import BeautifulSoup
import requests
from tkinter import *



class MailAddress():
    def __init__(self):
        self.MailValue = ""
        self.MailUrlSource = ""
        self.MailPageTitle = ""
    def UpdateMailValue(self, NewMailValue):
        self.MailValue = NewMailValue
    def UpdateMailUrlSource(self, NewMailUrlSource):
        self.MailUrlSource = NewMailUrlSource
    def UpdateMailPageTitle(self, NewMailPageTitle):
        self.MailPageTitle = NewMailPageTitle

class HtmlPage():
    def __init__(self):
        self.HtmlContent = ""
        self.Title = ""
        self.UrlPage = ""
    def UpdateHtmlContent(self, NewContent):
        self.HtmlContent = NewContent

PageActive = HtmlPage()


def DownloadPage(UrlSource):
    try:
        RequestPage = requests.get(UrlSource) # get page
        GoodPage =BeautifulSoup(RequestPage.text, "lxml")
        PageActive.UpdateHtmlContent(GoodPage)
        TitleTags = PageActive.HtmlContent.find("title")
        PageActive.Title = TitleTags.text
        PageActive.UrlPage = UrlSource
    except:
        print("     URL INVALIDE")

def DeleteUnknown(NewValue):
    ArobasePosition = NewValue.find("@")
    i = ArobasePosition
    SpacePosition = 0
    while i > 0:
        if NewValue[i] == " ":
            SpacePosition = i
            break
        i = i - 1
    i = ArobasePosition
    SpacePositionR = len(NewValue)
    while i < len(NewValue):
        if NewValue[i] == " ":
            SpacePositionR = i
            break
        i = i + 1
    ReturnWord = ""
    for i in range(SpacePosition , SpacePositionR):
        ReturnWord = ReturnWord + NewValue[i]
    return ReturnWord

MailAddressTable = []
LinkTable = ["http://localhost/c/Contactez-nous%20-%20AL-INFOTECH%20SARL.html"]

def FindLink(UrlDeLapage):
    try:
        page = requests.get(UrlDeLapage)

        html = BeautifulSoup(page.text, 'lxml')
        for line in html.find_all('a'):
            if line.get('href'):
                linkOk = line.get('href')
                httppos = linkOk.find("http")
                print("etat ancien : "+httppos)
                if httppos == 0:
                    LinkTable.append(linkOk)
                else:
                    linkOk = UrlDeLapage + linkOk
                    httppos = linkOk.find("http")
                    print("Nouvel etat : "+httppos)
                    LinkTable.append(linkOk)

                print("         Noveau lien  trouvé  :  " +linkOk )
    except:
        print("     URL INVALIDE ")


def FindMailAddress():
    AllMailAddress = PageActive.HtmlContent.findAll(text = re.compile("@"), limit = 100)
    for Mail in AllMailAddress:
        Mail = DeleteUnknown(Mail)
        Mail = Mail.strip()
        ArobasePosition = Mail.find("@")
        FullStopPosition = Mail.find(".")
        if (ArobasePosition >= 4) and (FullStopPosition >= 5) and (len(Mail) > 7):
            AddressMailOk = MailAddress()
            AddressMailOk.MailValue = Mail
            AddressMailOk.MailUrlSource = PageActive.UrlPage
            AddressMailOk.MailPageTitle = PageActive.Title
            MailAddressTable.append(AddressMailOk)
            print("             Nouvelle adresse mail trouvée : " + AddressMailOk.MailValue)

i = 1
for lien in LinkTable:

    DownloadPage(lien)
    print("     RECHERCHE D'ADRESSES MAIL ET DE LIEN SUR LA PAGE  :: " + lien)
    print("     cette page a pour titre : " + PageActive.Title)
    FindMailAddress()
    FindLink(lien)
    i = int(i) + 1
    if i==10:
        print ("        SEUIL ATTEINT MERCI!!!!!!!!!!!")
        break

print("                     Toutes les adresses MAIL ")

for l in MailAddressTable:
    print(l.MailValue)



FileConfiguration = FileNameAndLocation()
FileConfiguration.FileName = "Fichier d'adresses mail"






        
 

def WriteOnFile():
    FileDirectorie = FileConfiguration.GetPath()

    FileWrite = open(FileDirectorie, "w")
    FileWriter = csv.writer(FileWrite)
    Header = ["Adresse mail " , "Lien de l'adresse mail" , "Titre de la page"]
    FileWriter.writerow(Header)
    for Mail in MailAddressTable:
        MAILW = [Mail.MailValue, Mail.MailUrlSource, Mail.MailPageTitle]
        print(MAILW)
        FileWriter.writerow(MAILW)

    FileWrite.close()







MainWndow = Tk()
MainWndow.title("   Target Spider Crawler   ")
MainWndow.geometry("800x600")
MainWndow.resizable(width = False , height = False)

TitleFrame = Frame(MainWndow)
AppTitle = Label(TitleFrame , text = "Target Spider Crawler",
    fg = "red", font = ("Cooper Std Black", 15))
TitleFrame.pack()
AppTitle.pack(pady = 15)


FormFrame = Frame(MainWndow).pack()
Text = Label(FormFrame, text = "Entrer l'URL", font = ("Cooper Std Black", 10)).pack(pady = 6)
#myEntry = tk.Entry(FormFrame, bd = 4 , font = ("Cooper Std Black", 10), width = 25).pack(pady = 6)

myEntry = tk.Entry(FormFrame,  bd = 4 , font = ("Cooper Std Black", 10), width = 25)
myEntry.pack(pady=20)



FrameOther = Frame(MainWndow).pack(padx = 12, pady = 12)
Text2 = Label(FormFrame, text = "Selectionner le dossier d'enregistrement du fichier", font = ("Cooper Std Black", 10)).pack(padx = 6, pady = 6)
FileDirectory = tk.Entry(FormFrame,  bd = 4 , font = ("Cooper Std Black", 10), width = 25)
FileDirectory.pack(pady=20)
FileDirectoryButton = Button(FrameOther, text = "Selectionner",  bd = 2 , font = ("Cooper Std Black", 10), width = 15, command = lambda:[FileConfiguration.GetFileLocation()]).pack()


Text3 = Label(FormFrame, text = "Entrez le nom d'enregistrement du fihier", font = ("Cooper Std Black", 10)).pack(padx = 6, pady = 6)
FileName = tk.Entry(FormFrame,  bd = 4 , font = ("Cooper Std Black", 10), width = 25)
FileName.pack(pady=20)


SpiderButton = Button(FrameOther, text = "Lancer le Spider Crawler",  bd = 2 , font = ("Cooper Std Black", 10) , fg = "green" ,  width = 30, command = lambda:[SpiderCrawl()]).pack(padx = 6, pady = 20)

MainWndow.mainloop()

