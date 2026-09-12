from mpi4py import MPI
import random

# Inicialização do MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# -----------------------------
# Função para gerar logs
# -----------------------------
def gerar_logs(qtd):
    ips = [f"192.168.1.{i}" for i in range(1,255)]
    endpoints = [
    "/",
    "/login",
    "/products",
    "/cart",
    "/checkout",
    "/api/users",
    "/api/orders"
    ]
    metodos = ["GET","POST"]
    status = ["200","200","200","404","500"]
    logs = []

    #INSIRA AQUI O SEU CÓDIGO PARA GERAR OS DADOS DO LOG
    for _ in range(qtd):
        ip = random.choice(ips)
        metodo = random.choice(metodos)
        endpoint=  random.choice(endpoints)
        codigo = random.choice(status)
        linha = f"{ip} {metodo} {endpoint} {codigo}"
        logs.append(linha)
    return logs
# -----------------------------
# Processo 0 gera o dataset
# -----------------------------

logs_divididos = None
TOTAL_LOGS = 1000000 

if rank == 0:
    print("\nGerando dataset de logs...\n")
    logs = gerar_logs(TOTAL_LOGS)
    # DIVIDIR AQUI O DATASET ENTRE OS PROCESSOS
    parte = TOTAL_LOGS // size
    logs_divididos = [
        logs[i * parte:(i + 1) * parte]
        for i in range(size)
    ]

    

# -----------------------------
# Distribuição usando Scatter
# -----------------------------
#DISTRIBUIR OS DADOS USANDO SCATTER
logs_locais = comm.scatter(logs_divididos, root=0)

# -----------------------------
# Processamento local
# -----------------------------
#INSIRA AQUI O CÓDIGO DE PROCESSAMENTO LOCAL DO LOG
erros = 0

for log in logs_locais:
    campos = log.split()
    codigo_status = campos[3]
    if codigo_status == "404" or codigo_status == "500":
        erros += 1

# -----------------------------
# Resultado local
# -----------------------------
print(
    f"Processo {rank} analisou {len(logs_locais)} linhas "
    f"e encontrou {erros} erros."
)