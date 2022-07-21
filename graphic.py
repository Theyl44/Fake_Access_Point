import wx, os, subprocess
from wx.adv import AnimationCtrl
import wx.grid as grid

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.Centre()
        
        self.hLeftPanel = LeftPanel(self)
        self.hRightPanel = RightPanel(self)
        
        ### --- RIGHT SIDE --- ###
        self.width,self.height = parent.GetSize()
        self.x = int(self.width/2)
        self.xbsize=200
        self.ybsize=50
        self.step = 0
        self.font = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
        self.st = wx.StaticText(self, pos = (int((self.x/2)+self.x-85),30), size=(200,40) , label ="Entrez un nom de Wifi")
        self.st.SetForegroundColour('white')
        self.st.SetFont(self.font)
        
        self.checked = 0
        self.fapname = wx.TextCtrl(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)-85)), size=(140,40))
        self.restart = wx.StaticText(self, pos = (int((self.x/2)-77),143), size=(200,40) , label ="Lancer au redémarrage")
        self.restart.SetForegroundColour('black')
        self.restart.SetFont(self.font)
        self.cb1 = wx.CheckBox(self, label = '                                           ',pos = (int((self.x/2)-100),140))
        self.Bind(wx.EVT_CHECKBOX,self.onChecked)
        
        self.info = wx.Image("img/info.png", wx.BITMAP_TYPE_ANY)
        self.info = self.info.Scale(20, 20, wx.IMAGE_QUALITY_HIGH)
        self.info = self.info.ConvertToBitmap()

        self.button = wx.Button(self, label='1. Point d\'accès' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4))), size=(self.xbsize,self.ybsize))
        self.button.Bind(wx.EVT_BUTTON, self.on_button1)
        self.button7 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+7), style = wx.BORDER_NONE)
        self.button7.Bind(wx.EVT_BUTTON, self.infosc1)
        self.button7.SetBitmap(self.info)
        self.button2 = wx.Button(self, label='2. Portail Captif' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+100)), size=(self.xbsize,self.ybsize))
        self.button2.Bind(wx.EVT_BUTTON, self.on_button2)
        self.button8 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+107), style = wx.BORDER_NONE)
        self.button8.Bind(wx.EVT_BUTTON, self.infosc2)
        self.button8.SetBitmap(self.info)
        self.button3 = wx.Button(self, label='3. Attaque Karma' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+200)), size=(self.xbsize,self.ybsize))
        self.button3.Bind(wx.EVT_BUTTON, self.on_button3)
        self.button9 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+207), style = wx.BORDER_NONE)
        self.button9.Bind(wx.EVT_BUTTON, self.infosc3)
        self.button9.SetBitmap(self.info)
        self.button4 = wx.Button(self, label='4. DNS Spoofing', pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+300)), size=(self.xbsize,self.ybsize))
        self.button4.Bind(wx.EVT_BUTTON, self.on_button4)
        self.button10 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+307), style = wx.BORDER_NONE)
        self.button10.Bind(wx.EVT_BUTTON, self.infosc4)
        self.button10.SetBitmap(self.info)
        ### --- ---------- --- ###
        
        ### --- LEFT SIDE --- ###
        self.lightpng = wx.Image("img/fap.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.darkpng = wx.Image("img/darkfap.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.img = wx.StaticBitmap(self, -1, self.lightpng, (8,170), (self.lightpng.GetWidth(), self.lightpng.GetHeight()))
        self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="INACTIF")
        self.active.SetForegroundColour('red')
        self.active.SetFont(self.font)
        self.on = 0
        self.button5 = wx.Button(self, label='Log', pos = (20,510), size=(60,40))
        self.button5.Bind(wx.EVT_BUTTON, self.on_button5)
        self.button6 = wx.Button(self, label='Reset', pos = (270,510), size=(60,40))
        self.button6.Bind(wx.EVT_BUTTON, self.on_button6)
        ### --- ---------- --- ###
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)        
        hBoxSizer.Add(self.hLeftPanel, 1, wx.EXPAND)
        hBoxSizer.Add(self.hRightPanel, 1, wx.EXPAND)        

        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(hBoxSizer, 1, wx.EXPAND)

        self.SetSizer(vBoxSizer)
    
    def onChecked(self, event):
        if self.checked == 0:
            self.hLeftPanel.SetBackgroundColour('#054867')
            self.hRightPanel.SetBackgroundColour('#ECECEC')
            self.st.SetForegroundColour('black')
            self.restart.SetForegroundColour('white')
            self.img.Destroy()
            self.img = wx.StaticBitmap(self, -1, self.darkpng, (8,170), (self.darkpng.GetWidth(), self.darkpng.GetHeight()))
            self.checked = 1
            if self.step != 0:
                self.name.SetForegroundColour('black')
        else:
            self.hLeftPanel.SetBackgroundColour('#ECECEC')
            self.hRightPanel.SetBackgroundColour('#054867')
            self.st.SetForegroundColour('white')
            self.restart.SetForegroundColour('black')
            self.img.Destroy()
            self.img = wx.StaticBitmap(self, -1, self.lightpng, (8,170), (self.lightpng.GetWidth(), self.lightpng.GetHeight()))
            self.checked = 0
            if self.step != 0:
                self.name.SetForegroundColour('white')
            
    def on_button1(self, event):
        if self.on == 0:
            if self.fapname.GetValue() == "":
                self.ShowWarning()
            else:
                self.on = 1
                self.step = 1
                self.fap = self.fapname.GetValue()
                self.fapname.Destroy()
                fontname = wx.Font(15, wx.NORMAL, wx.ITALIC, wx.BOLD)
                x = int(self.width/2 + self.width/4 - 12*(len(self.fap)/2))
                self.name = wx.StaticText(self, pos = (x,60), size=(200,40) , label = self.fap)
                self.name.SetFont(fontname)
                cmd="sudo sed -i -r \"s/^(fap_name=).*/fap_name=\\\""+self.fap+"\\\"/g\" scriptgraphic.sh"
                os.system(cmd)
                if self.checked == 0:
                    self.name.SetForegroundColour('white')
                    cmd="sudo ./scriptgraphic.sh 1"
                    os.system(cmd)
                    self.active.Destroy()
                    self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="ACTIF")
                    self.active.SetForegroundColour('green')
                    self.ShowSuccess()
                else:
                    self.name.SetForegroundColour('black')
                    cmd="sudo ./scriptgraphic.sh r 1"
                    os.system(cmd)
                    self.ShowReboot()
            
    def on_button2(self, event):
        if self.on == 0:
            if self.fapname.GetValue() == "":
                self.ShowWarning()
            else:
                self.step = 2
                self.button.Destroy()
                self.button2.Destroy()
                self.button3.Destroy()
                self.button4.Destroy()
                self.button7.Destroy()
                self.button8.Destroy()
                self.button9.Destroy()
                self.button10.Destroy()
                self.fap = self.fapname.GetValue()
                self.fapname.Destroy()
                cmd="sudo sed -i -r \"s/^(fap_name=).*/fap_name=\\\""+self.fap+"\\\"/g\" scriptgraphic.sh"
                os.system(cmd)
                fontname = wx.Font(15, wx.NORMAL, wx.ITALIC, wx.BOLD)
                xbsize=200
                ybsize=50
                x = int(self.width/2 + self.width/4 - 12*(len(self.fap)/2))
                self.name = wx.StaticText(self, pos = (x,60), size=(200,40) , label = self.fap)
                if self.checked == 0:
                    self.name.SetForegroundColour('white')
                else:
                    self.name.SetForegroundColour('black')
                self.name.SetFont(fontname)
                self.button21 = wx.Button(self, label='1. Simple Portail Captif' , pos = (int((self.x/2)+self.x-xbsize/2),int((self.height/4))), size=(xbsize,ybsize))
                self.button21.Bind(wx.EVT_BUTTON, self.on_button21)
                self.button22 = wx.Button(self, label='2. Double Portail Captif' , pos = (int((self.x/2)+self.x-xbsize/2),int((self.height/4)+100)), size=(xbsize,ybsize))
                self.button22.Bind(wx.EVT_BUTTON, self.on_button22)
                self.button23 = wx.Button(self, label='3. Portail Captif Légitime' , pos = (int((self.x/2)+self.x-xbsize/2),int((self.height/4)+200)), size=(xbsize,ybsize))
                self.button23.Bind(wx.EVT_BUTTON, self.on_button23)
                self.button7 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+7), style = wx.BORDER_NONE)
                self.button7.Bind(wx.EVT_BUTTON, self.infosc21)
                self.button7.SetBitmap(self.info)
                self.button8 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+107), style = wx.BORDER_NONE)
                self.button8.Bind(wx.EVT_BUTTON, self.infosc22)
                self.button8.SetBitmap(self.info)
                self.button9 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+207), style = wx.BORDER_NONE)
                self.button9.Bind(wx.EVT_BUTTON, self.infosc23)
                self.button9.SetBitmap(self.info)
            
    def on_button3(self, event):
        if self.on == 0:
            print('Scénario 3 RIP : '+self.fapname.GetValue())
            if self.fapname.GetValue() == "":
                self.ShowWarning()
            else:
                self.ShowWarning()
            
    def on_button4(self, event):
        if self.on == 0:
            if self.fapname.GetValue() == "":
                self.ShowWarning()
            else:
                self.on = 1
                self.step = 1
                self.fap = self.fapname.GetValue()
                self.fapname.Destroy()
                fontname = wx.Font(15, wx.NORMAL, wx.ITALIC, wx.BOLD)
                x = int(self.width/2 + self.width/4 - 12*(len(self.fap)/2))
                self.name = wx.StaticText(self, pos = (x,60), size=(200,40) , label = self.fap)
                self.name.SetForegroundColour('white')
                self.name.SetFont(fontname)
                cmd="sudo sed -i -r \"s/^(fap_name=).*/fap_name=\\\""+self.fap+"\\\"/g\" scriptgraphic.sh"
                os.system(cmd)
                if self.checked == 0:
                    cmd="sudo ./scriptgraphic.sh 4 "
                    os.system(cmd)
                    self.active.Destroy()
                    self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="ACTIF")
                    self.active.SetForegroundColour('green')
                    self.ShowSuccess()
                else:
                    cmd="sudo ./scriptgraphic.sh r 4 "
                    os.system(cmd)
                    self.ShowReboot()
            
    def on_button21(self, event):
        if self.on == 0:
            self.on = 1
            if self.checked == 0:
                cmd="sudo ./scriptgraphic.sh 2 0 1"
                os.system(cmd)
                os.system("sudo gnome-terminal -- python3 sc2/dnsserver.py")
                os.system("sudo service isc-dhcp-server start")
                self.active.Destroy()
                self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="ACTIF")
                self.active.SetForegroundColour('green')
                self.ShowSuccess()
            else:
                cmd="sudo ./scriptgraphic.sh r 2 0 1"
                os.system(cmd)
                self.ShowReboot()
        
    def on_button22(self, event):
        if self.on == 0:
            self.on = 1
            if self.checked == 0:
                cmd="sudo ./scriptgraphic.sh 2 0 2"
                os.system(cmd)
                os.system("sudo gnome-terminal -- python3 sc2/dnsserver.py")
                os.system("sudo service isc-dhcp-server start")
                self.active.Destroy()
                self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="ACTIF")
                self.active.SetForegroundColour('green')
                self.ShowSuccess()
            else:
                cmd="sudo ./scriptgraphic.sh r 2 0 2"
                os.system(cmd)
                self.ShowReboot()
        
    def on_button23(self, event):
        if self.on == 0:
            self.on = 1
            self.step = 3
            self.button21.Destroy()
            self.button22.Destroy()
            self.button23.Destroy()
            self.button7.Destroy()
            self.button8.Destroy()
            self.button9.Destroy()
            xbsize=200
            ybsize=50
            self.log = wx.StaticText(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)-20)), size=(200,40) , label ="Identifiant :")
            self.log.SetFont(self.font)
            self.login = wx.TextCtrl(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4))), size=(140,40))
            self.passwd = wx.StaticText(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)+80)), size=(200,40) , label ="Mot de passe :")
            self.passwd.SetFont(self.font)
            if self.checked == 0:
                self.log.SetForegroundColour('white')
                self.passwd.SetForegroundColour('white')
            else:
                self.log.SetForegroundColour('black')
                self.passwd.SetForegroundColour('black')
            self.password = wx.TextCtrl(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)+100)), size=(140,40), style=wx.TE_PASSWORD)
            self.button233 = wx.Button(self, label='Valider' , pos = (int((self.x/2)+self.x-xbsize/2),int((self.height/4)+200)), size=(xbsize,ybsize))
            self.button233.Bind(wx.EVT_BUTTON, self.on_button233)
    
    def on_button233(self, event):
        if self.login.GetValue() == "" or self.password.GetValue() == "":
            self.ShowIDS()
        else:
            self.step=4
            self.logvalue = self.login.GetValue()
            self.passvalue = self.password.GetValue()
            self.login.Destroy()
            self.password.Destroy()
            self.button233.Destroy()
            self.passwd.Destroy()
            self.logged = wx.StaticText(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)+10)), size=(200,40) , label =self.logvalue)
            if self.logged == 0:
                self.logged.SetForegroundColour('black')
            else:
                self.logged.SetForegroundColour('white')
            self.logged.SetFont(self.font)
            if self.checked == 0:
                cmd="sudo ./scriptgraphic.sh 2 0 3 "+self.logvalue+" "+self.passvalue
                os.system(cmd)
                os.system("sudo gnome-terminal -- python3 sc2/dnsserver.py")
                os.system("sudo service isc-dhcp-server start")
                self.active.Destroy()
                self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="ACTIF")
                self.active.SetForegroundColour('green')
                self.ShowSuccess()
            else:
                cmd="sudo ./scriptgraphic.sh r 2 0 3 "+self.logvalue+" "+self.passvalue
                os.system(cmd)
                self.ShowReboot()
            
    def on_button5(self, event):
        self.frame = MySdFrame(parent=self, title="Logs")
        self.frame.Show()
    
    def on_button6(self, event):
        if self.step == 1:
            self.step = 0
            self.name.Destroy()
            self.fapname = wx.TextCtrl(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)-85)), size=(140,40))
            os.system("sudo ./stop.sh")
            self.active.Destroy()
            self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="INACTIF")
            self.active.SetForegroundColour('red')
        elif self.step == 2:
            self.name.Destroy()
            self.button21.Destroy()
            self.button22.Destroy()
            self.button23.Destroy()
            self.button7.Destroy()
            self.button8.Destroy()
            self.button9.Destroy()
        elif self.step == 3:
            self.name.Destroy()
            self.login.Destroy()
            self.log.Destroy()
            self.passwd.Destroy()
            self.password.Destroy()
            self.button233.Destroy()
        elif self.step ==4:
            self.name.Destroy()
            self.logged.Destroy()
            self.log.Destroy()
        if self.step == 2 or self.step == 3 or self.step == 4:
            self.step = 0
            self.active.Destroy()
            self.active = wx.StaticText(self, pos = (int((self.x/2)-30),370), size=(200,40) , label ="INACTIF")
            self.active.SetForegroundColour('red')
            self.button = wx.Button(self, label='1. Point d\'accès' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4))), size=(self.xbsize,self.ybsize))
            self.button.Bind(wx.EVT_BUTTON, self.on_button1)
            self.button2 = wx.Button(self, label='2. Portail Captif' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+100)), size=(self.xbsize,self.ybsize))
            self.button2.Bind(wx.EVT_BUTTON, self.on_button2)
            self.button3 = wx.Button(self, label='3. Attaque Karma' , pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+200)), size=(self.xbsize,self.ybsize))
            self.button3.Bind(wx.EVT_BUTTON, self.on_button3)
            self.button4 = wx.Button(self, label='4. DNS Spoofing', pos = (int((self.x/2)+self.x-self.xbsize/2),int((self.height/4)+300)), size=(self.xbsize,self.ybsize))
            self.button4.Bind(wx.EVT_BUTTON, self.on_button4)
            self.fapname = wx.TextCtrl(self, pos = (int((self.x/2)+self.x-140/2),int((self.height/4)-85)), size=(140,40))
            self.button7 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+7), style = wx.BORDER_NONE)
            self.button7.Bind(wx.EVT_BUTTON, self.infosc1)
            self.button7.SetBitmap(self.info)
            self.button8 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+107), style = wx.BORDER_NONE)
            self.button8.Bind(wx.EVT_BUTTON, self.infosc2)
            self.button8.SetBitmap(self.info)
            self.button9 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+207), style = wx.BORDER_NONE)
            self.button9.Bind(wx.EVT_BUTTON, self.infosc3)
            self.button9.SetBitmap(self.info)
            self.button10 = wx.Button(self, size = (40,40), pos=(int((self.x/2)+self.x-self.xbsize/2) + 210 , int((self.height/4))+307), style = wx.BORDER_NONE)
            self.button10.Bind(wx.EVT_BUTTON, self.infosc4)
            self.button10.SetBitmap(self.info)
            if self.on == 1:
                os.system("sudo ./stop.sh")
        self.on = 0
            
    def infosc1(self, event):
        wx.MessageBox('Le scénario 1 mettra en place un point d\'accès wifi sans restrictions où vous pourrez récupérer les trames réseaux (exploitables sur Wireshark).', 'Scénario 1', wx.OK | wx.ICON_INFORMATION)
    
    def infosc2(self, event):
        wx.MessageBox('Le scénario 2 mettra en place un point d\'accès wifi avec l\'obligation de se connecter à un portail captif. Vous allez récupérer: \n- les identifiants saisis sur le portail captif\n- les sites consultés\n- les trames réseaux (exploitables sur Wireshark)', 'Scénario 2', wx.OK | wx.ICON_INFORMATION)
    
    def infosc21(self, event):
        wx.MessageBox('Ce scénario fera apparaître un portail captif lors de la connexion au wifi. Les identifiants saisis valideront la connexion à la première tentative (qu\'ils soient bons ou mauvais). Vous allez récupérer: \n- les identifiants saisis sur le portail captif\n- les sites consultés\n- les trames réseaux (exploitables sur Wireshark)', 'Simple portail captif', wx.OK | wx.ICON_INFORMATION)
        
    def infosc22(self, event):
        wx.MessageBox('Ce scénario fera apparaître un portail captif lors de la connexion au wifi. Les identifiants saisis valideront la connexion au bout de la deuxième tentative (qu\'ils soient bons ou mauvais). Vous allez récupérer: \n- les identifiants saisis sur le portail captif\n- les sites consultés\n- les trames réseaux (exploitables sur Wireshark)', 'Double portail captif', wx.OK | wx.ICON_INFORMATION)
        
    def infosc23(self, event):
        wx.MessageBox('Ce scénario fera apparaître un portail captif lors de la connexion au wifi. Les identifiants saisis seront vérifiés sur le vrai portail captif SystemeU. On vous demandera de saisir vos identifiants pour vous reconnecter au vrai portail captif (afin que vous ayez toujours une connexion). Vous allez récupérer: \n- les identifiants saisis sur le portail captif\n- les sites consultés\n- les trames réseaux (exploitables sur Wireshark)', 'Portail captif légitime', wx.OK | wx.ICON_INFORMATION)
        
    def infosc3(self, event):
        wx.MessageBox('NOT YET', 'Scénario 3', wx.OK | wx.ICON_INFORMATION)
    
    def infosc4(self, event):
        wx.MessageBox('Le scénario 4 mettra en place un point d\'accès wifi sans restrictions, cependant lorsque les clients du wifi accèderont à une page en HTTP, une fausse page de connexion Google s\'affichera pour qu\'ils se connectent. Vous allez récupérer: \n- les identifiants saisis sur la page Google\n- les trames réseaux (exploitables sur Wireshark).', 'Scénario 4', wx.OK | wx.ICON_INFORMATION)
        
    def ShowWarning(self):
        wx.MessageBox('Nom de Wifi null ou invalide', 'Info', wx.OK | wx.ICON_ERROR)
        
    def ShowSuccess(self):
        wx.MessageBox('Votre point d\'accès est lancé avec le nom : '+self.fap, 'Success', wx.OK | wx.ICON_INFORMATION)
    
    def ShowIDS(self):
        wx.MessageBox('Champ d\'identifiant ou de mot de passe null', 'Attention', wx.OK | wx.ICON_INFORMATION)
    
    def ShowReboot(self):
        wx.MessageBox('Votre point d\'accès sera visible au redémarrage avec le nom : '+self.fap, 'Attention', wx.OK | wx.ICON_INFORMATION)
        
