#!/usr/bin/python
import os, subprocess
username = subprocess.run(['whoami'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')

def is_installed(prog):
    path = subprocess.run(['which',prog], stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n','')
    return [True,path] if path != '' else False

def rm_line(live_file,txt):
    with open(live_file, 'r') as f:
        lines = f.readlines()
        with open(live_file, 'w') as f:
            for line in lines:
                if line.strip("\n") != txt: f.write(line)
def create_file(filename, sudopower=False):
    os.system("sudo touch "+filename) if sudopower == True else os.system("touch "+filename)
def remove_file(filename, sudopower=False):
    os.system("sudo rm "+filename) if sudopower == True else os.system("rm "+filename)
def create_folder(foldername,sudopower=False):
    os.system('sudo mkdir -p '+foldername) if sudopower == True else os.system('mkdir -p '+foldername)
def remove_folder(foldername,recursive=False,sudopower=False):
    if sudopower == True: os.system("sudo rm -rf "+foldername) if recursive == True else os.system("sudo rmdir "+foldername)
    elif recursive == True: os.system("rm -rf "+foldername)
    else: os.system("rmdir "+foldername)
def add_line_if_not_exist(alfile, txtlist, checkerline):
    retmsg = []
    if checkerline in open(alfile).read(): retmsg.append("Already Present !")
    else:
        f = open(alfile,'a+')
        for txt in txtlist:
            retmsg.append(txt)
            txt = txt+"\n"
            f.write(txt)
        f.close()
    return retmsg
def s_Modules_initializer():
    s_text = ['','### MY_S_BIN INIT ###','export PATH=~/s/bin/:$PATH','### MY_S_BIN INIT ###','']
    for msg in add_line_if_not_exist('/home/'+username+'/.bashrc',s_text,'export PATH=~/s/bin/:$PATH'): print(msg)
def re_co_un(rcu):
    d = ['Re-install','Configure','Uninstall','Abort (Exit)']
    patterns = ['rc','ru','rcu','c','r']
    dict = {'rc':[d[0],d[1]],'ru':[d[0],d[2]],'rcu':[d[0],d[1],d[2]],'c':[d[1]],'r':[d[0]]}
    counter = 1
    choice = []
    for pattern in patterns:
        if pattern == rcu: choice = dict[pattern]

    choice.append(d[3])
    for c in choice:
        print("{} - {}".format(counter,c))
        counter = counter + 1

    a = input()
    if a == "1" or a == "2" or a == "3" or a == "4":
        a = int(a)
        if a == len(choice):
            print("\n :: Process Aborted !!!")
            quit()
        elif a > len(choice):
            print("Wrong Input !\n :: Aborting !!!")
            quit()
        elif a <= len(choice):
            return choice[a-1][0:1].lower()
    else:
        print("Wrong Input !\n :: Aborting !!!")
        quit()

def installer(script):
    pNAME = script['pINFO']['name']
    rcu = script['pINFO']['rcu']
    iCONF = script['pINFO']['iCONF']
    eMSG = script['pINFO']['eMSG']
    rMTD = script['rMTD']
    cMTD = script['cMTD']
    uMTD = script['uMTD']
    rCMDs = script['rCMDs']
    cCMDs = script['cCMDs']
    uCMDs = script['uCMDs']
    def cmds_installer(cmds):
        if cmds != False:
            for cmd in cmds: os.system(cmd)

    def install_prog():
        rMTD() if rMTD != False else cmds_installer(rCMDs)
        if iCONF != False:
            cMTD() if cMTD != False else cmds_installer(cCMDs)
        if eMSG != False: print(eMSG)

    if is_installed(pNAME) != False:
        print("\n :: {} is Already Installed >>> {}\n".format(pNAME.upper(),is_installed(pNAME)[1]))
        b = re_co_un(rcu)
        if b == 'r': install_prog()
        elif b == 'c':
            cMTD() if cMTD != False else cmds_installer(cCMDs)
        elif b == 'u':
            uMTD() if uMTD != False else cmds_installer(uCMDs)
            print("\n :: {} Uninstalled !".format(pNAME.upper()))
    else: install_prog()

### mpv
def configure_mpv():
    conf_path = '/home/'+username+'/.config/mpv'
    create_folder(conf_path)
    conf_file = open(conf_path+"/input.conf","w+") # Because MPV Don't Create This File after Installation !
    conf_file.close()
    c = [' seek ','Alt+',' add video-pan-x ',['right','left','down','up'],['0.1','-0.1','0.1','-0.1'],['h','g','b','y']]
    conf = ['# mpv keybindings','', '## Seek units are in seconds','h'+c[0]+'5','g'+c[0]+'-5','y'+c[0]+'30','b'+c[0]+'-30','','# Move video rectangle']
    for v in range(4):
        conf.append("{}{}{}{}".format(c[1],c[3][v],c[2],c[4][v]))
        conf.append("{}{}{}{}".format(c[1],c[5][v],c[2],c[4][v]))
    for msg in add_line_if_not_exist(conf_path+"/input.conf",conf,conf[0]): print(msg)

mpv_script = {
    'pINFO':{'name':'mpv','rcu':'rcu','iCONF':True,'eMSG':False},
    'rMTD':False,'cMTD':configure_mpv,'uMTD':False,
    'rCMDs':['rm -rf /home/'+username+'/.config/mpv','sudo pacman -S mpv'],'cCMDs':False,
    'uCMDs':['rm -rf /home/'+username+'/.config/mpv','sudo pacman -R mpv']
    }

### youtube-dl
youtubedl_script = {
    'pINFO':{'name':'youtube-dl','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl',
            'sudo chmod a+rx /usr/local/bin/youtube-dl'],'cCMDs':False,'uCMDs':['sudo rm -rf /usr/local/bin/youtube-dl']
    }

### lampp
xampp_script = {
    'pINFO':{'name':'lampp','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo ./.xampp/xampp-linux-x64-7.3.1-0-installer.run',
             'cd '+is_installed('ls')[1][:-3]+' && sudo ln -sf /opt/lampp/xampp lampp'],'cCMDs':False,
    'uCMDs':['cd /opt/lampp && ./uninstall','cd '+is_installed('ls')[1][:-3]+' && sudo rm -rf lampp']
    }

### git
def configure_git():
    print("Enter Your Email: ")
    git_email = input()
    print("Enter Your Username: ")
    git_username = input().replace(" ",'')
    conf_file = open('/home/'+username+'/.gitconfig',"w+")
    conf_file.close()
    os.system("git config --global user.email "+git_email)
    os.system("git config --global user.name "+git_username)
    os.system("less /home/"+username+"/.gitconfig")
    print("\n :: Git Configured Successfully !")

git_script = {'pINFO':{'name':'git','rcu':'c','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':configure_git,'uMTD':False,'rCMDs':False,'cCMDs':False,'uCMDs':False}

### emacs
def configure_emacs():
    conf_text = ['(custom-set-variables',' ;; custom-set-variables was added by Custom.',
                 ' ;; If you edit it by hand, you could mess it up, so be careful.',
                 ' ;; Your init file should contain only one such instance.',
                 ' ;; If there is more than one, they won\'t work right.',
                 ' \'(inhibit-startup-screen t))','(custom-set-faces',
                 ' ;; custom-set-faces was added by Custom.',
                 ' ;; If you edit it by hand, you could mess it up, so be careful.',
                 ' ;; Your init file should contain only one such instance.',
                 ' ;; If there is more than one, they won\'t work right.',' )']

    print("Never Create Backup~ files? (y/n)")
    abf = input()
    print("Never Create #autosave# files? (y/n)")
    acasf = input()
    conf_file = open('/home/'+username+'/.emacs','w+')

    for conf in conf_text:
        conf = conf+"\n"
        conf_file.write(conf)

    if abf == "y" or abf == "Y": conf_file.write("(setq make-backup-files nil) ; stop creating backup~ files\n")

    if acasf == "y" or acasf == "Y": conf_file.write("(setq auto-save-default nil) ; stop creating #autosave# files\n")
    conf_file.close()
    os.system("less /home/"+username+"/.emacs")
    print("Emacs Configured Successfully !")

emacs_script = {
    'pINFO':{'name':'emacs','rcu':'rcu','iCONF':True,'eMSG':False},
    'rMTD':False,'cMTD':configure_emacs,'uMTD':False,
    'rCMDs':['sudo pacman -S emacs'],'cCMDs':False,'uCMDs':['sudo pacman -R emacs']
    }

### xdman
xdman_script = {
    'pINFO':{'name':'xdman','rcu':'ru','iCONF':False,'eMSG':"\n :: XDMAN Installed !"},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo ./.xdm/install.sh'],'cCMDs':False,'uCMDs':['sudo /opt/xdman/uninstall.sh']
    }

## Chromium
chromium_script = {
    'pINFO':{'name':'chromium','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo pacman -S chromium'],'cCMDs':False,'uCMDs':['sudo pacman -R chromium']
    }

## feh
feh_script = {
    'pINFO':{'name':'feh','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo pacman -S feh'],'cCMDs':False,'uCMDs':['sudo pacman -R feh']
    }

## go lang
def configure_go():
    init_text = ['','### GO_LANG INIT ###','export GOROOT=/usr/local/go','export GOPATH=$HOME/s/Work/go',
                 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH','### GO_LANG INIT ###','']
    add_line_if_not_exist("/home/"+username+"/.bashrc",init_text,init_text[2])
    os.system("cat /home/"+username+"/.bashrc")

def go_inst_cmds():
    print("Removing Previous Configurations...")
    go_uninstall()
    print("Installing New files...")
    junky = '/home/'+username+'/H__GO_INSTALLER__H'
    os.system('mkdir -p '+junky)
    os.system("tar -xzvf ./.go/go1.11.5.linux-amd64.tar.gz -C "+junky+'/')
    os.system('rm -rf '+junky+'/gocache '+junky+'/tmp')
    os.system('sudo mv '+junky+'/go /usr/local/')
    os.system('rmdir '+junky)
    print("Initializing...")
    configure_go()

def go_uninstall():
    rm_line('/home/'+username+'/.bashrc',"### GO_LANG INIT ###")
    rm_line('/home/'+username+'/.bashrc',"export GOROOT=/usr/local/go")
    rm_line('/home/'+username+'/.bashrc',"export GOPATH=$HOME/s/Work/go")
    rm_line('/home/'+username+'/.bashrc',"export PATH=$GOPATH/bin:$GOROOT/bin:$PATH")
    os.system("sudo rm -rf /usr/local/go")

go_script = {
    'pINFO':{'name':'go','rcu':'rcu','iCONF':True,'eMSG':"\n :: Go is installed, Restart Terminal and Verify\n :: $ go version\n :: $ go env"},
    'rMTD':go_inst_cmds,'cMTD':configure_go,'uMTD':go_uninstall,
    'rCMDs':False,'cCMDs':False,'uCMDs':False
    }

### atom
def apm_install(plugin):
    print("Install "+plugin+" Plugin? (y/n)")
    a = input()
    if a == "y" or a == "Y":
        print(":: Please Wait... This can Take Several Minutes")
        os.system("apm i "+plugin)

def atom_plugins():
    apm_install('atomic-emacs')
    apm_install('atom-beautify')

atom_script = {
    'pINFO':{'name':'atom','rcu':'rcu','iCONF':True,'eMSG':False},
    'rMTD':False,'cMTD':atom_plugins,'uMTD':False,
    'rCMDs':['sudo pacman -S atom'],'cCMDs':False,'uCMDs':['sudo pacman -R atom']
    }

### Anaconda
def configure_conda():
    print("Auto Activate base? (y/n)")
    aab = input()
    if aab == "y" or aab == "Y":
        os.system("conda config --set auto_activate_base true")
    elif aab == "n" or aab == "N":
        os.system("conda config --set auto_activate_base false")
    print("\n :: Restart Your Terminal !")

conda_script = {
    'pINFO':{'name':'conda','rcu':'rc','iCONF':False,'eMSG':"\n :: Restart Your Terminal !"},
    'rMTD':False,'cMTD':configure_conda,'uMTD':False,
    'rCMDs':["bash ./.anaconda/Anaconda3-2019.03-Linux-x86_64.sh"],'cCMDs':False,'uCMDs':False
    }

# GEANY
geany_script = {
    'pINFO':{'name':'geany','rcu':'r','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':["mkdir -p /home/"+username+"/JUNKY_INSTALLER__E",
            "tar -xzvf .geany/geany-1.35.tar.gz -C /home/"+username+"/JUNKY_INSTALLER__E/",
            "cd /home/"+username+"/JUNKY_INSTALLER__E/geany-1.35 && ./configure && make && sudo make install",
            "rm -rf /home/"+username+"/JUNKY_INSTALLER__E"],'cCMDs':False,'uCMDs':False}

# Audacity
audacity_script = {
    'pINFO':{'name':'audacity','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo pacman -S audacity'],'cCMDs':False,'uCMDs':['sudo pacman -R audacity']
    }

### PPSSPP
def ppsspp_inst_cmds():
    psp_path = '/home/'+username+'/s/MY_OPT/PPSSPP'
    os.system("mkdir -p "+psp_path)
    os.system('mkdir -p /home/'+username+'/s/bin')
    os.system('cp ./.ppsspp/ppsspp_amd64.zip ./.ppsspp/launcher.sh '+psp_path+'/')
    os.system('cd '+psp_path+' && unzip ppsspp_amd64.zip && rm ppsspp_amd64.zip')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/PPSSPP/launcher.sh PPSSPP')
    print("initializing s_Module!")
    s_Modules_initializer()

ppsspp_script = {'pINFO':{'name':'PPSSPP','rcu':'ru','iCONF':False,'eMSG':"\n :: PPSSPP Installed !\n :: Restart Your Terminal !"},
    'rMTD':ppsspp_inst_cmds,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':["rm /home/"+username+"/s/bin/PPSSPP","rm -rf /home/"+username+"/s/MY_OPT/PPSSPP"]}

### HEROKU
def heroku_inst_cmds():
    os.system('mkdir -p /home/'+username+'/s/MY_OPT')
    os.system('mkdir -p /home/'+username+'/s/bin')
    os.system('tar -xzvf ./.heroku/heroku-linux-x64.tar.gz -C /home/'+username+'/s/MY_OPT/')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/heroku/bin/heroku heroku')
    s_Modules_initializer()

heroku_script = {'pINFO':{'name':'heroku','rcu':'ru','iCONF':False,'eMSG':"\n :: Heroku Installed !\n :: Restart Your Terminal !"},
    'rMTD':heroku_inst_cmds,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':['rm -rf /home/'+username+'/s/MY_OPT/heroku','rm /home/'+username+'/s/bin/heroku']}

### Kdenlive
def kdenlive_inst_cmds():
    print("Removing Previous Files ...")
    kdenlive_uninstaller()
    print("Installing New Files ...")
    os.system('mkdir -p /home/'+username+'/s/bin')
    os.system('cp .kdenlive/kdenlive /home/'+username+'/s/bin/')
    os.system('chmod 755 /home/'+username+'/s/bin/kdenlive')
    print("Initializing S Module")
    s_Modules_initializer()
    print("Creating Alias")
    alias_txt = ['','alias kdenlive="kdenlive 1>/dev/null 2>/dev/null &"','']
    for msg in add_line_if_not_exist('/home/'+username+'/.bashrc',alias_txt,alias_txt[1]): print(msg)

def kdenlive_uninstaller():
    os.system('rm /home/'+username+'/s/bin/kdenlive')
    rm_line('/home/'+username+'/.bashrc','alias kdenlive="kdenlive 1>/dev/null 2>/dev/null &"')

kdenlive_script = {
    'pINFO':{'name':'kdenlive','rcu':'ru','iCONF':False,'eMSG':" :: Kdenlive Installed !\n :: Restart Your Terminal !"},
    'rMTD':kdenlive_inst_cmds,'cMTD':False,'uMTD':kdenlive_uninstaller,
    'rCMDs':False,'cCMDs':False,'uCMDs':False
    }

### MongoDB
def mongodb_inst_cmds():
    print("Removing Previous Files ...")
    monogodb_uninstaller()
    print("Installing New Files ...")
    os.system('mkdir -p /home/'+username+'/s/MY_OPT /home/'+username+'/s/bin')
    os.system('sudo mkdir -p /data/db /var/log/mongod')
    os.system('sudo chown -R '+username+':'+username+' /data/db')
    os.system('sudo chown -R '+username+':'+username+' /var/log/mongod')
    os.system('tar -xzvf ./.mongodb/mongodb-linux-x86_64-ubuntu1804-4.0.10.tgz -C /home/'+username+'/s/MY_OPT/')
    os.system('echo -n "#!" > /home/'+username+'/s/MY_OPT/mongodb-linux-x86_64-ubuntu1804-4.0.10/mongod')
    os.system('echo "`which bash`" >> /home/'+username+'/s/MY_OPT/mongodb-linux-x86_64-ubuntu1804-4.0.10/mongod')
    os.system('cat .mongodb/.sense.txt >> /home/'+username+'/s/MY_OPT/mongodb-linux-x86_64-ubuntu1804-4.0.10/mongod')
    os.system('chmod +x /home/'+username+'/s/MY_OPT/mongodb-linux-x86_64-ubuntu1804-4.0.10/mongod')
    os.system('mv /home/'+username+'/s/MY_OPT/mongodb-linux-x86_64-ubuntu1804-4.0.10 /home/'+username+'/s/MY_OPT/mongodb')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/mongodb/bin/mongo mongo')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/mongodb/mongod mongod')
    print("Initializing S Module")
    s_Modules_initializer()

def monogodb_uninstaller():
    os.system('sudo rm -rf /data /var/log/mongod')
    os.system('rm -rf /home/'+username+'/s/MY_OPT/mongodb')
    os.system('rm /home/'+username+'/s/bin/mongo /home/'+username+'/s/bin/mongod')

mongodb_script = {'pINFO':{'name':'mongo','rcu':'ru','iCONF':False,'eMSG':"\n :: MongoDB Installed !\n :: Restart Your Terminal !"},
    'rMTD':mongodb_inst_cmds,'cMTD':False,'uMTD':monogodb_uninstaller,'rCMDs':False,'cCMDs':False,'uCMDs':False}

### Node
def node_inst_cmds():
    print("Removing Previous Files ...")
    node_uninstaller()
    print("Installing New Files ...")
    os.system('mkdir -p /home/'+username+'/s/MY_OPT')
    os.system('tar -xvf ./.node/node-v10.15.1-linux-x64.tar.xz -C /home/'+username+'/s/MY_OPT/')
    os.system('mv /home/'+username+'/s/MY_OPT/node-v10.15.1-linux-x64 /home/'+username+'/s/MY_OPT/node')
    print("Adding To PATH !")
    path_txt = ['','### NODE INIT ###','export PATH=$HOME/s/MY_OPT/node/bin:$PATH','### NODE INIT ###','']
    for msg in add_line_if_not_exist('/home/'+username+'/.bashrc',path_txt,path_txt[2]): print(msg)

def node_uninstaller():
    os.system('rm -rf /home/'+username+'/s/MY_OPT/node')
    rm_line('/home/'+username+'/.bashrc','### NODE INIT ###')
    rm_line('/home/'+username+'/.bashrc','export PATH=$HOME/s/MY_OPT/node/bin:$PATH')

def configure_node():
    print("Install Nodemon? (y/n)")
    nodemon = input()
    if nodemon == 'y' or nodemon == "Y": os.system('cd /home/'+username+'/s/MY_OPT/node/bin && ./npm install -g nodemon')

node_script = {'pINFO':{'name':'node','rcu':'rcu','iCONF':True,'eMSG':"\n :: Node Installed !\n :: Restart Your Terminal"},
    'rMTD':node_inst_cmds,'cMTD':configure_node,'uMTD':node_uninstaller,'rCMDs':False,'cCMDs':False,'uCMDs':False}

# RVM
def rvm_ruby_inst_cmds():
    gpg_key = "gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB"
    print("\n :: If GPG Key Error Occurs\n :: Grab New Key from this URL >>> https://rvm.io/rvm/install\n")
    print(" :: Install Using Existing GPG Key? (y/n)")
    inp = input()
    gpg_lv = False
    if inp == "y" or inp == "Y":
        os.system(gpg_key)
        gpg_lv = True
    else:
        print(" :: GPG Command Look Like this:\n   "+gpg_key+"\n")
        print(" :: Enter New GPG Command:")
        cmd = input()
        if 'gpg --keyserver ' in cmd:
            print("\n >>> Installing New GPG Key: Please Wait...")
            os.system(cmd)
            gpg_lv = True
        else:
            print("\n >>> Invalid Command !!!\n")
            gpg_lv = False
            print("Exiting ... !")

    if gpg_lv == True:
        rvm_text = [" :: Which Version To Install?","  1 - Install RVM (development version)","  2 - Install RVM stable with ruby",
        "  3 - Additionally with rails (poor man's railsinstaller)","  4 - Or with jruby, rails and puma","\n :: Choose [1-4], 2 is default"]
        for rvmt in rvm_text: print(rvmt)

        rvm_rb = input()
        rtn = 0
        if rvm_rb == "1": rtn = 1
        elif rvm_rb == "2": rtn = 2
        elif rvm_rb == "3": rtn = 3
        elif rvm_rb == "4": rtn = 4
        else: rtn = 2
        print(" :: Choosen : {} :: Sure (y/n)".format(rvm_text[rtn]))
        user_rtn_sure = input()
        if user_rtn_sure == 'y' or user_rtn_sure == 'Y':
            if rtn == 1: os.system("\\curl -sSL https://get.rvm.io | bash")
            elif rtn == 2: os.system("\\curl -sSL https://get.rvm.io | bash -s stable --ruby")
            elif rtn == 3: os.system("\\curl -sSL https://get.rvm.io | bash -s stable --rails")
            elif rtn == 4: os.system("\\curl -sSL https://get.rvm.io | bash -s stable --ruby=jruby --gems=rails,puma")

            print("Adding To Path")
            rvm_path_text = ['','# This loads RVM into a shell session.','[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"']
            for msgs in add_line_if_not_exist('/home/'+username+'/.bashrc',rvm_path_text,rvm_path_text[2]): print(msgs)
            print("\n :: RVM Installed !\n :: Restart Your Terminal !")

def rvm_ruby_uninstaller():
    os.system('rvm implode')
    os.system('rm -rf /home/'+username+'/.rvm')
    rm_line('/home/'+username+'/.bashrc','# This loads RVM into a shell session.')
    rm_line('/home/'+username+'/.bashrc','[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"')

rvm_script = {'pINFO':{'name':'rvm','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':rvm_ruby_inst_cmds,'cMTD':False,'uMTD':rvm_ruby_uninstaller,'rCMDs':False,'cCMDs':False,'uCMDs':False}

### Vysor
def vysor_inst_cmds():
    print("Removing Previous Files:")
    os.system('rm /home/'+username+'/s/bin/vysor && rm -rf /home/'+username+'/s/MY_OPT/vysor')
    os.system('mkdir -p /home/'+username+'/s/bin /home/'+username+'/s/MY_OPT')
    os.system('cp -a .vysor /home/'+username+'/s/MY_OPT/vysor')
    os.system('echo -n "#!" > /home/'+username+'/s/MY_OPT/vysor/vysor_launcher')
    os.system('echo "`which bash`" >> /home/'+username+'/s/MY_OPT/vysor/vysor_launcher')
    v_launcher = ['cd ~/s/MY_OPT/vysor','./vysor 1>/dev/null && 2>/dev/null &','exit 0']
    add_line_if_not_exist('/home/'+username+'/s/MY_OPT/vysor/vysor_launcher',v_launcher,v_launcher[1])
    os.system('chmod 755 /home/'+username+'/s/MY_OPT/vysor/*')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/vysor/vysor_launcher vysor')
    print("Initializing S Module")
    s_Modules_initializer()

vysor_script = {
    'pINFO':{'name':'vysor','rcu':'ru','iCONF':False,'eMSG':"\n :: Vysor Installed !\n :: Restart Your Terminal !"},
    'rMTD':vysor_inst_cmds,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':['rm /home/'+username+'/s/bin/vysor','rm -rf /home/'+username+'/s/MY_OPT/vysor']
    }

### Postman
def postman_inst_cmds():
    os.system('rm /home/'+username+'/s/bin/postman && rm -rf /home/'+username+'/s/MY_OPT/Postman')
    os.system('mkdir -p /home/'+username+'/s/bin /home/'+username+'/s/MY_OPT')
    os.system('cd .Postman && tar -xzvf Postman-linux-x64-7.0.6.tar.gz -C /home/'+username+'/s/MY_OPT/')
    os.system('rm /home/'+username+'/s/MY_OPT/Postman/Postman')
    os.system('sudo pacman -S gconf')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/Postman/app/Postman postman')
    s_Modules_initializer()

postman_script = {'pINFO':{'name':'postman','rcu':'ru','iCONF':False,'eMSG':"\n :: Postman Installed !\n :: Restart Your Terminal !"},
    'rMTD':postman_inst_cmds,'cMTD':False,'uMTD':False,'rCMDs':False,'cCMDs':False,
    'uCMDs':['rm /home/'+username+'/s/bin/postman','rm -rf /home/'+username+'/s/MY_OPT/Postman','sudo pacman -R gconf']}

### Robo 3T
def robo3T_inst_cmds():
    os.system('rm /home/'+username+'/s/bin/robo3t && rm -rf /home/'+username+'/s/MY_OPT/robo3T')
    os.system('mkdir -p /home/'+username+'/s/bin /home/'+username+'/s/MY_OPT')
    os.system('cd .robo3T && tar -xzvf robo3t-1.2.1-linux-x86_64-3e50a65.tar.gz -C /home/'+username+'/s/MY_OPT/')
    os.system('mv /home/'+username+'/s/MY_OPT/robo3t-1.2.1-linux-x86_64-3e50a65 /home/'+username+'/s/MY_OPT/robo3T')
    os.system('cd /home/'+username+'/s/bin && ln -sf /home/'+username+'/s/MY_OPT/robo3T/bin/robo3t robo3t')
    s_Modules_initializer()

robo3T_script = {
    'pINFO':{'name':'robo3t','rcu':'ru','iCONF':False,'eMSG':"\n :: Robo3T Installed !\n :: Restart Your Terminal !"},
    'rMTD':robo3T_inst_cmds,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':['rm /home/'+username+'/s/bin/robo3t','rm -rf /home/'+username+'/s/MY_OPT/robo3T']}

### xClip
def xclip_inst_cmds():
    xclip_text = ['','alias xclip="xclip -selection c"','']
    os.system('sudo pacman -S xclip')
    print("Creating Alias !")
    for msg in add_line_if_not_exist('/home/'+username+'/.bashrc',xclip_text,xclip_text[1]): print(msg)

def xclip_uninstaller():
    os.system("sudo pacman -R xclip")
    rm_line('/home/'+username+'/.bashrc','alias xclip="xclip -selection c"')

xclip_script = {
    'pINFO':{'name':'xclip','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':xclip_inst_cmds,'cMTD':False,'uMTD':xclip_uninstaller,'rCMDs':False,'cCMDs':False,'uCMDs':False}

# YDL (Youtube Downloader)
def ydl_inst_cmd():
    os.system("mkdir -p /home/"+username+"/s/bin")
    os.system("rm -rf /home/"+username+"/s/bin/ydl")
    os.system("cd /home/"+username+"/s/bin && git clone https://github.com/electrodragon/ydl.git")
    os.system("mv /home/"+username+"/s/bin/ydl /home/"+username+"/s/bin/ydldir")
    os.system("mv /home/"+username+"/s/bin/ydldir/ydl /home/"+username+"/s/bin/ && rm -rf /home/"+username+"/s/bin/ydldir")
    s_Modules_initializer()

ydl_script = {
    'pINFO':{'name':'ydl','rcu':'ru','iCONF':False,'eMSG':"\n :: Restart Your Terminal"},
    'rMTD':ydl_inst_cmd,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':['rm /home/'+username+'/s/bin/ydl']}

# ytmpv
def ytmpv_inst_cmds():
    os.system("mkdir -p /home/"+username+"/s/bin")
    os.system("rm -rf /home/"+username+"/s/bin/ytmpv")
    os.system("cd /home/"+username+"/s/bin && git clone https://github.com/electrodragon/ytmpv.git")
    os.system("mv /home/"+username+"/s/bin/ytmpv /home/"+username+"/s/bin/ytmpvdir")
    os.system("mv /home/"+username+"/s/bin/ytmpvdir/ytmpv /home/"+username+"/s/bin/ && rm -rf /home/"+username+"/s/bin/ytmpvdir")
    s_Modules_initializer()

ytmpv_script = {
    'pINFO':{'name':'ytmpv','rcu':'ru','iCONF':False,'eMSG':"\n :: Restart Your Terminal"},
    'rMTD':ytmpv_inst_cmds,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':['rm /home/'+username+'/s/bin/ytmpv']}

# scrcpy
scrcpy_script = {
    'pINFO':{'name':'scrcpy','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,'cCMDs':False,'uCMDs':['sudo pacman -R scrcpy'],
    'rCMDs':['mkdir -p /home/'+username+'/__JUNKY_SCRCPY','cd /home/'+username+'/__JUNKY_SCRCPY && git clone \'https://aur.archlinux.org/scrcpy.git\'',
             'cd /home/'+username+'/__JUNKY_SCRCPY/scrcpy && makepkg -Acs PKGBUILD && sudo pacman -U ./*.pkg.tar*','rm -rf /home/'+username+'/__JUNKY_SCRCPY']}

# HANDBRAKE
handbrake_gui_script = {
    'pINFO':{'name':'ghb','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo pacman -S handbrake'],'cCMDs':False,'uCMDs':['sudo pacman -R handbrake']
    }
handbrake_cli_script = {
    'pINFO':{'name':'HandBrakeCLI','rcu':'ru','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['sudo pacman -S handbrake-cli'],'cCMDs':False,'uCMDs':['sudo pacman -R handbrake-cli']
    }

# Virtual Box
vbox_script = {
    'pINFO':{'name':'virtualbox','rcu':'r','iCONF':False,'eMSG':"\n :: Restart Your System !"},'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':['pamac install virtualbox $(pacman -Qsq "^linux" | grep "^linux[0-9]*[-rt]*$" | awk \'{print $1"-virtualbox-host-modules"}\' ORS=\' \')',
    'sudo vboxreload','pamac build virtualbox-ext-oracle','sudo gpasswd -a $USER vboxusers'],'cCMDs':False,'uCMDs':False}

# OpenSSH
def openssh_configure():
    print("\n :: SSH STATUS !\n")
    os.system('sudo systemctl status sshd | grep \'Active:\'')
    a = input("\n :: [s]tart, [e]nable, s[t]op, [d]isable : ")
    if a == 's': os.system('sudo systemctl start sshd')
    elif a == 'e': os.system('sudo systemctl enable sshd')
    elif a == 't': os.system('sudo systemctl stop sshd')
    elif a == 'd': os.system('sudo systemctl disable sshd')
    else:
        print("\n :: Wrong Input !")
        quit()
    os.system('sudo systemctl status sshd | grep \'Active:\'')
    print("\n :: IP\n")
    os.system('ip a | grep -i \'inet 192\'')
    print("\n :: More: https://linuxhint.com/arch_linux_ssh_server")

openssh_script = {
    'pINFO':{'name':'sshd','rcu':'rc','iCONF':True,'eMSG':False},
    'rMTD':False,'cMTD':openssh_configure,'uMTD':False,
    'rCMDs':['sudo pacman -S openssh'],'cCMDs':False,'uCMDs':False
    }

"""
script = {
    'pINFO':{'name':'name','rcu':'rcu','iCONF':False,'eMSG':False},
    'rMTD':False,'cMTD':False,'uMTD':False,
    'rCMDs':False,'cCMDs':False,'uCMDs':False
    }
"""

softwares = []
softwares.append(mpv_script)
softwares.append(youtubedl_script)
softwares.append(xampp_script)
softwares.append(git_script)
softwares.append(emacs_script)
softwares.append(xdman_script)
softwares.append(chromium_script)
softwares.append(feh_script)
softwares.append(go_script)
softwares.append(atom_script)
softwares.append(conda_script)
softwares.append(geany_script)
softwares.append(audacity_script)
softwares.append(ppsspp_script)
softwares.append(heroku_script)
softwares.append(kdenlive_script)
softwares.append(mongodb_script)
softwares.append(node_script)
softwares.append(rvm_script)
softwares.append(vysor_script)
softwares.append(postman_script)
softwares.append(robo3T_script)
softwares.append(xclip_script)
softwares.append(ydl_script)
softwares.append(ytmpv_script)
softwares.append(scrcpy_script)
softwares.append(handbrake_gui_script)
softwares.append(handbrake_cli_script)
softwares.append(vbox_script)
softwares.append(openssh_script)

a = 1
for software in softwares:
    if is_installed(software['pINFO']['name']) == False:
        print("{} - {} \t \t >>> Not Installed --------------".format(a,software['pINFO']['name'].upper()))
    else:
        print("{} - {}".format(a,software['pINFO']['name'].upper()))
    a = a + 1
print("Choose [1 - {}]: ".format(len(softwares)))
choosen = int(input())
if choosen > len(softwares) or choosen < 1:
    print("Wrong Input !")
else:
    print("Choosen : {} :: SURE (y/n)".format(softwares[choosen - 1]['pINFO']['name'].upper()))
    sure = input()
    sure = sure.lower()
    if sure == "y":
        installer(softwares[choosen - 1])
