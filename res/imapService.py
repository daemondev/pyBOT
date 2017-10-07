import win32service
import win32event
import servicemanager
import socket
import imaplib2, time
from threading import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime
import email

class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()

    def start(self):
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        while True:
            if self.event.isSet():
                return
            self.needsync = False
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            self.M.idle(callback=callback)
            self.event.wait()
            if self.needsync:
                self.event.clear()
                self.dosync()


    def dosync(self):
        #DO SOMETHING HERE WHEN YOU RECEIVE YOUR EMAIL

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "receiveemail"
    _svc_display_name_ = "receiveemail"


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        M = imaplib2.IMAP4_SSL("imap.gmail.com", 993)
        M.login("YourID", "password")
        M.select("INBOX")
        idler = Idler(M)
        idler.start()
        while True:
            time.sleep(1*60)
        idler.stop()
        idler.join()
        M.close()
        M.logout()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