class MyResultPanel(wx.Panel):
    def __init__(self,parent):
        super(MyResultPanel,self).__init__(parent)
        self.search = wx.TextCtrl(self, pos = (50,50), size=(140,40),style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER,self.search_data)
        
        self.clear = wx.Button(self, label='Effacer TOUS les logs', pos = (270,510), size=(60,40))
        self.clear.Bind(wx.EVT_BUTTON, parent.ClearLogs)
        
        self.mygrid = grid.Grid(self)

        self.print_data()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search, 1, wx.EXPAND)
        sizer.Add(self.clear, 1, wx.EXPAND)
        sizer.Add(self.mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def search_data(self, event):

        text = self.search.GetValue()

        f = open("/var/www/log.txt", "r")
        index = 0 
        nb_ligne_grid_searched = 0
        list_trouve = []
        for i in f.readlines() : 
            if text.lower() in i.lower() : 
                # print(i)
                list_trouve.append(i)
                nb_ligne_grid_searched += 1

        if nb_ligne_grid_searched != 0 : 
            self.mygrid.DeleteRows(0,self.nb_ligne_grid)
            self.nb_ligne_grid = nb_ligne_grid_searched
            self.mygrid.AppendRows(self.nb_ligne_grid)


            for i in list_trouve : 
                tab = i.split("|")
                self.mygrid.SetCellValue(index,0,tab[0])        
                self.mygrid.SetReadOnly(index, 0)
                for j in range(1, 6):
                    value = tab[j].split(" : ")
                    self.mygrid.SetCellValue(index,j,value[1])    
                    self.mygrid.SetReadOnly(index, j)      
                index+=1       

        else : 
            self.search.SetValue("")
            wx.MessageBox('Aucun Resultat', 'Info', wx.OK | wx.ICON_ERROR)
        
    def print_data(self):
        f = open("/var/www/log.txt", "r")
        self.nb_ligne_grid = len(f.readlines())  
        if self.nb_ligne_grid <= 30:
            self.mygrid.CreateGrid(30,6)
        else:
            self.mygrid.CreateGrid(self.nb_ligne_grid,6)
        self.mygrid.SetColLabelValue(0, "Date")
        self.mygrid.SetColSize(0, 170)
        self.mygrid.SetColLabelValue(1, "IP")
        self.mygrid.SetColSize(1, 110)
        self.mygrid.SetColLabelValue(2, "MAC")
        self.mygrid.SetColSize(2, 150)
        self.mygrid.SetColLabelValue(3, "Login")
        self.mygrid.SetColSize(3, 150)
        self.mygrid.SetColLabelValue(4, "Password")
        self.mygrid.SetColSize(4, 150)
        self.mygrid.SetColLabelValue(5, "Machine")
        self.mygrid.SetColSize(5, 250)

        f.close()
        f = open("/var/www/log.txt", "r")
        index = 0
        for i in f.readlines() : 
            tab = i.split("|")
            self.mygrid.SetCellValue(index,0,tab[0])        
            self.mygrid.SetReadOnly(index, 0)
            for j in range(1, 6):
                value = tab[j].split(" : ")
                self.mygrid.SetCellValue(index,j,value[1])    
                self.mygrid.SetReadOnly(index, j)      
            index+=1
        if index <= 30:
            for i in range(index, 30):
                self.mygrid.SetCellValue(index,0,"")        
                self.mygrid.SetReadOnly(index, 0)
                for j in range(1, 6):
                    self.mygrid.SetCellValue(index,0,"")        
                self.mygrid.SetReadOnly(index, 0)
                index+=1
        
            
        f.close()
                    
            
class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#ECECEC')

class RightPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#054867') #054867

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Fake Access Point', pos=(600,150),size=(700,600), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        panel = MyPanel(self)
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    
    def OnClose(self, event):
        os.system("sudo ./stop.sh")
        wx.Exit()

class MySdFrame(wx.Frame):
    def __init__(self, parent,title):
        super(MySdFrame, self).__init__(parent,title=title,pos =(650,200), size=(1000,600))
        self.panel = MyResultPanel(self) 
        self.parent = parent
    def ClearLogs(self, event):
        r = wx.MessageBox('Voulez-vous vraiment effacer tous les logs ? ', 'Attention',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if r == 2:
            os.system("sudo rm /var/www/log.txt")
            os.system("sudo touch /var/www/log.txt")
            os.system("sudo chmod 646 /var/www/log.txt")
            wx.MessageBox('Tous les logs ont été effacés.', 'Attention', wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            wx.MessageBox('Opération annulée, les logs n\'ont pas été effacés.', 'Attention', wx.OK | wx.ICON_INFORMATION)
        
if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = MyFrame()
    app.MainLoop()


