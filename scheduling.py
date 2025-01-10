from tkinter import *
from tkinter import messagebox

def inserimentoDati(n):
    def listaDati():
        try:
            errore=False
            dati=[]
            if int(finestra2.grid_slaves(row=n+2)[0].get())>0:
                quantum=int(finestra2.grid_slaves(row=n+2)[0].get())
            
            for i in range(1,n+1,1):
                if int(finestra2.grid_slaves(row=i, column=1)[0].get())>=0 and int(finestra2.grid_slaves(row=i, column=2)[0].get())>0 and int(finestra2.grid_slaves(row=n+2)[0].get())>0:
                    dati.append([int(finestra2.grid_slaves(row=i, column=1)[0].get()),int(finestra2.grid_slaves(row=i, column=2)[0].get())])
                else:
                    errore=True
            if errore==False:
                finestra2.destroy()
                soluzione(dati,quantum)
            else:
                messagebox.showerror( "errore","errore, inserire un dato valido") 
        except:
            messagebox.showerror( "errore","errore, inserire un dato valido") 
    try:
        n=int(n)
        if n>0:
            finestra.destroy()
            finestra2 = Tk()
            finestra2.title("dati scheduling")
            tempo = Label(finestra2, text = 'tempo di arrivo')
            tempo.grid(column=1,row=0)
            durata = Label(finestra2, text = 'durata')
            durata.grid(column=2,row=0)
            for i in range(1,n+1,1):
                nprocessi = Label(finestra2, text = 'P'+str(i))
                nprocessi.grid(column=0,row=i)
                for c in range(1,3,1):
                    datiTesto = Entry(finestra2)
                    datiTesto.grid(column=c,row=i)  
            quantum_label=Label(finestra2, text = 'quantum')
            quantum_label.grid(columnspan=3,row=n+1)
            quantum=Entry(finestra2)
            quantum.grid(columnspan=3,row=n+2)
            bottone=Button(finestra2,text="inserisci",command=lambda:listaDati())
            bottone.grid(columnspan=3)     
        else:
            messagebox.showerror( "errore","errore, inserire un dato valido")
    except:
        messagebox.showerror( "errore","errore, inserire un dato valido")


def disegna_metro(canvas, lunghezza, unità): 
    canvas_width = lunghezza 
    canvas.config(width=canvas_width, height=100)
    canvas.create_line(0, 50, canvas_width, 50, fill="black")

    for i in range(lunghezza + 1):
        x = i * unità
        if i % 5 == 0:
            canvas.create_line(x, 45, x, 55, fill="black", width=2)
            canvas.create_text(x, 65, text=str(i), anchor=N)
        elif i % 1 == 0:
            canvas.create_line(x, 47, x, 53, fill="black")
    

def disegna_metro2(finestra3,tempo,u,dati,riga):
    unità = u
    schermo=95*unità
    lunghezza = tempo*unità
    if lunghezza>schermo:
        i=0
        while i==0:
            unità-=1
            if tempo*unità<=schermo:
                lunghezza=tempo*unità
                i=1

         

    canvas = Canvas(finestra3)
    canvas.grid(column=0, row=riga, sticky="ew",columnspan=len(dati))

    
    disegna_metro(canvas, lunghezza, unità)

