from datetime import datetime,timezone
def mission_time(self):
    now_utc = datetime.now(timezone.utc)
    time_utc = now_utc.time()
    v = time_utc.strftime('%H:%M:%S')
    cont1 = list(v.split(":"))
    cont=[]
    for i in range(len(cont1)):
            a = cont1[i]
            a = int(a)
            cont+=[a]
    cont[0] = cont[0]*3600
    cont[1] = cont[1]*60
    cont = cont[0] + cont[1] + cont[2]
    self.time = cont
    m = self.time//60
    s = self.time%60
    h = m//60
    m = m%60
    tim = "{:02d}:{:02d}:{:02d}".format(h,m,s)
    self.time+=1
            
    self.MENU2_mission_time.setText("Mission Time:"+str(tim))