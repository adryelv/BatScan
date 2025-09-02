# 🦇 BatScan – Scanner de Portas e Serviços

> Um scanner de rede leve e direto ao ponto, feito em Python, com foco em aprendizado de **ethical hacking**.

---

## 📌 Funcionalidades

- 🔍 Escaneia portas abertas em um host (IP ou domínio)  
- 📌 Detecta serviços comuns em portas (HTTP, SSH, FTP, etc)  
- 🛡️ Identificação inicial de SO pelo valor do TTL  
- 🎚️ Escolha de exportação (`.json` ou `.txt`)  
- ⚡ Multithreading para acelerar o scan  
- 📜 Banner grabbing para identificar serviços com mais precisão  

---

## 🧪 Demonstração

```bash
$ python batscan.py --ip 192.168.0.1 --export json
🔍 Detectando o sistema operacional via TTL...
Sistema operacional provável: Linux (TTL=64)

🔍 Escaneando portas abertas...
[+] Porta 22 aberta - Serviço: ssh - Banner: OpenSSH 7.4
[+] Porta 80 aberta - Serviço: http - Banner: Apache/2.4.29
```

## 🛠️ Tecnologias

**Linguagem**
- Python 3.10+

**Bibliotecas padrão utilizadas:** 
- socket
- subprocess
- re
- os
- json
- threading
- queue
- platform

- ## 🔮 Melhorias Futuras
- 📂 Permitir salvar também em CSV
- 🕵️ Modo “stealth” com scapy (SYN scan, estilo Nmap)
- 🎨 Output colorido no terminal (verde para portas abertas, vermelho para fechadas)
- 🎯 Configuração de intervalo de portas a escanear
- ⚙️ Ajuste de número de threads e timeout
- 💻 Interface CLI com argparse para facilitar o uso via linha de comando

✍️ Desenvolvido para fins de aprendizado em redes e ethical hacking.



# 🦇 BatScan – Port and Service Scanner

> A lightweight and straightforward network scanner built in Python, focused on **ethical hacking** learning.

---

## 📌 Features

- 🔍 Scans open ports on a host (IP or domain)  
- 📌 Detects common services on ports (HTTP, SSH, FTP, etc.)  
- 🛡️ Basic OS fingerprinting through TTL values  
- 🎚️ Export results in `.json` or `.txt`  
- ⚡ Multithreading to speed up scanning  
- 📜 Banner grabbing to identify services with more accuracy  

---

## 🧪 Demonstration

```bash
$ python batscan.py --ip 192.168.0.1 --export json
🔍 Detecting operating system via TTL...
Likely operating system: Linux (TTL=64)

🔍 Scanning open ports...
[+] Port 22 open - Service: ssh - Banner: OpenSSH 7.4
[+] Port 80 open - Service: http - Banner: Apache/2.4.29
```
# 🛠️ Technologies

**Language:**
Python 3.10+

**Standard libraries used:**
- socket
- subprocess
- re
- os
- json
- threading
- queue
- platform

# 🔮 Future Improvements
- 📂 Allow saving results in CSV format
- 🕵️ Add a “stealth mode” using scapy (SYN scan, Nmap-like)
- 🎨 Colored terminal output (green for open ports, red for closed)
- 🎯 Configurable port range to scan
- ⚙️ Adjustable thread count and timeout
- 💻 Command-line interface with argparse for easier usage

✍️ Developed for educational purposes in networking and ethical hacking.