def soluzione(dati,quantum):
    nomi=[]
    finestra3=Tk()
    finestra3.rowconfigure(2, weight=1)
    finestra3.columnconfigure(0, weight=1)
    finestra3.resizable(True,True)
    processi=Label(finestra3, text = 'FCFS',font="bold")
    processi.grid(column=0,row=0,columnspan=len(dati))
    canvas = Canvas(finestra3, width=sum([d[1]*20 for d in dati]), height=20)  
    canvas.grid(column=0, row=1, columnspan=len(dati), sticky="ew")
    
    def riordinafcfs(i):
        while i<len(dati): 
            backup=0
            if i!=len(dati)-1:
                if dati[i][0]>dati[i+1][0]:
                    backup=dati[i]
                    dati[i]=dati[i+1]
                    dati[i+1]=backup
                    i=0
                else:
                    i+=1
            else:
                i+=1
        for j in range (len(dati)):
            nomi.append("P"+str(dati[j][2]))

    
    for i in range(len(dati)):
        dati[i]=[dati[i][0],dati[i][1],i+1]
    i=0
    riordinafcfs(0)
    lunghezzadati=len(dati)

    def calcoli(canvas,finestra3,dati,riga,lunghezzadati,datiRR):
        
        tw=0
        tr=0
        tempo_di_completamento=0
        if riga==0:
            processi=Label(finestra3, text = 'FCFS',font="bold")
            processi.grid(column=0,row=riga,columnspan=len(dati))
        elif riga==5:
            processi=Label(finestra3, text = 'SJF',font="bold")
            processi.grid(column=0,row=riga,columnspan=len(dati))
        elif riga==10:
            processi=Label(finestra3, text = 'RR',font="bold")
            processi.grid(column=0,row=riga,columnspan=len(dati))
        canvas = Canvas(finestra3, width=sum([d[1]*20 for d in dati]), height=20)  
        canvas.grid(column=0, row=riga+1, columnspan=len(dati), sticky="ew")
        tempo=dati[0][0]       
        for i in range(len(dati)):
                if i == 0 or tempo_di_completamento < dati[i][0]:
                    tempo_di_completamento = dati[i][0]

                x = tempo_di_completamento * 20
                attesa = tempo_di_completamento - dati[i][0]
                turnoround = attesa + dati[i][1]
                tempo_di_completamento += dati[i][1]
                canvas.create_rectangle(x, 0, x + dati[i][1] * 20, 20, fill="blue")
                canvas.create_text(x + dati[i][1] * 10, 10, text=nomi[i], anchor=CENTER,fill="white")

                tw += attesa
                tr += turnoround

                if tempo>=dati[i][0]:
                    tempo+=dati[i][1]
                else:
                    tempo=dati[i][0]+dati[i][1]
        if riga==10:
            tw=0
            tr=0
            for i in range(len(datiRR)):
                    attesa = datiRR[i][2]-datiRR[i][1] - datiRR[i][0]
                    turnoround = datiRR[i][2]-datiRR[i][0]

                    tw += attesa
                    tr += turnoround


        tw /= lunghezzadati
        tr /= lunghezzadati
        disegna_metro2(finestra3, tempo, 20, dati,riga+2)
        scrittatw = Label(finestra3, text = "tw= "+str(tw),anchor="center")
        scrittatw.grid(columnspan=len(dati),row=riga+3,column=0)
        scrittatr = Label(finestra3, text = "tr= "+str(tr),anchor="center")
        scrittatr.grid(columnspan=len(dati),row=riga+4,column=0)
    calcoli(canvas,finestra3,dati,0,lunghezzadati,0)

    arrivati=[]


    def riordinasjf(posizione,dati,arrivati):
                nomi.clear()
                j=0
                while j in range(len(dati)):
                    i=0
                    while i in range (len(dati)-1):
                        if dati[i][1]>dati[i+1][1] and dati[i+1][0]<=posizione:
                            dati[i], dati[i + 1] = dati[i+ 1], dati[i]
                            i=0
                        else:
                            i+=1
                    if dati[j][0]<=posizione:
                        arrivati.append(dati[j])
                        posizione+=dati[j][1]
                        dati.pop(j)
                    else:
                        arrivati.append(dati[j])
                        posizione=dati[j][0]+dati[j][1]
                        dati.pop(j)
                
                            

                for j in range (len(arrivati)):
                    nomi.append("P"+str(arrivati[j][2]))
                return arrivati


                
                        

                        
                            
                
                  
    posizione=dati[0][0]
    dati=riordinasjf(posizione,dati,arrivati)
    calcoli(canvas,finestra3,dati,5,lunghezzadati,0)


    def riordinaRR(i,posizione,fatti,dati,nomi,quantum):
        calcoli=[]
        for b in range(len(dati)):
            calcoli.append([dati[b][0],dati[b][1],0])
        primo=True
        nomi.clear()
        attesa=[dati[0]]
        dati.pop(i)
        a=0
        fine=False
        
        
        while fine==False:
            
            
            

                
                
            if len(dati)>0:
                if len(dati)!=0 :
                    if posizione<dati[a][0] and len(attesa)==0:
                        posizione=dati[a][0]
                while a!=len(dati):
                    if posizione>=dati[a][0] :
                        attesa.append(dati[a])
                        dati.pop(a)
                    else:
                        break    
                


            if len(attesa)!=0:
                if attesa[i][1]-quantum>-1:
                    fatti.append([attesa[i][0],quantum,attesa[i][2]])
                    attesa[i][1]-=quantum
                    
                    if primo!=True :
                        posizione+=quantum

                        while a!=len(dati):
                            if posizione>=dati[a][0] :
                                attesa.append(dati[a])
                                dati.pop(a)
                            else:
                                break    
                    
                    
                    if attesa[i][1]==0:
                        calcoli[attesa[i][2]-1][2]=posizione
                        attesa.pop(i)
                        
                    else:
                        attesa.append(attesa[i])
                        attesa.pop(i)  
                    
                    
                elif attesa[i][1]<quantum:


                    resto=quantum-(quantum-attesa[i][1])
                    fatti.append([attesa[i][0],resto,attesa[i][2]])
                    calcoli[attesa[i][2]-1][2]=posizione+resto
                    attesa[i][1]-=resto
                    attesa.pop(i)
                    if primo!=True and len(attesa)>0:
                        posizione+=resto

                        while a!=len(dati):
                            if posizione>=dati[a][0] :
                                attesa.append(dati[a])
                                dati.pop(a)
                            else:
                                break    
                          
            primo=False
            if len(dati)==0 and len(attesa)==0:
                fine=True
                
      
        for j in range (len(fatti)):
            nomi.append("P"+str(fatti[j][2]))
        risultati=[fatti,calcoli]
        return risultati
    
    
    riordinafcfs(0)
    i=0
    if dati[0][1]==1:
        posizione=dati[0][0]+1
    if dati[0][1]>=quantum:
        posizione=dati[0][0]+quantum
    fatti=[]
    while i!=len(dati):
            if i+1!=len(dati):
                if dati[i][2]>dati[i+1][2] and dati[i][0]==dati[i+1][0]:
                    dati[i], dati[i + 1] = dati[i+ 1], dati[i]
                    i=0
                else:i+=1
            else:i+=1
    i=0
    nomi=[]
    risultati=riordinaRR(0,posizione,fatti,dati,nomi,quantum)
    
    calcoli(canvas,finestra3,risultati[0],10,lunghezzadati,risultati[1])
        


    finestra3.mainloop()

finestra = Tk()
finestra.title("dati scheduling")
processi = Label(finestra, text = 'inserisci quanti processi vuoi calcolare')
processi.pack()
processiTesto = Entry(finestra)
processiTesto.pack()
bottone=Button(finestra,text="inserisci",command=lambda:inserimentoDati(processiTesto.get()))
bottone.pack()
finestra.mainloop()
