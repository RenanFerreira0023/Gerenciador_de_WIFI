import subprocess
import tkinter as tk
import json
import time

import datetime
import sys

# Função para listar as redes Wi-Fi disponíveis
def listar_redes_wifi():
    result = subprocess.run('netsh wlan show networks', shell=True, capture_output=True, text=True)
    redes_wifi.config(state="normal")
    redes_wifi.delete(1.0, "end")

    # Modificando o resultado para mostrar apenas os SSIDs
    redes_encontradas = [line.split(":")[1].strip() for line in result.stdout.split("\n") if "SSID" in line]
    redes_wifi.insert("end", "\n".join(redes_encontradas))
    
    redes_wifi.config(state="disabled")

# Função para conectar à rede Wi-Fi com senha
def conectar_wifi():
    ssid = ssid_entry.get()
    senha = senha_entry.get()
    comando = f'netsh wlan set profileparameter name="{ssid}" keyMaterial="{senha}"'
    subprocess.run(comando, shell=True)
    comando = f'netsh wlan connect name="{ssid}"'
    subprocess.run(comando, shell=True)
    status_label.config(text=f"Conectado à rede: {ssid}")



# Função para desconectar da rede Wi-Fi
def desconectar_wifi():
    comando = 'netsh wlan disconnect'
    subprocess.run(comando, shell=True)
    status_label.config(text="Desconectado da rede")




# Função para verificar e controlar o Wi-Fi com base nos horários
def verificar_horario_wifi_BKP():
    hora_atual = time.strftime("%H:%M")
    hora_inicio = hora_inicio_entry_1.get()
    hora_final = hora_final_entry_1.get()
    
    result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
    
    if "Conectado" in result.stdout:
        if hora_inicio <= hora_atual <= hora_final:
            # Está dentro do horário, Wi-Fi já está ligado
            status_label.config(text="Wi-Fi ligado")
        else:
            # Está fora do horário, desligue o Wi-Fi
            comando = 'netsh wlan disconnect'
            subprocess.run(comando, shell=True)
            status_label.config(text="Desconectado da rede")
            status_label.config(text="Wi-Fi desligado")
    else:
        if hora_inicio <= hora_atual <= hora_final:
            # Está dentro do horário, ligue o Wi-Fi
            # subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', shell=True)
            ssid = ssid_entry.get()
            senha = senha_entry.get()
            comando = f'netsh wlan set profileparameter name="{ssid}" keyMaterial="{senha}"'
            subprocess.run(comando, shell=True)
            comando = f'netsh wlan connect name="{ssid}"'
            subprocess.run(comando, shell=True)
            status_label.config(text=f"Conectado à rede: {ssid}")

            status_label.config(text="Wi-Fi ligado")
        else:
            # Está fora do horário, Wi-Fi já está desligado
            status_label.config(text="Wi-Fi desligado")
    
    # Agende a próxima verificação em 5 segundos
    window.after(15000, verificar_horario_wifi)


# Função para verificar e controlar o Wi-Fi com base nos horários
def verificar_horario_wifi():
    hora_atual = time.strftime("%H:%M")
    usar_faixa_1 = switch_var_1.get()
    hora_inicio_1 = hora_inicio_entry_1.get()
    hora_final_1 = hora_final_entry_1.get()
    
    usar_faixa_2 = switch_var_2.get()
    hora_inicio_2 = hora_inicio_entry_2.get()
    hora_final_2 = hora_final_entry_2.get()
    
    usar_faixa_3 = switch_var_3.get()
    hora_inicio_3 = hora_inicio_entry_3.get()
    hora_final_3 = hora_final_entry_3.get()
    
    result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
    
   

    if "Conectado" in result.stdout or "Conected" in result.stdout:
        # o wifi esta ligado
        status_label.config(text="Wi-Fi Ligado")
        inHours = "NO"
        if usar_faixa_1 == True and  hora_inicio_1 <= hora_atual and hora_final_1 >= hora_atual:
            inHours = "YES"
        if usar_faixa_2 == True and hora_inicio_2 <= hora_atual and hora_final_2 >= hora_atual:
            inHours = "YES"
        if usar_faixa_3 == True and hora_inicio_3 <= hora_atual and hora_final_3 >= hora_atual:
            inHours = "YES"

        if(inHours == "NO"):
            # Está fora do horário, desligue o Wi-Fi
            comando = 'netsh wlan disconnect'
            subprocess.run(comando, shell=True)
            status_label.config(text="Desconectado da rede")
            status_label.config(text="Wi-Fi desligado")
    else:
        # o wifi esta desligado
        status_label.config(text="Wi-Fi desligado")
        inHours = "NO"
        if usar_faixa_1 == True and  hora_inicio_1 <= hora_atual and hora_final_1 >= hora_atual :
            inHours = "YES"
        if usar_faixa_2 == True and hora_inicio_2 <= hora_atual and hora_final_2 >= hora_atual:
            inHours = "YES"
        if usar_faixa_3 == True and hora_inicio_3 <= hora_atual and hora_final_3 >= hora_atual:
            inHours = "YES"

        if inHours == "YES":
            # Está dentro do horário, ligue o Wi-Fi
            # subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', shell=True)
            ssid = ssid_entry.get()
            senha = senha_entry.get()
            comando = f'netsh wlan set profileparameter name="{ssid}" keyMaterial="{senha}"'
            subprocess.run(comando, shell=True)
            comando = f'netsh wlan connect name="{ssid}"'
            subprocess.run(comando, shell=True)
            status_label.config(text=f"Conectado à rede: {ssid}")
            

    # Agende a próxima verificação em 15 segundos
    window.after(15000, verificar_horario_wifi)



