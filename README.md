# 🦇 BatScan – Scanner de Portas e Serviços

> Um scanner de rede leve e direto ao ponto, feito em Python, com foco em aprendizado de ethical hacking.

---

## 📌 Funcionalidades

- 🔍 Escaneia portas abertas em um host (IP ou domínio)
- 📌 Detecta serviços comuns em portas (HTTP, SSH, FTP, etc)
- 🎯 Detecção básica de sistema operacional via TTL
- 📤 Exporta resultados em `.json` ou `.txt`

---

## 🧪 Demonstração

```bash
$ python batscan.py --ip 192.168.0.1 --export json
[+] Porta 22 aberta (Provavelmente SSH)
[+] Porta 80 aberta (Provavelmente HTTP)
Sistema operacional provável: Linux (TTL=64)
```

- ## 🛠️ Tecnologias
- Python 3.10+
- socket
- json
- subprocess
- re
- os

- ## 🔮 Melhorias Futuras
- Permitir salvar em CSV.
- Usar threading para acelerar o scan.
