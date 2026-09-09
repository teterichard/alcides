import random
import time
from mpi4py import MPI

N = 10000000

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Distribui pontos de modo equilibrado entre os processos.
base = N // size
resto = N % size
local_n = base + (1 if rank < resto else 0)

random.seed((rank + 1) * 1234567)
dentro = 0
inicio = time.time()
for _ in range(local_n):
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1:
        dentro += 1

fim = time.time()

total_inside = comm.reduce(dentro, op=MPI.SUM, root=0)
total_points = comm.reduce(local_n, op=MPI.SUM, root=0)

if rank == 0:
    pi = 4.0 * total_inside / total_points
    print(f"PI aproximado: {pi}")
    print(f"Pontos totais: {total_points}")
    print(f"Pontos dentro: {total_inside}")
    print(f"Tempo: {(fim - inicio) * 1000:.2f} ms")

MPI.Finalize()
