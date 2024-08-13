import customtkinter as ctk
import tkinter as tk
import re
import keyboard
import pyautogui
import webbrowser

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
appWidth, appHeight = 900, 500

# Função para extrair CPFs do texto
def extrair_cpfs(texto):
    padrao_cpf_formatado = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
    padrao_cpf_numerico = r'\b\d{11}\b'
    padrao_cpf_outros = r'\d{3}\.\d{3}\.\d{3}\.\d{2}'
    sem_padrao_1 = r'\d{3}\.\d{6}\.\d{2}'
    sem_padrao_2 = r'\d{3}\.\d{8}'
    sem_padrao_3 = r'\d{3}\.\d{3}\.\d{5}'
    sem_padrao_4 = r'\d{6}\.\d{3}\.\d{2}'
    sem_padrao_5 = r'\d{9}\.\d{2}'
    sem_padrao_6 = r'\d{3}-\d{6}-\d{2}'
    sem_padrao_7 = r'\d{3}-\d{8}'
    sem_padrao_8 = r'\d{3}-\d{3}-\d{5}'
    sem_padrao_9 = r'\d{9}-\d{2}'
    sem_padrao_10 = r'\d{3}-\d{3}-\d{3}-\d{2}'

    cpfs_formatados = re.findall(padrao_cpf_formatado, texto)
    cpfs_numericos = re.findall(padrao_cpf_numerico, texto)
    cpfs_outros = re.findall(padrao_cpf_outros, texto)
    padra_1 = re.findall(sem_padrao_1, texto)
    padra_2 = re.findall(sem_padrao_2, texto)
    padra_3 = re.findall(sem_padrao_3, texto)
    padra_4 = re.findall(sem_padrao_4, texto)
    padra_5 = re.findall(sem_padrao_5, texto)
    padra_6 = re.findall(sem_padrao_6, texto)
    padra_7 = re.findall(sem_padrao_7, texto)
    padra_8 = re.findall(sem_padrao_8, texto)
    padra_9 = re.findall(sem_padrao_9, texto)
    padra_10 = re.findall(sem_padrao_10, texto)

    cpfs_formatados_limpos = [re.sub(r'\D', '', cpf) for cpf in cpfs_formatados]
    cpfs_formatados_outros = [re.sub(r'\D', '', cpf) for cpf in cpfs_outros]
    a_1 = [re.sub(r'\D', '', cpf) for cpf in padra_1]
    a_2 = [re.sub(r'\D', '', cpf) for cpf in padra_2]
    a_3 = [re.sub(r'\D', '', cpf) for cpf in padra_3]
    a_4 = [re.sub(r'\D', '', cpf) for cpf in padra_4]
    a_5 = [re.sub(r'\D', '', cpf) for cpf in padra_5]
    a_6 = [re.sub(r'\D', '', cpf) for cpf in padra_6]
    a_7 = [re.sub(r'\D', '', cpf) for cpf in padra_7]
    a_8 = [re.sub(r'\D', '', cpf) for cpf in padra_8]
    a_9 = [re.sub(r'\D', '', cpf) for cpf in padra_9]
    a_10 = [re.sub(r'\D', '', cpf) for cpf in padra_10]
    cpfs_todos = cpfs_formatados_limpos + cpfs_numericos + cpfs_formatados_outros + a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7 + a_8 + a_9 + a_10

    return cpfs_todos

def processar_cpfs(mensagem):
    texto = app.inserir.get("1.0", tk.END)
    cpfs = extrair_cpfs(texto)
    if "Lista" in mensagem:
        cpfs_com_virgula = '\n'.join(cpfs)
    else:
        cpfs_com_virgula = ',\n'.join(cpfs)

    app.displayBox.delete("1.0", tk.END)
    app.displayBox.insert(tk.END, mensagem + "\n" + cpfs_com_virgula)

def auto_colar(mensagem):
    try:
        texto_copiado = app.clipboard_get()
        app.inserir.delete("1.0", tk.END)
        app.inserir.insert(tk.END, texto_copiado)
        processar_cpfs(mensagem)
    except tk.TclError:
        print("Nenhum texto copiado ou erro ao acessar a área de transferência.")

