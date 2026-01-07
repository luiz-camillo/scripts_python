import subprocess   
import sys
import shlex 

def iniciar_script():
    print("\nOlá, vamos iniciar a checagem SNMP")
    print("\nTestando conectividade com a internet......")

    #IPS de teste (DNS GOOGLE)
    ips_teste =["8.8.8.8", "8.8.4.4"]
    online = False

    for ip in ips_teste:
        #-c 1 (1 pacote), -W (espera 2 segundos)
        teste = subprocess.run(["ping", "-c", "1", "-W", "2", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if teste.returncode == 0:
            online = True
            break

    if online: 
        print("Conexão com a internet confirmada através do teste de ping para os DNS DA GOOGLE (8.8.8.8 e 8.8.4.4)")
    else:
        print ("Sem conexão com a internet, verifique suas configurações de rede e tente novamente!")
        sys.exit()

iniciar_script()


ips = []

print("\n\nAgora informe os IPS dos hosts que iremos checar")

#contador para manter visual quantos ips estão sendo informados 
cont = 0

while True:   

    #antes de adicionar a lista de ips, vou fazer as validações e armazenar o ip em uma variável para depois adicionar na lista
    tmpIp = (input(f"Digite o {cont+1}º IP: (Para seguir tecle Enter)\n")).strip()

    if tmpIp == "":
        break
    else:
        ips.append(tmpIp)
        cont += 1


print(f"\nOk, você informou {cont} IP(S), segue lista para verificação, se digitou algum IP errado feche e execute novamente o script!")


for ip in ips:
    print(ip)
        
input("\nPressione ENTER para continuar para a próxima etapa...")

print("\nA lista de IPs foi configurada com sucesso!\n")

ping = []

for ip in ips:
    print(f"Testando PING para o IP {ip} ...", end=" ", flush=True)
    tmpPing = subprocess.run(["ping", "-c", "1", "-W", "2", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ping.append(tmpPing.returncode)
    print("\n")

community = []

print("\n")
print("\n")

for ip in ips:
    comm = input(f"Digite a community para o Host {ip}: ").strip()
    comm_protegida = shlex.quote(comm)
    community.append(comm_protegida)
    print("\n")

porta = []

print("\n")
print("\n")

for ip in ips:
    p = input(f"Digite a porta snmp para o Host {ip}: (PRESSIONE ENTER PARA PORTA PADRÃO 161)").strip()
    if p == "":
        porta.append("161")
    else:
        porta.append(p)
           

input("\nOk, irei realizar o teste SNMP nos hosts com PING OK (Pressione ENTER para seguir)")

snmp_status = []

for i, ip in enumerate(ips):

    if ping[i] == 0:
        print(f"Iniciando SNMPWALK no Host {ip}")
        comando = ["snmpwalk", "-v2c", "-c", community[i], f"{ip}:{porta[i]}", "sysName"]
        teste_snmp = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if teste_snmp.returncode == 0:
            snmp_status.append(teste_snmp.returncode)
        else:
            snmp_status.append(teste_snmp.returncode)
    else:
        print(f"Host {ip}: Pulado (Sem Ping)")
        snmp_status.append(None)

input("\n\nTodos os testes foram realizados (PRESSIONE ENTER PARA OS RESULTADOS)")

print("\n" + "="*60)
print("              RESULTADOS DA VERIFICAÇÃO")
print("="*60)


for i, ip in enumerate(ips):
    comm_limpa = community[i].replace("'", "")
    print(f"\nHost: {ip} - community: {comm_limpa} - porta snmp: {porta[i]}")

    if ping[i] == 0:
        print("PING OK")
    else:
        print("SEM PING PARA O HOST VERIFIQUE CONECTIVIDADE")

    if snmp_status[i] == 0:
        print("SNMP OK")
    elif snmp_status[i] is None:
        print("SNMP NÃO EXECUTADO (HOST OFFLINE)")
    else:
        print("Timeout SNMP (VERIFIQUE COMMUNITY OU PORTA)")

print("\n" + "="*60)
print("Fim do script.")





