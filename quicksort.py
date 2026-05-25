"""
Práctica: Diseño de algoritmos recursivos
Módulo  : Quick sort recursivo

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.

Recuerda identificar en tus comentarios:
    # PASO BASE
    # HIPÓTESIS INDUCTIVA (como comentario en prosa)
    # PASO RECURSIVO
"""
import time
import random
import sys

# Aumentamos el límite para evitar RecursionError en el peor caso (arreglos ordenados)
sys.setrecursionlimit(200_000)

# ---------------------------------------------------------------------------
# Problema A – Partición de Lomuto
# ---------------------------------------------------------------------------

def particiona(arr: list, lo: int, hi: int) -> int:
    """
    Reorganiza arr[lo..hi] en torno al pivote arr[hi] (esquema Lomuto).
    """
    pivot = arr[hi]
    i = lo - 1

    for j in range(lo, hi):
        # TODO COMPLETADO: si arr[j] <= pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # TODO COMPLETADO: coloca el pivote en su posición definitiva
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def particiona_aleatoria(arr: list, lo: int, hi: int) -> int:
    """
    Igual que particiona, pero elige el pivote al azar.
    """
    # TODO COMPLETADO: elige un índice aleatorio e intercambia
    idx = random.randint(lo, hi)
    arr[idx], arr[hi] = arr[hi], arr[idx]
    return particiona(arr, lo, hi)


# ---------------------------------------------------------------------------
# Problema B – Quick sort recursivo
# ---------------------------------------------------------------------------

def quicksort(arr: list, lo: int = 0, hi: int = None) -> None:
    if hi is None:
        hi = len(arr) - 1

    # PASO BASE: si lo >= hi, el subarreglo tiene 0 o 1 elemento
    if lo >= hi:
        return

    # PASO RECURSIVO
    # 1. Obtener posición del pivote
    p = particiona(arr, lo, hi)
    
    # 2. Llamada izquierda (antes del pivote)
    quicksort(arr, lo, p - 1)
    
    # 3. Llamada derecha (después del pivote)
    quicksort(arr, p + 1, hi)


def quicksort_aleatorio(arr: list, lo: int = 0, hi: int = None) -> None:
    if hi is None:
        hi = len(arr) - 1

    if lo >= hi:
        return

    # TODO: mismo esquema que quicksort, pero llamando a particiona_aleatoria
    p = particiona_aleatoria(arr, lo, hi)
    quicksort_aleatorio(arr, lo, p - 1)
    quicksort_aleatorio(arr, p + 1, hi)

# ---------------------------------------------------------------------------
# Problema D – Versión instrumentada
# ---------------------------------------------------------------------------

def _particiona_conteo(arr: list, lo: int, hi: int, conteo: list, aleatorio: bool = False) -> int:
    if aleatorio:
        idx = random.randint(lo, hi)
        arr[idx], arr[hi] = arr[hi], arr[idx]
        
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        conteo[0] += 1  # comparación
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1

def quicksort_conteo(arr: list, lo: int, hi: int, conteo: list, aleatorio: bool = False) -> None:
    if lo >= hi:
        return
    p = _particiona_conteo(arr, lo, hi, conteo, aleatorio)
    quicksort_conteo(arr, lo, p - 1, conteo, aleatorio)
    quicksort_conteo(arr, p + 1, hi, conteo, aleatorio)

# ---------------------------------------------------------------------------
# Pruebas y Experimentos
# ---------------------------------------------------------------------------

def _pruebas_particion():
    A = [3, 6, 8, 10, 1, 2, 1]
    p = particiona(A, 0, 6)
    assert A[p] == 1
    assert all(v <= 1 for v in A[:p])
    assert all(v >= 1 for v in A[p+1:])
    print(f"✓ Partición correcta: {A}, pivote en índice {p}")

def _pruebas_quicksort():
    casos = [[], [1], [2, 1], [3, 1, 4, 1, 5, 9, 2, 6], list(range(100, 0, -1))]
    for arr in casos:
        ref = sorted(arr)
        quicksort(arr)
        assert arr == ref
    print("✓ Quick sort correcto en todos los casos de prueba.")

def _experimento_comparaciones():
    print(f"\n{'n':>8} {'aleatorio':>12} {'ordenado (fijo)':>17} {'ordenado (random)':>19}")
    print("-" * 62)
    for n in [100, 500, 1000, 2000]:
        # Aleatorio
        c_al = [0]; quicksort_conteo(list(range(n)), 0, n-1, c_al, True)
        # Ordenado Fijo
        c_ord = [0]; quicksort_conteo(list(range(n)), 0, n-1, c_ord, False)
        # Ordenado Aleatorio
        c_rand = [0]; quicksort_conteo(list(range(n)), 0, n-1, c_rand, True)
        print(f"{n:>8,} {c_al[0]:>12,} {c_ord[0]:>17,} {c_rand[0]:>19,}")

def _experimento_tiempo():
    print(f"\n{'n':>10} {'T_quicksort (ms)':>18} {'T_sorted (ms)':>15} {'Razón':>8}")
    print("-" * 56)
    for n in [1000, 10000, 100000]:
        arr_orig = [random.randint(0, n) for _ in range(n)]
        
        t0 = time.perf_counter()
        quicksort(arr_orig.copy())
        t_qs = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        sorted(arr_orig)
        t_so = (time.perf_counter() - t0) * 1000

        print(f"{n:>10,} {t_qs:>18.3f} {t_so:>15.3f} {t_qs/t_so:>8.2f}x")

if __name__ == "__main__":
    print("=" * 60)
    print("Quick sort recursivo")
    print("=" * 60)
    _pruebas_particion()
    _pruebas_quicksort()
    _experimento_comparaciones()
    _experimento_tiempo()
