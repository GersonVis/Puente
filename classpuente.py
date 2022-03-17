import socket
import  threading
class Conectado:
    def __init__(self, host, puerto, conectado, hosts, useragent, val):
        self.host=host
        self.puerto=puerto
        self.conectado=conectado
        self.hosts=hosts
        self.deneapro=1
        self.useragent=useragent
        self.agent=0
        self.val=val
        self.rec=threading.Thread(target=self.Reciviendo)
        self.rec.start()
        self.arch=''
        self.cont=""
        self.host2=""
        self.thEnvio=""
    def meCod(self, cab, et):
        cab=cab.partition(et)[2]
        cab=cab.partition(chr(13)+chr(10))[0]
        return cab
    def Reciviendo(self):
        self.recivido=self.conectado.recv(1024)
        #print self.recivido
        self.host2=self.meCod(self.recivido, "Host:")
        host=self.host2
        useragent=self.meCod(self.recivido, "User-Agent:")
        if useragent=="":
            return 0
#       print host
        if self.deneapro==1:       
         for comprobar in self.hosts:
            if host.find(comprobar)!=-1:
               # print comprobar
                return 0
       #  print "host aprobado", host
        elif deneapro==2:
           for comprobar in hosts:
            if host.find(comprobar)==1:
                pass
        t=0
        for comprobar in self.useragent:
            if useragent.find(comprobar)!=-1:
                t=1
                break
        if t==self.agent:
            return 0
        print "host aprobado: ", host, useragent
        
        self.soProxy=socket.socket()
        self.soProxy.connect((self.host, self.puerto))        
        self.thEnvio=threading.Thread(target=self.Envio)
        self.thEnvio.start()
        
        direc=host+str(self.val)+".txt"
    #    arch=open("Transferencia/"+direc, "w")
    #    arch.close()
    #    self.archi=open("Transferencia/"+direc, 'a')
        
     #   escucha=threading.Thread(target=self.Envio)
     #  escucha.start()
        while len(self.recivido)>0:
            #print self.recivido
    #        self.archi.write(self.recivido)
           
            self.cont+=self.recivido
            self.soProxy.send(self.recivido)
            print "vpn dns", self.recivido
            self.recivido=self.conectado.recv(2014)
           
               
   #     self.archi.close()
#        arch=open("Transferencia/"+direc, "w")
#        arch.write(self.cont)
#        arch.close()
    def Envio(self):
        bufProxy=self.soProxy.recv(1024)
        while len(bufProxy)>0:
    #        self.archi.write(bufProxy)
            self.cont+=bufProxy   
            self.conectado.send(bufProxy)
            print "navegador", bufProxy
            bufProxy=self.soProxy.recv(1024)
   #     self.archi.close()
        
class Servidor:
    
    def __init__(self, host, puerto):
        self.servidor=socket.socket()
        self.hosts=[]
        self.useragent=[]
        self.deneapro=1
        self.Reintentar(host, puerto)
        self.conectados=[]
    def cerrar(self):
        op=""
        while op!="0":
            print "Introduce la opcion: "
            op=raw_input()
            if op=="1":
                for cone in self.conectados:
                    #print cone.host2
                    try:
                        cone.conectado.close()
                    except IOError:
                         print "Error"
    def Reintentar(self, host, puerto):
        while 1:
            try:
                self.servidor.bind((host, puerto))
                print "ESCUCHANDO"
                break
            except IOError:
                pass
    def Hosts(self, arc, deneapr=1):
        self.deneapro=deneapr
        ar=open(arc, "r")
        for linea in ar:            
          lin=linea.replace("\n", "")
          self.hosts.append(lin)
        ar.close()
    def UserAgent(self, arc, deneapr=1):
        self.deneapro=deneapr
        ar=open(arc, "r")
        for linea in ar:            
          lin=linea.replace("\n", "")
          self.useragent.append(lin)
        ar.close()    
    def Escuchar(self, NumEscuchar=400):
        self.servidor.listen(NumEscuchar)
        c=0
     #   thr=threading.Thread(target=self.cerrar)
     #   thr.start()
        print "escuchando"
        while(NumEscuchar>0):
            conectado, info = self.servidor.accept()
            #print "conectado"
            co=Conectado("192.168.137.103", 8081, conectado, self.hosts, self.useragent, c)
            co.agent=1
            self.conectados.append(co)
            NumEscuchar-=1
            c+=1
servidor=Servidor("192.168.137.1", 2002)  
servidor.Hosts("Reglas/hosts.txt")
servidor.UserAgent("Reglas/UserAgent.txt")
servidor.Escuchar()   