def salvar_valores():
    valores = {
        "ssid": ssid_entry.get(),
        "senha": senha_entry.get(),
        "usar_horario_1": str(switch_var_1.get()),
        "hora_inicio_1": hora_inicio_entry_1.get(),
        "hora_final_1": hora_final_entry_1.get(),

        "usar_horario_2": str(switch_var_2.get()),
        "hora_inicio_2": hora_inicio_entry_2.get(),
        "hora_final_2": hora_final_entry_2.get(),

        "usar_horario_3": str(switch_var_3.get()),
        "hora_inicio_3": hora_inicio_entry_3.get(),
        "hora_final_3": hora_final_entry_3.get()
    }

    with open('valores.json', 'w') as json_file:
        json.dump(valores, json_file)
        status_label.config(text="Salvo com sucesso!")    
        
def carregar_valores():
    try:
        with open('valores.json', 'r') as json_file:
            valores = json.load(json_file)
            ssid_entry.delete(0, 'end')
            ssid_entry.insert(0, valores["ssid"])
            senha_entry.delete(0, 'end')
            senha_entry.insert(0, valores["senha"])
            
            switch_var_1.set(eval(valores["usar_horario_1"])) 
            hora_inicio_entry_1.delete(0, 'end')
            hora_inicio_entry_1.insert(0, valores["hora_inicio_1"])
            hora_final_entry_1.delete(0, 'end')
            hora_final_entry_1.insert(0, valores["hora_final_1"])

            switch_var_2.set(eval(valores["usar_horario_2"])) 
            hora_inicio_entry_2.delete(0, 'end')
            hora_inicio_entry_2.insert(0, valores["hora_inicio_2"])
            hora_final_entry_2.delete(0, 'end')
            hora_final_entry_2.insert(0, valores["hora_final_2"])

            switch_var_3.set(eval(valores["usar_horario_3"])) 
            hora_inicio_entry_3.delete(0, 'end')
            hora_inicio_entry_3.insert(0, valores["hora_inicio_3"])
            hora_final_entry_3.delete(0, 'end')
            hora_final_entry_3.insert(0, valores["hora_final_3"])

    except FileNotFoundError:
        # Se o arquivo não existe, use os valores padrão
        switch_var_1.set(True) 
        hora_inicio_entry_1.insert(0, "01:30")
        hora_final_entry_1.insert(0, "07:30")

        switch_var_2.set(False) 
        hora_inicio_entry_2.insert(0, "08:00")
        hora_final_entry_2.insert(0, "12:30")

        switch_var_3.set(True) 
        hora_inicio_entry_3.insert(0, "13:30")
        hora_final_entry_3.insert(0, "18:00")

def control_valid_system():
    # Defina a data de referência (30/10/2023)
    data_referencia = datetime.date(2023, 10, 29)
    # Obtenha a data atual
    data_atual = datetime.date.today()
    # Verifique se a data atual é maior do que a data de referência
    if data_atual > data_referencia:
        print(" # # # # # DEMO FINALIZADA , OBRIGADO ! # # # # # ")
        sys.exit()  # Encerra o programa


        
# Configuração da janela tkinter
window = tk.Tk()
window.title("Gerenciador de Wi-Fi")
window.iconbitmap("iconApp.ico")

# Lista de redes Wi-Fi
redes_wifi = tk.Text(window, height=10, width=40, state="disabled")
redes_wifi.grid(row=0, column=0, columnspan=2)

