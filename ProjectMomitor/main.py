from PyQt5 import QtWidgets , QtGui,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from design import Ui_MainWindow
import psutil
import threading
from hurry.filesize import size
import time
import sys
import platform,socket,re,uuid,json,logging
import speedtest

class SystemMonitor(QThread,Ui_MainWindow):
    
    x = pyqtSignal(int)
    def run(self):
        try:
            while True:
                value = psutil.virtual_memory().percent
                self.x.emit(int(value))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting Ram informations")
class ProcessorUI(QThread,Ui_MainWindow):
    
    y = pyqtSignal(int)
    def run(self):
        try:
            while True:
                value = psutil.cpu_percent()
                self.y.emit(int(value))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting Cpu informations")     
class DISKVALUE(QThread,Ui_MainWindow):
    """
    Runs a disk thread.
    """
    z = pyqtSignal(int)

    def run(self):
        try:
            while True:
                obj_Disk = psutil.disk_usage('/')
                self.z.emit(int(obj_Disk.percent))
                time.sleep(1)            
        except:
            self.statusBar.showMessage("Error in getting disk informations")

#main class
class WindowShow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.SystemInfo()
        self.StartThread()
        self.actionAbout.triggered.connect(self.details)
        self.actionExit.triggered.connect(self.exit)
        th = threading.Thread(target=self.StatusInfo)
        th.setDaemon(True)
        th.start()
                   
    
    def SystemInfo(self):
        speed=speedtest.Speedtest()
        download=speed.download()
        upload=speed.upload()
        load1, load5, load15 = psutil.getloadavg()
        network = psutil.net_io_counters(pernic=True)
        ifaces = psutil.net_if_addrs()
        networks = list()
        for k, v in ifaces.items():
            ip = v[0].address
            data = network[k]
            ifnet = dict()
            ifnet['ip'] = ip
            
            ifnet['sent'] = '%.2fMB' % (data.bytes_sent/1024/1024)
            ifnet['recv'] = '%.2fMB' % (data.bytes_recv/1024/1024)
            ifnet['packets_sent'] = data.packets_sent
            ifnet['packets_recv'] = data.packets_recv
        
            networks.append(ifnet)
        print(networks)

        try:
            self.pltf.setText(self.pltf.text()+" "+platform.system())
            self.pltf_ver.setText(self.pltf_ver.text()+" "+platform.version())
            self.pltf_re.setText(self.pltf_re.text()+" "+platform.release())
            self.ram.setText(self.ram.text()+" "+str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")
            self.host.setText(self.host.text()+" "+socket.gethostname())
            self.ip.setText(self.ip.text()+" "+socket.gethostbyname(socket.gethostname()))
            self.mac.setText(self.mac.text()+" "+':'.join(re.findall('..', '%012x' % uuid.getnode())))            
            self.cpu.setText(self.cpu.text()+" "+platform.processor())
            self.cpu_cores.setText(self.cpu_cores.text()+" "+str(psutil.cpu_count()))
            self.cpu.setText(self.cpu.text()+" "+platform.processor())
            self.cpu_cores.setText(self.cpu_cores.text()+" "+str(psutil.cpu_count()))
            self.mac1.setText(self.mac1.text()+" "+str(size(speed.download())))
            self.mac2.setText(self.mac2.text()+" "+str(size(speed.upload())))          
            self.loadavg.setText(self.loadavg.text()+" "+str(psutil.getloadavg()))
            self.networktraffic.setText(self.networktraffic.text()+" "+str(networks))

        except:
            self.statusBar.showMessage("Error in getting System informations")
    def StartThread(self):
        self.ram_obj = SystemMonitor()
        self.cpu_obj = ProcessorUI() 
        self.disk_obj = DISKVALUE()
        self.ram_obj.x.connect(self.RamBar)
        self.cpu_obj.y.connect(self.CPUBar)
        self.disk_obj.z.connect(self.DiskBar)
        self.ram_obj.start()
        self.cpu_obj.start()
        self.disk_obj.start()
    
    def StatusInfo(self):
        try:
            while True:
                obj_Disk = psutil.disk_usage('/')
                self.ram_info.setText("\nAvailable Memory :"+str(round(psutil.virtual_memory().available/(1024.0**3),2)) + "Go"+"\n\n"+"Used Memory :"+str(round(psutil.virtual_memory().used/(1024.0**3),2)) + "Go")
                self.diskinfo.setText("\ntotal Disk  :"+ str(round(obj_Disk.total / (1024.0 ** 3),2))+"Go\n\nused Disk  :"+str(round(obj_Disk.used / (1024.0 ** 3),2)) + "Go\n\nfree Disk  :"+ str(round(obj_Disk.free / (1024.0 ** 3),2)) + "Go" )
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting additional information about ram and cpu")
    
    def RamBar(self, value):
        self.RamProgressBar.setValue(value)
    def CPUBar(self, value):
        self.CpuProgressBar.setValue(value)    
    def DiskBar(self,value):
        self.DiskProgressBar.setValue(value)
    def details(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About")
        msg.setText("SystemMonitor:\nVersion:1.0\nProgrammer:Oussama Ben Sassi")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()                                                  
    def exit(self):
        QtWidgets.QApplication.quit() 

app = QtWidgets.QApplication(sys.argv)
win = WindowShow()
sys.exit(app.exec_())        