def iniciar_insercao_cpfs():
    texto_cpfs = app.cpfs_textbox.get("1.0", tk.END).strip()
    app.cpfs_lista = texto_cpfs.splitlines()
    app.cpfs_index = 0

    def colar_proximo_cpf():
        if app.cpfs_index < len(app.cpfs_lista):
            cpf = app.cpfs_lista[app.cpfs_index]
            pyautogui.typewrite(cpf)
            app.cpfs_lista[app.cpfs_index] += " - OK"
            app.popup_label.configure(text="\n".join(app.cpfs_lista))
            app.cpfs_index += 1
        if app.cpfs_index >= len(app.cpfs_lista):
            app.popup.destroy()
            keyboard.remove_hotkey('capslock')

    keyboard.add_hotkey('capslock', colar_proximo_cpf)

    window_position = pyautogui.position()
    app.popup = tk.Toplevel(app)
    app.popup.title("Inserção Automática")
    app.popup.geometry(f"+{window_position[0]+20}+{window_position[1]+20}")
    app.popup_label = ctk.CTkLabel(app.popup, text="\n".join(app.cpfs_lista), font=ctk.CTkFont(size=12), text_color="black")
    app.popup_label.pack(pady=10)

def cancelar_insercao_cpfs():
    try:
        if hasattr(app, 'popup'):
            app.popup.destroy()
        keyboard.remove_hotkey('capslock')
        keyboard.remove_hotkey('alt')
        keyboard.remove_hotkey('capslock')  # Remover CapsLock = Ctrl+C
        print("Operação de inserção automática cancelada e mapeamentos de teclas desfeitos.")
    except Exception as e:
        print(f"Erro ao cancelar operação: {e}")

def mapear_capslock_para_ctrl_c():
    keyboard.add_hotkey('capslock', lambda: keyboard.send('ctrl+v'))
    print("CapsLock mapeado para Ctrl+v")

def mapear_alt_para_ctrl_v():
    keyboard.add_hotkey('alt', lambda: keyboard.send('ctrl+c'))
    print("Alt mapeado para Ctrl+c")

def abrir_popup_funciona():
    popup = tk.Toplevel(app)
    popup.title("Como Funciona")
    popup.geometry("400x260")
    label = ctk.CTkLabel(popup, text="Coloque os CPFs na caixa de texto e ao clicar\n em Iniciar em Quantidade o Capslock\n funcionará como um Ctrl+V e abrirá uma\n pequena tela com os CPFs.\n Escolha um lugar para colar e a\n cada vez que apertar o\n Capslock será inserido o\n CPF neste lugar e na pequena\n janela será marcado ao lado do CPF um - ok. ", font=ctk.CTkFont(size=14), text_color="black")
    label.pack(pady=20)
    btn_close = ctk.CTkButton(popup, text="Fechar", command=popup.destroy, fg_color="gray5")
    btn_close.pack(pady=10)