# Input para o nome da rede e senha
ssid_label = tk.Label(window, text="Nome da Rede (SSID):")
ssid_label.grid(row=1, column=0)
ssid_entry = tk.Entry(window)
ssid_entry.grid(row=1, column=1)
senha_label = tk.Label(window, text="Senha:")
senha_label.grid(row=2, column=0)
senha_entry = tk.Entry(window, show="*")
senha_entry.grid(row=2, column=1)



# Botões
listar_button = tk.Button(window, text="Listar Redes Wi-Fi", command=listar_redes_wifi)
listar_button.grid(row=3, column=0)
connect_button = tk.Button(window, text="Conectar", command=conectar_wifi)
connect_button.grid(row=3, column=1)
disconnect_button = tk.Button(window, text="Desconectar", command=desconectar_wifi)
disconnect_button.grid(row=4, column=0, columnspan=2)

#################################


##############################################

switch_var_1 = tk.BooleanVar()
switch_var_1.set(True)  

switch_1 = tk.Checkbutton(window, variable=switch_var_1, )
switch_1.grid(row=6, column=1)  # Posicione o switch à direita do campo de entrada

label_1 = tk.Label(window, text="==== Horário 1 ====")
label_1.grid(row=6, column=0)
hora_inicio_label_1 = tk.Label(window, text="Horário de Início (HH:MM):")
hora_inicio_label_1.grid(row=7, column=0)

hora_inicio_entry_1 = tk.Entry(window , width=5)
hora_inicio_entry_1.insert(0, "")  # Valor padrão
hora_inicio_entry_1.grid(row=7, column=1)

hora_final_label_1 = tk.Label(window, text="Horário Final (HH:MM):")
hora_final_label_1.grid(row=8, column=0)

hora_final_entry_1 = tk.Entry(window , width=5)
hora_final_entry_1.insert(0, "")  # Valor padrão
hora_final_entry_1.grid(row=8, column=1)



#################################

switch_var_2 = tk.BooleanVar()
switch_var_2.set(True)  

switch_2 = tk.Checkbutton(window, variable=switch_var_2)
switch_2.grid(row=10, column=1)  # Posicione o switch à direita do campo de entrada

label_2 = tk.Label(window, text="==== Horário 2 ====")
label_2.grid(row=10, column=0)
hora_inicio_label_2 = tk.Label(window, text="Horário de Início (HH:MM):")
hora_inicio_label_2.grid(row=11, column=0)

hora_inicio_entry_2 = tk.Entry(window , width=5)
hora_inicio_entry_2.insert(0, "")  # Valor padrão
hora_inicio_entry_2.grid(row=11, column=1)

hora_final_label_2 = tk.Label(window, text="Horário Final (HH:MM):")
hora_final_label_2.grid(row=12, column=0)

hora_final_entry_2 = tk.Entry(window , width=5)
hora_final_entry_2.insert(0, "")  # Valor padrão
hora_final_entry_2.grid(row=12, column=1)



#################################

switch_var_3 = tk.BooleanVar()
switch_var_3.set(True)  

switch_3 = tk.Checkbutton(window, variable=switch_var_3)
switch_3.grid(row=14, column=1)  # Posicione o switch à direita do campo de entrada

label_3 = tk.Label(window, text="==== Horário 3 ====")
label_3.grid(row=14, column=0)
hora_inicio_label_3 = tk.Label(window, text="Horário de Início (HH:MM):")
hora_inicio_label_3.grid(row=15, column=0)

hora_inicio_entry_3 = tk.Entry(window , width=5)
hora_inicio_entry_3.insert(0, "")  # Valor padrão
hora_inicio_entry_3.grid(row=15, column=1)

hora_final_label_3 = tk.Label(window, text="Horário Final (HH:MM):")
hora_final_label_3.grid(row=16, column=0)

hora_final_entry_3 = tk.Entry(window , width=5)
hora_final_entry_3.insert(0, "")  # Valor padrão
hora_final_entry_3.grid(row=16, column=1)



##############################################

salve_horario_button = tk.Button(window, text="Salvar", command=salvar_valores)
salve_horario_button.grid(row=17, column=0, columnspan=2)

# Status
status_label = tk.Label(window, text="")
status_label.grid(row=18, column=0, columnspan=2)


# Texto do rótulo
texto = "# # # Gerenciador de WIFI v1.1 # # #"
texto += "\nRenan Dutra Ferreira   < - - Desenvolvedor"
texto += "\n @_fdutra  < - - Instagram para contato"
# Crie um rótulo e use o gerenciador 'grid' para posicionar
label = tk.Label(window, text=texto)
label.grid(row=19, column=0, columnspan=2, padx=10, pady=10)


control_valid_system()

listar_redes_wifi()
carregar_valores()
verificar_horario_wifi()
window.mainloop()
