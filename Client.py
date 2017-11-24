import errno, os, winreg, socket
from time import gmtime, strftime

class installedSoftwareAuditor():

    def currentTime(self):
        self.dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        #print(dateTime)

    def getHostname(self):
        self.host = socket.gethostname()

    def readRegistry(self):
        self.regprograms = []
        keywords = ['Service Pack', 'C++', 'SQL', 'Intel', 'HP', 'Microsoft'] # Keywords to ignore in self.regprograms list
        self.regprograms.append(self.dateTime)
        self.regprograms.append(self.host)
        self.regprograms.append(self.sophosLastUpdate)

        try:
            environment = os.environ['PROCESSOR_ARCHITECTURE'].lower()
            environment64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
        except:
            pass
        if environment == 'x86' and not environment64:
            environment_keys = {'0'}
        elif environment == 'x86' or environment == 'amd64':
            environment_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled architecture %s" % environment)

        #Check last logged on user
        for environment_key in environment_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI", 0, winreg.KEY_READ | environment_key)
            try:
                self.regprograms.append(str((winreg.QueryValueEx(key, 'LastLoggedOnUser')[0])))
            except OSError as e:
                if e.errno == errno.ENOENT:
                    pass
            finally:
                key.Close()

        #model
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS", 0, winreg.KEY_READ | environment_key)
        try:
            self.regprograms.append(str((winreg.QueryValueEx(key, 'SystemManufacturer')[0]))+" "+((winreg.QueryValueEx(key, 'SystemProductName')[0])))
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
        finally:
            key.Close()

        #Gather list of all installed software
        for environment_key in environment_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | environment_key)
            for x in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, x)
                skey = winreg.OpenKey(key, skey_name)
                try:
                    self.programs = str(winreg.QueryValueEx(skey, 'DisplayName')[0]+" (Version: "+str(winreg.QueryValueEx(skey, 'DisplayVersion')[0])+")")
                    if not any(k in self.programs for k in keywords):
                        self.regprograms.append(self.programs)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        pass
                finally:
                    skey.Close()

    def SophosUpdate(self):
        #directory path of log files
        path = ("C:\\ProgramData\\Sophos\\AutoUpdate\\Logs\\")
        #listing all files within path
        try:
            directory = os.listdir(path)
            if path is False:
                self.sophosLastUpdate = ("Sophos not installed")
        except OSError as x:
            if x.errno == errno.ENOENT:
                pass
        #iterating over files in path and checking if specific log file name appears
        paths = [os.path.join(path, basename) for basename in directory if "ALUpdate" in basename]
        #getting the name of the last modified file and assigning it to a variable
        latest = (max(paths, key=os.path.getctime))
        #print(latest)

        self.sophosLastUpdate = (latest[52:54] + "/" + latest[50:52] + "/" + latest[46:50])
        #print(self.sophosLastUpdate)

    def portSender(self):
        IP = '172.19.2.1' # IP associated with CYJQJG2 which hosts the Receiver
        PORT = 5000
        installedprograms = ('\n'.join(map(str, self.regprograms)))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(installedprograms.encode(), (IP, PORT))

    def main(self):
        self.currentTime()
        self.getHostname()
        self.SophosUpdate()
        self.readRegistry()
        self.portSender()

if __name__ == "__main__":
    auditor = installedSoftwareAuditor()
    auditor.main()
