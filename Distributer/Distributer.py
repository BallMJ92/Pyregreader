import re, os
class ClientDistributer:

    def ReadCSVFile(self, file):
        hosts = []
        with open(file, 'r') as csvlist:
            for x in csvlist:
                hosts.append(x)

        splitelement = re.compile('\n').split
        self.hostlist = [part for listElement in hosts for part in splitelement(listElement) if part]

    def CommandTests(self):
        #iterates over the hostlist variable and runs command
        for hosts in self.hostlist:
            try:
                # Below required files to be copied from Receiver host machine to all required clients using 'r copy'
                sendMsvdll = (r'copy C:\Windows\System32\msvcp140.dll \\%s\c$\\Windows\System32\msvcp140.dll' % (hosts))
                sendVcruntime = (r'copy C:\Windows\System32\vcruntime140.dll \\%s\c$\\Windows\System32\vcruntime140.dll' % (hosts))
                sendProgram = (r'xcopy C:\Users\mball\Desktop\PythonSoftware\Client\* \\%s\c$\programdata\ /e /i' % (hosts))
                sendShortcut = (r'copy C:\Users\mball\Desktop\PythonSoftware\Shortcuts\Client.lnk "\\%s\c$\\programdata\microsoft\windows\start menu\programs\startup\Client.lnk"' % (hosts))
            except OSError as e:
                print("Error sending files to %s" % (hosts))
                wait = input("Press enter to exit...")

            """
            Do not run following command unless script is live - 
            """
            os.system(sendMsvdll)
            os.system(sendVcruntime)
            os.system(sendProgram)
            os.system(sendShortcut)

            print(sendMsvdll)
            print(sendVcruntime)
            print(sendProgram)
            print (sendShortcut)
            print("----------")
        wait = input("Press enter to exit...")

    def main(self):
        CSVFileName = ("hostnames.csv")
        self.ReadCSVFile(CSVFileName)
        self.CommandTests()

if __name__ == "__main__":
    ReadCSV = ClientDistributer()
    ReadCSV.main()
