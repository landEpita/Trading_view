import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

from devise import *
from affichage import *
from strat import *

LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Trading algo")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        F =StartPage

        frame = F(container, self)

        self.frames[F] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        menubar = frame.menubar(self)
        self.configure(menu=menubar)
        return frame





class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        self.controller= controller
        tk.Frame.__init__(self, parent)
        self.devise = Devise("AAPL", (2015,1,1), (2019,1,1))
        self.Close_var = tk.IntVar()
        self.MA_var = tk.IntVar()
        self.STD_var = tk.IntVar()
        self.BBD_var =tk.IntVar()
        self.RSI_var =tk.IntVar()
        self.LMA_var =tk.IntVar()
        self.Hold_var_RSI =tk.IntVar()
        self.Hold_var_MA =tk.IntVar()
        self.Hold_var_MA_RSI =tk.IntVar()

        self.Hold_var_ichi1 =tk.IntVar()
        self.Hold_var_ichi2 =tk.IntVar()
        self.Hold_var_ichi3 =tk.IntVar()
        
        self.kuma_var = tk.IntVar()
        self.tenkan_var = tk.IntVar()
        self.chikou_var = tk.IntVar()
        self.kijun_var = tk.IntVar()

        self.name = "AAPL"
        self.txt = ""
        self.money = 100000
        self.res = 0
        self.lma = 100

        self.choice()

    def choice(self):
        Mainframe = tk.Frame(self,borderwidth=2)
        Mainframe.pack(side=tk.RIGHT,padx=5,pady=5)
        Frame1 = tk.Frame(Mainframe,borderwidth=2,relief=tk.GROOVE)
        Frame1.pack(side=tk.TOP,padx=10,pady=10) 

        Frame2 = tk.Frame(Mainframe,borderwidth=2,relief=tk.GROOVE)
        Frame2.pack(side=tk.BOTTOM,padx=10,pady=10)

        Frame3 = tk.Frame(Mainframe,borderwidth=2)
        Frame3.pack(side=tk.BOTTOM, padx=10, pady=10)
     
        Frame_ichi = tk.Frame(Frame3,borderwidth=2,relief=tk.GROOVE)
        Frame_ichi.pack(side=tk.RIGHT, padx=10, pady=10)

        Frame_strat = tk.Frame(Frame3,borderwidth=2,relief=tk.GROOVE)
        Frame_strat.pack(side=tk.LEFT,padx=10,pady=10)

    
        value = tk.StringVar() 
        value.set(self.name)
        entree = tk.Entry(Frame1, textvariable=value, width=30)
        value2 = tk.StringVar() 


        Close_check = tk.Checkbutton(Frame1, text="Close", variable=self.Close_var) 
        MA_check = tk.Checkbutton(Frame1, text="MA", var=self.MA_var)
        STD_check = tk.Checkbutton(Frame1, text="Ecart type", var=self.STD_var)
        BBD_check = tk.Checkbutton(Frame1, text="BBD", var=self.BBD_var)
        RSI_check = tk.Checkbutton(Frame1, text="RSI", var=self.RSI_var)
        LMA_check = tk.Checkbutton(Frame1, text="long MA", var=self.LMA_var)
        self.LMA = tk.Spinbox(Frame1, from_=60, to=200);

        Hold_check_RSI = tk.Checkbutton(Frame_strat, text="Holding_RSI", var=self.Hold_var_RSI)
        Hold_check_MA = tk.Checkbutton(Frame_strat, text="Holding_MA", var=self.Hold_var_MA)
        Hold_check_MA_RSI = tk.Checkbutton(Frame_strat, text="Holding_MA_CHIKU", var=self.Hold_var_MA_RSI)
        Hold_check_ichi_1 = tk.Checkbutton(Frame_strat, text="Holding_ichi_1", var=self.Hold_var_ichi1)
        Hold_check_ichi_2 = tk.Checkbutton(Frame_strat, text="Holding_ichi_2", var=self.Hold_var_ichi2)
        Hold_check_ichi_3 = tk.Checkbutton(Frame_strat, text="Holding_ichi_3", var=self.Hold_var_ichi3)

        Kijun = tk.Checkbutton(Frame_ichi, text="Kijun 26", var=self.kijun_var)
        Tenkan = tk.Checkbutton(Frame_ichi, text="Tenkan 9", var=self.tenkan_var)
        Chikou = tk.Checkbutton(Frame_ichi, text="Chikou", var=self.chikou_var)
        Kuma = tk.Checkbutton(Frame_ichi, text="Kuma", var=self.kuma_var)


        button_run = tk.Button(Frame1, text="Run",
                            command=lambda: self.runbutton(value.get()))


        self.val = tk.StringVar() 
        self.val.set(self.money)
        money = tk.Entry(Frame2, textvariable=self.val, width=30)
        money.pack()
        self.val2 = tk.StringVar() 
        self.val2.set(self.res)
        tk.Entry(Frame2, textvariable=self.val2, width=30).pack()


        self.shell = tk.Canvas(Frame2, width=250, height=500, bg='ivory', bd=0, scrollregion=(0, 0, 1000, 1000))
        self.shell.pack(side=tk.TOP, padx=5, pady=5)

        hbar=tk.Scrollbar(Frame2,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=self.shell.xview)
        vbar=tk.Scrollbar(Frame2,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.shell.yview)
        self.shell.config(width=250,height=300)
        self.shell.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)



        entree.pack()


        self.text_id = self.shell.create_text(10,10, anchor="nw", text=self.txt)
        

        Close_check.pack()
        MA_check.pack()
        STD_check.pack()
        BBD_check.pack()
        RSI_check.pack()
        LMA_check.pack()
        self.LMA.pack()
        Hold_check_RSI.pack()
        Hold_check_MA.pack()
        Hold_check_MA_RSI.pack()
        Hold_check_ichi_1.pack()
        Hold_check_ichi_2.pack()
        Hold_check_ichi_3.pack()
        
        Kuma.pack()
        Kijun.pack()
        Tenkan.pack()
        Chikou.pack()

        button_run.pack()
   
  
    def update(self):
        for widget in self.winfo_children():
            widget.pack_forget() # Si vous utilisez .pack()
        self.lma = self.LMA.get()
        self.money = self.val.get()
        _, nb,self.txt = resume(self.devise, int(self.money))
        self.res = nb
        self.choice()
        self.drawing()
        self.shell.create_text(10,10, anchor="nw", text=self.txt)
   
    def preporcessing(self, a):
        index = self.devise.data.index
        if self.Close_var.get() == 1:
            a.plot(index, self.devise.data['Adj Close'], label='Close')
        if self.MA_var.get() == 1:
            a.plot(index, self.devise.op_data['30 Day MA'], label='30 Day MA')
        if self.STD_var.get() == 1:
            a.plot(index, self.devise.op_data['30 Day STD'], label='30 Day STD')
        if self.BBD_var.get() == 1:
            print_BB(self.devise,a)
        if self.RSI_var.get() == 1:
            a.plot(index, self.devise.op_data['RSI'], label='RSI')
            a.fill_between(index, y1=30, y2=70, color='#adccff', alpha='0.3')
        if self.LMA_var.get() == 1:
            elt = self.devise.MA(int(self.lma))
            a.plot(index, elt, label= str(self.lma)+" long MA")
            #a.plot(index, self.devise.op_data['100 Day MA'], label='100 Day MA')
        
        
        if self.Hold_var_RSI.get() == 1:
            print_holding_RSI(self.devise,a)
        if self.Hold_var_MA.get() == 1:
            print_holding_MA(self.devise, a, self.devise.MA(int(self.lma)))
        if self.Hold_var_MA_RSI.get() == 1:
            print_holding_MA_CHIKU(self.devise, a)
        if self.Hold_var_ichi1.get() == 1:
            print_holding_ICHI(self.devise,a,1)
        if self.Hold_var_ichi2.get() == 1:
            print_holding_ICHI(self.devise,a,2)
        if self.Hold_var_ichi3.get() == 1:
            print_holding_ICHI(self.devise,a,3)
        

        if self.kuma_var.get() == 1:
            a.plot(index, self.devise.Ichimoku()['senkou_span_a'])
            a.plot(index, self.devise.Ichimoku()['senkou_span_b'])
            a.fill_between(index, y1=self.devise.Ichimoku()['senkou_span_b'], y2=self.devise.Ichimoku()['senkou_span_a'], color='#adccff', alpha='0.3')
        if self.kijun_var.get() == 1:
            a.plot(index, self.devise.Ichimoku()['kijun_sen'], label='kijun_sen')
        if self.tenkan_var.get() == 1:
            a.plot(index, self.devise.Ichimoku()['tenkan_sen'], label='tenkan_sen')
        if self.chikou_var.get() == 1:
            a.plot(index, self.devise.Ichimoku()['chikou_span'], label='chikou_span')







    def drawing(self):

        self.f = Figure(figsize=(5,5), dpi=100)

        a = self.f.add_subplot(111)
        a.grid()
        self.preporcessing(a)
        a.set_title('Courbe '+ self.name)
        a.set_xlabel('Date (Year/Month)')
        a.set_ylabel('Price(USD)')
        a.legend()
        #cursor = Cursor(a, useblit=True, color='grey', linewidth=0.5)




        canvas = FigureCanvasTkAgg(self.f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def add_Devise(self, name):
        try:
            if (self.name != name):
                self.devise = Devise(name, (2018,1,1), (2018,12,10))
                self.name = name
        except:
            print("not found")

    def runbutton(self, string):
        self.add_Devise(string)
        self.update()

    def menubar(self, root):
        menubar = tk.Menu(root)
        pageMenu = tk.Menu(menubar)
        pc = tk.Menu(menubar)
        pageMenu.add_command(label="AAPL", command= lambda: self.runbutton("AAPL"))
        pageMenu.add_command(label="FB", command= lambda: self.runbutton("FB"))
        pageMenu.add_command(label="IBM", command= lambda: self.runbutton("IBM"))
        pageMenu.add_command(label="GOOG", command= lambda: self.runbutton("GOOG"))
        pageMenu.add_command(label="MSFT", command= lambda: self.runbutton("MSFT"))
        pageMenu.add_command(label="AMZN", command= lambda: self.runbutton("AMZN"))
        pageMenu.add_command(label="SNY", command= lambda: self.runbutton("SNY"))
        pageMenu.add_command(label="NTDOY", command= lambda: self.runbutton("NTDOY"))
        pageMenu.add_command(label="HPQ", command= lambda: self.runbutton("HPQ"))
        pageMenu.add_command(label="QCOM", command= lambda: self.runbutton("QCOM"))
        pageMenu.add_command(label="NVDA", command= lambda: self.runbutton("NVDA"))

        pc.add_command(label="Global", command=pourcentage_duree)
        pc.add_command(label="Par année", command=pourcentage_annee)
        
        menubar.add_cascade(label="Devise", menu=pageMenu)
        menubar.add_cascade(label="Pourcentage", menu=pc)
        return menubar

    



app = SeaofBTCapp()
app.mainloop()