# Função para copiar o conteúdo da caixa de exibição
def copiar_texto():
    try:
        texto_a_copiar = app.displayBox.get("1.0", tk.END).strip()
        app.clipboard_clear()
        app.clipboard_append(texto_a_copiar)
        print("Texto copiado")
    except tk.TclError:
        print("Erro ao copiar texto")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("RMD_v1.0.3")
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(width=False, height=False)
    
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0,fg_color="teal")
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Refiner Macro Date", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        
        self.progressbar = ctk.CTkProgressBar(self.sidebar_frame, orientation="horizontal", mode="indeterminate", width=220, height=5,fg_color="teal",indeterminate_speed=0.2)
        self.progressbar.grid(row=1, column=0, padx=0, pady=10)
        self.progressbar.start()
        
        
        self.btn_page1 = ctk.CTkButton(self.sidebar_frame, text="Filtro", command=self.show_page1, corner_radius=15,border_width=1,border_color="orange")
        self.btn_page1.grid(row=2, column=0, padx=20, pady=10)
        self.btn_page2 = ctk.CTkButton(self.sidebar_frame, text="Converter Imagem", command=self.show_page2, corner_radius=15,border_width=1,border_color="orange")
        self.btn_page2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Nova Ferramenta", command=self.show_page3, corner_radius=15,border_width=1,border_color="orange")
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_5 = ctk.CTkButton(self.sidebar_frame, text="IA Chat", command=self.show_page4, corner_radius=15,border_width=1,border_color="orange")
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_7 = ctk.CTkButton(self.sidebar_frame, text="Sobre", command=self.show_page5, corner_radius=15,border_width=1,border_color="orange")
        self.sidebar_button_7.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_6 = ctk.CTkButton(self.sidebar_frame, text="APOIE O PROJETO", command=self.apoio,height=20, fg_color="transparent", text_color="white",hover_color="orange",border_width=2)
        self.sidebar_button_6.grid(row=9, column=0, padx=20, pady=(150,10))

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.show_page1()
        
    def show_page1(self):
        self.clear_frame()
        label = ctk.CTkLabel(self.main_frame, text=" FILTRO DE CPF ", font=ctk.CTkFont(size=24),fg_color="green",corner_radius=12)
        label.pack(pady=20)
        btn_apagar = ctk.CTkButton(self.main_frame, text="Apagar", width=10, height=6, command=self.apagar_texto,font=ctk.CTkFont(size=10), fg_color="gray25", hover_color="red")
        btn_apagar.pack(pady=0)

        self.inserir = ctk.CTkTextbox(self.main_frame, width=500, height=150,border_width=1,border_color="gray40")
        self.inserir.pack(pady=1)        
        
        self.seg_button_1 = ctk.CTkSegmentedButton(self.main_frame)
        self.seg_button_1.pack(pady=5)
        self.seg_button_1.configure(values=["Compartilhado", "Individual", "Lista"], command=self.segment_button_function)

        self.displayBox = ctk.CTkTextbox(self.main_frame, width=500, height=160,border_width=1,border_color="gray40")
        self.displayBox.pack(pady=0)
        
        btn_copiar = ctk.CTkButton(self.main_frame, text="Copiar", width=10, height=6, command=copiar_texto, font=ctk.CTkFont(size=10), fg_color="gray25",hover_color="teal")
        btn_copiar.pack(pady=2)
        
    def segment_button_function(self, value):
        if value == "Compartilhado":
            auto_colar("Inserir Créditos Compartilhados")
        elif value == "Individual":
            auto_colar("Inserir Créditos Individuais")
        elif value == "Lista":
            auto_colar("Lista de CPFs:")

    def apagar_texto(self):
        self.inserir.delete("1.0", tk.END)
        self.displayBox.delete("1.0", tk.END)

    def show_page2(self):
        self.clear_frame()
        label = ctk.CTkLabel(self.main_frame, text="CONVERSOR DE IMAGEM EM TEXTO", font=ctk.CTkFont(size=24))
        label.pack(pady=20)
        
        btn_convert_images = ctk.CTkButton(self.main_frame, text="Escolher Imagens", command=self.convert_images)
        btn_convert_images.pack(pady=20)
        
    def apoio(self):
        url = "https://rmd103.wordpress.com/"
        webbrowser.open(url)

    def show_page3(self):
        self.clear_frame()
        label = ctk.CTkLabel(self.main_frame, text="  Popup CPF's  ", font=ctk.CTkFont(size=24),fg_color="teal",corner_radius=15)
        label.pack(pady=10)
        
        
        self.cpfs_textbox = ctk.CTkTextbox(self.main_frame, width=200, height=200,border_width=1,border_color="gray40")
        self.cpfs_textbox.pack(pady=10)
        
        btn_inserir_cpfs = ctk.CTkButton(self.main_frame, text="Iniciar em quantidade", command=iniciar_insercao_cpfs, width=200,height=10,border_width=1,border_color="gray40")
        btn_mapear_capslock = ctk.CTkButton(self.main_frame, text="Trocar CapsLock por Ctrl+V", command=mapear_capslock_para_ctrl_c, width=200,fg_color="teal",height=10,border_width=1,border_color="gray40")
        btn_mapear_alt = ctk.CTkButton(self.main_frame, text="Trocar Alt por Ctrl+C", command=mapear_alt_para_ctrl_v, width=200,fg_color="teal",height=10,border_width=1,border_color="gray40")
        btn_cancelar_insercao = ctk.CTkButton(self.main_frame, text="Cancelar Ação", command=cancelar_insercao_cpfs, width=200,fg_color="red",hover_color="purple",height=10,border_width=1,border_color="gray40")
        btn_inserir_cpfs.pack(pady=5)
        btn_mapear_capslock.pack( pady=5)
        btn_mapear_alt.pack(pady=5)
        btn_cancelar_insercao.pack( pady=5)

        btn_funcao = ctk.CTkButton(self.main_frame, text="                                                                                                                                                                    Como funciona?", command=abrir_popup_funciona, font=ctk.CTkFont(size=12), fg_color="transparent", hover_color="gray17")
        btn_funcao.pack(pady=10)

    def show_page4(self):
        self.clear_frame()
        label = ctk.CTkLabel(self.main_frame, text="    IA Chat   ", font=ctk.CTkFont(size=24),text_color="white",fg_color="orange",corner_radius= 15)
        label.pack(pady=20)
        
        self.chat_input = ctk.CTkTextbox(self.main_frame, width=500, height=50,fg_color="gray40",border_width=1,border_color="gray60")
        self.chat_input.pack(pady=10)
        
        btn_send_message = ctk.CTkButton(self.main_frame, text="Enviar", command=self.send_message,fg_color="orange",hover_color="teal")
        btn_send_message.pack(pady=5)
        
        self.chat_display = ctk.CTkTextbox(self.main_frame, width=500, height=250,fg_color="gray40",border_width=1,border_color="gray60")
        self.chat_display.pack(pady=10)
        
    def show_page5(self):
        self.clear_frame()
        label = ctk.CTkLabel(self.main_frame, text="Sobre", font=ctk.CTkFont(size=24))
        label.pack(pady=20)
        blabel = ctk.CTkButton(self.main_frame, text="Nota de Atualização - Versão 1.0.3 [↓]", font=ctk.CTkFont(size=18), command=self.nota, fg_color="green")
        blabel.pack(pady=20)
        
    def nota(self):
        label = ctk.CTkLabel(self.main_frame, text="Funcionalidades Implementadas:", font=ctk.CTkFont(size=16))
        label.pack(pady=10)
        label = ctk.CTkLabel(self.main_frame, text="∙ Filtro de CPF: Filtra CPFs de texto, exibe os resultados e copia manualmente.\n∙ Conversor de Imagem em Texto: Seleção de imagens para futura conversão em texto.\n∙ Ferramentas: Mapeia CapsLock para Ctrl+C e Alt para Ctrl+V, e permite inserção automática de CPFs.\n∙ IA Chat: Simula interações de chat com resposta predefinida.\n∙ Contato: Informações de contato e notas de atualização.\n∙ Apoie o Projeto: Link para apoiar o desenvolvimento do projeto. ", font=ctk.CTkFont(size=12))
        label.pack(pady=10)
        label = ctk.CTkLabel(self.main_frame, text="Melhorias Planejadas para Versões Futuras:", font=ctk.CTkFont(size=16))
        label.pack(pady=5)
        label = ctk.CTkLabel(self.main_frame, text="∙ Conversor de Imagens: Completar a funcionalidade para conversão de imagens em texto na versão 1.0.4.\n∙ IA Chat: Implementação de uma inteligência artificial para resposta a mensagens no chat.\n", font=ctk.CTkFont(size=12))
        label.pack(pady=2)
        self.label = ctk.CTkLabel(self.main_frame, text="@by Jefferson\n\n\n", font=("italian",20))
        self.label.pack(pady=0)
        self.current_color = "red"
        self.change_color()
    def change_color(self):
        if self.current_color == "red":
            self.current_color = "teal"
        elif self.current_color == "teal":
            self.current_color = "green"
        elif self.current_color == "green":
            self.current_color = "orange"
        elif self.current_color == "orange":
            self.current_color = "purple"
        elif self.current_color == "purple":
            self.current_color = "white"
        elif self.current_color == "white":
            self.current_color = "yellow"
        else:
            self.current_color = "red"
        self.label.configure(text_color=self.current_color)
        self.after(500, self.change_color)
   
   
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def convert_images(self):
        file_paths = tk.filedialog.askopenfilenames(title="Selecione as imagens para converter", filetypes=[("Image files", ".png;.jpg;.jpeg;.bmp")])
        for file_path in file_paths:
            label = ctk.CTkLabel(self.main_frame, text=(f"Imagem selecionada: {file_path}"), font=ctk.CTkFont(size=12))
            label.pack(pady=10)
            btn_converter = ctk.CTkButton(self.main_frame, text="Converter em Texto", command=self.converter)
            btn_converter.pack(pady=20)
            self.textboximg = ctk.CTkTextbox(self.main_frame, width=380, height=150)
            self.textboximg.pack(pady=10)
            
    def converter(self):
        self.textboximg.insert(tk.END, f"\n\n\n\n\n\n\n   Conversor ainda não disponivel. Será inserido na versão 1.0.4.")

    def send_message(self):
        message = self.chat_input.get("1.0", tk.END).strip()
        if message:
            response = self.get_ai_response(message)
            self.chat_display.insert(tk.END, f"-> Você: {message}\n\n-> IA: Ainda não estou pronto para isso. \n\n\n\n\n\n\n\n\n\n\n")
            self.chat_display.insert(tk.END, f"             {response}\n")
            self.chat_input.delete("1.0", tk.END)
    def get_ai_response(self, message):
        print("Erro ao se comunicar com a API")
        return "Inteligência artificial ainda não disponivel. Será inserido na versão 1.0.4."

if __name__ == "__main__":
    app = App()
    app.mainloop()
