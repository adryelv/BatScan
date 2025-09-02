import socket
import subprocess
import platform
import re
import json
import os
import threading
from queue import Queue

# ------------------------------------- SCAN DE PORTAS -------------------------------------
def scan_port(ip, port, result_list):
    # Realiza o scan de uma porta especificada em um IP, armazenando na lista fornecida (result_list)
    # um dicionário com a porta, o serviço associado e o banner, caso a porta esteja aberta.
    # Imprime uma mensagem com os detalhes se a porta estiver aberta. Portas fechadas são ignoradas.
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        service = get_service_name(port)
        banner = grab_banner(ip, port)
        result_list.append({"porta": port, "servico": service, "banner": banner})
        print(f"[+] Porta {port} aberta - Serviço: {service} - Banner: {banner}")
    except:
        pass
    finally:
        s.close()

def get_service_name(port):
    # Retorna o nome do serviço associado à porta, se for conhecida. Caso contrário, retorna "Desconhecido"
    try:
        return socket.getservbyport(port) # Retorna o nome padrão de um serviço (como "http", "ssh", etc), de acordo com a IANA
    except:
        return "Desconhecido"

# ------------------------------------- BANNER GRABBING -------------------------------------
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        # Tenta receber um banner do serviço
        banner = s.recv(1024).decode(errors="ignore").strip()
        return banner if banner else "Nenhum banner"
    except:
        return "Falhou"
    finally:
        s.close()

# ------------------------------------- DETECÇÃO DE SO -------------------------------------
def detect_ttl(ip):
    # Executa um ping para o IP/domínio fornecido, extrai o valor do TTL da resposta usando regex. 
    # Com base no valor do TTL, tenta inferir o sistema operacional do host (Linux, Windows Roteador/Outro).
    # Retorna uma string descritiva com o valor do TTL e a possível identificação do sistema, ou uma mensagem de erro.
    command = ["ping", "-c", "1", ip] if platform.system() != "windows" else ["ping", "-n", "1", ip]

    try:
        response = subprocess.check_output(command, universal_newlines=True)
        match = re.search(r"ttl=(\d+)", response.lower())
        if match:
            ttl = int(match.group(1))
            if ttl <= 64:
                os_name = "Provavelmente Linux/Unix"
            elif ttl <= 128:
                os_name = "Provavelmente Windows"
            else:
                os_name = "Provavelmente Roteador/Outro"
            return ttl, os_name
        else:
            return None, "TTL não encontrado"
    except Exception as e:
        return None, f"Erro ao pingar: {e}"

# ------------------------------------- MULTITHREADING -------------------------------------
def threader(ip, q, result_list):
    while not q.empty():
        port = q.get()
        scan_port(ip, port, result_list)
        q.task_done()

# ------------------------------------- MAIN -------------------------------------
ip = input("Digite o IP ou domínio: ")

print("\n🔍 Detectando o sistema operacional via TTL...")
ttl, system = detect_ttl(ip)
print(f"{system} (TTL={ttl})" if ttl else system)

print("\n🔍 Escaneando portas abertas...\n")

# Cria um dicionário que armazena as informações para exportar depois.
result = {
    "ip": ip,
    "sistema_operacional": system,
    "ttl": ttl,
    "portas_abertas": []
}

# Fila de portas
q = Queue()
for port in range(1, 1025):
    q.put(port)

# Cria threads
threads = []
for _ in range(50): # Número de threads
    t = threading.Thread(target=threader, args=(ip, q, result["portas_abertas"]))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# ------------------------------------- EXPORT -------------------------------------
export = input("\nDeseja exportar os resultados? (s/n): ").lower()
# Exporta o resultado do scan para json ou txt e envia para a pasta results.
os.makedirs("results", exist_ok=True)
if export == 's':
    format = input("Formato de exportação desejável? (json/txt): ").lower()    
    if format == 'json':
        # Com 'with open' abre um arquivo, nesse caso 'resultado_scan.json ou resultado_scan.txt'. "w" escreve o resultado do scan e armazena em result.
        with open("results/result_scan.json", "w") as f:
            json.dump(result, f, indent=4)
        print("✅ Resultado salvo em results/resultado_scan.json")

    elif format == 'txt':
        with open("results/result_scan.txt", "w") as f:
            f.write(f"IP escaneado: {ip}\n")
            f.write(f"Sistema operacional: {system} (TTL={ttl})\n\n")
            f.write("Portas abertas:\n")
            for item in result["portas_abertas"]:
                f.write(f"- Porta {item['porta']} → Serviço: {item['servico']} → Banner {item['banner']}\n")
        print("✅ Resultado salvo em results/resultado_scan.txt")

    else:
        print("❌ Formato não suportado.")
