import socket
import subprocess
import platform
import re
import json
import os

def scan_port(ip, port):
    # Realiza o escaneamento da porta especificada, retornando True se estiver aberta
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()

def get_service_name(port):
    # Retorna o nome do serviço associado à porta, se for conhecida. Caso contrário, retorna "Desconhecido"
    try:
        return socket.getservbyport(port) # Retorna o nome padrão de um serviço (como "http", "ssh", etc), de acordo com a IANA
    except:
        return "Desconhecido"

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

for port in range(1, 1025):
    # Faz escaneamento sequencial das portas de 1 à 1024.
    # Para cada porta aberta detecta o serviço, mostra no terminal, armazena no dicionário (result).
    if scan_port(ip, port):
        service = get_service_name(port)
        print(f"[+] Porta {port} aberta - Serviço provável: {service}")
        result["portas_abertas"].append({"porta": port, "servico": service})

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
                f.write(f"- Porta {item['porta']} → Serviço: {item['servico']}\n")
        print("✅ Resultado salvo em results/resultado_scan.txt")

    else:
        print("❌ Formato não suportado.")