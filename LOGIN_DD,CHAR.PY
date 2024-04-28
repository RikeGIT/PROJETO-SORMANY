import customtkinter as ctk
import sqlite3 
from tkinter import *
from tkinter import messagebox
class BackEnd():
 
    def conecta_db(self):
        self.conn = sqlite3.connect("DD_CHARGEN.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados Conectado")
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados Desconectado")

    def criar_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL

            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso")
        self.desconecta_db()


    def cadastrar_usuario_bdd(self):
        self.usarname_cadastro_bd = self.cadastro_user.get()
        self.senha_cadastro_bd = self.cadastro_senha.get()
        self.csenha_cadastro_bd = self.confirmar_senha.get()

        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Senha, Confirma_senha)
            VALUES (?, ?, ?)""", (self.usarname_cadastro_bd, self.senha_cadastro_bd, self.csenha_cadastro_bd))
        try:
            if(self.usarname_cadastro_bd == "" or self.senha_cadastro_bd == "" or self.csenha_cadastro_bd == ""):
                messagebox.showerror(title="Sistema de login", message= "ERROR!!! \nPor favor preencha todos os campos!")
        
            elif (len(self.usarname_cadastro_bd) <= 4):
                messagebox.showwarning(title="Sistema de login", message="Nome de Usuario deve ter mais do que 4 caracteres")

            elif (len(self.senha_cadastro_bd) <= 4):
                messagebox.showwarning(title="Sistema de login", message="A senha deve ter mais do que 4 caracteres")

            
            elif (self.senha_cadastro_bd != self.csenha_cadastro_bd):
                messagebox.showerror(title="Sistema de login", message= "ERROR \n As senhas não coincidem.")
            
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de Login", message=(f"Parabéns {self.usarname_cadastro_bd} \nSua conta foi criada com sucesso"))
                self.desconecta_db()
                self.limpar_entry_cadastro()
        except:
            messagebox.showerror(title= "Sistema de Login",message= "ERROR NO PROCESSAMENTO DO CADASTRO")
            self.desconecta_db()
    def verifica_login(self):
        self.username_login = self.user.get()
        self.senha_login = self.senha.get()

        self.conecta_db()
        
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))
        self.verifica_dados = self.cursor.fetchone() #percorrendo a Tabela de usuarios

        try:
            if(self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistemas de Login", message=f"Parabéns {self.username_login}\nLogin feito com sucesso")
                self.desconecta_db()
                self.limpar_entry_login()
        except:
            messagebox.showerror(title="Sistema de login", message="Login invalido")
            self.desconecta_db()

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.Cores()
        self.configurar_janela_inicial()
        self.tela_login()
        self.criar_tabela()
    
    def Cores(self):
        self.c1 = "#000000"  # preto
        self.c2 = "#FFFFFF"  # branco                                                       
        self.c3 = "#F8F6EA"  # branco/bege
        self.c4 = "#000711"  # AZUL FOSCO/MAR
        self.c5 = "#1F1F1F"  # transparente
        self.c6 = "#560000"  # vermelho
        self.c7 = "#5A6770"  # cinza/dragao
        self.c8 = "#838383"  # cinza/borda

    def configurar_janela_inicial(self):
        self.geometry("1920x1080")
        self.title("DD CHAR GEN")
        self.resizable(False, False)
        self.attributes('-fullscreen', True)
        
    def tela_login(self):
        # BACKGROUND
        self.background_img = PhotoImage(file = "imagens\POHA-PFVR.png")
        self.back_img = ctk.CTkLabel(self, text=None, image= self.background_img)
        self.back_img.grid(row = 1, column = 0,)
        
        # FRAME LOGIN

        self.login_frame = ctk.CTkFrame(self, width=400, height=353, border_width= 2, border_color= self.c1, fg_color = "#FFD8BB" )
        self.login_frame.place(x = 930, y = 358)

        # WIDGETS V

        # Usuario
        self.user = ctk.CTkEntry(self.login_frame, width= 332, height= 52, placeholder_text= "Nome de Usuario", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 10)
        self.user.place(x = 32, y = 33)

        # Senha

        self.senha = ctk.CTkEntry(self.login_frame, width= 332, height= 52, placeholder_text= "Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.senha.place(x = 32, y = 121)

        # Botão para ver senhaz

        self.ver_senha = ctk.CTkCheckBox(self.login_frame, text= "Clique para ver a Senha", font=("PtSerif", 12), text_color= self.c1, corner_radius= 10)
        self.ver_senha.place(x = 45, y = 194)

        # Botão entrar

        self.entrar = ctk.CTkButton(self.login_frame, width= 300, height= 45, text= "ENTRAR", font=("PtSerif", 20), fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 15, command= self.verifica_login)
        self.entrar.place(x = 45, y = 230)

        # Botão criar conta

        self.criar_conta = ctk.CTkButton(self.login_frame, text="CRIAR CONTA", font=("PtSerif", 12), fg_color=self.c6, border_color=self.c1, hover_color="#3E0101", border_width= 3, width=150, height=39, corner_radius= 15, command= self.tela_de_cadastro)
        self.criar_conta.place(x = 123, y = 289)

    def tela_de_cadastro(self):
        # REMOVENDO TELA DE LOGIN
        self.login_frame.place_forget()


        # Widgets tela de cadastro

        self.registro_frame = ctk.CTkFrame(self, width= 400, height= 433, border_width= 2, border_color= self.c1, fg_color= "#ffd8bb")
        self.registro_frame.place(x = 930, y =358)

        # CADASTRAR Usuario
        self.cadastro_user = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Nome de Usuario", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 10)
        self.cadastro_user.place(x = 32, y = 33)
        
        # CADASTRAR Senha

        self.cadastro_senha = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.cadastro_senha.place(x = 32, y = 116)

        # CONFIRMAR Senha

        self.confirmar_senha = ctk.CTkEntry(self.registro_frame, width= 332, height= 52, placeholder_text= "Confirmar Senha", font=("PtSerif", 20), text_color= self.c2,fg_color = ("#061121"), border_color= self.c7,border_width= 3, corner_radius= 10, show = "*")
        self.confirmar_senha.place(x = 32, y = 198)

        # REGISTRE-SE

        self.registre_se = ctk.CTkButton(self.registro_frame, width= 300, height= 45, text= "Registre-se", font=("PtSerif", 20), fg_color = ("#061121"),border_color= self.c7, border_width= 3, corner_radius= 15, command= self.cadastrar_usuario_bdd)
        self.registre_se.place(x = 45, y = 280)


        # OU 
        self.ou_lb = ctk.CTkLabel(self.registro_frame, width= 30, height= 16, text= "OU", text_color= self.c1, font=("PtSerif", 20))
        self.ou_lb.place(x = 187, y = 330)

        # VOLTAR

        self.voltar = ctk.CTkButton(self.registro_frame, text="VOLTAR", font=("PtSerif", 12), fg_color=self.c6, border_color=self.c1, hover_color="#3E0101", border_width= 3, width=150, height=39, corner_radius= 15, command= self.voltar_login)
        self.voltar.place(x = 125, y = 364)
    def voltar_login(self):
        self.registro_frame.place_forget()
        self.tela_login()
    def limpar_entry_cadastro(self):
        self.cadastro_user.delete(0, END)
        self.cadastro_senha.delete(0, END)
        self.confirmar_senha.delete(0, END)
        self.cadastro_user.delete(0, END)
    def limpar_entry_login(self):
        self.user.delete(0, END)
        self.senha.delete(0, END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
