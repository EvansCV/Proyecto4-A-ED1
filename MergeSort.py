# Código de implementación genérica para el MergeSort con enteros.
# Hay que corregirla porque esto fue una traducción literal de Java hecha por Evans y al parecer no funciona.
def merge_sort(array, low, high): # [14, 7, 3, 12, 9, 11, 6, 2]
    if low < high:
        mid = (low + high) // 2
        mid = mid.__round__()
        merge_sort(array, low, mid)
        merge_sort(array, mid + 1, high)
        merge(array, low, high, mid)
    return


def merge(array, low, high, mid):
    # arreglo temporal
    c = []
    i = low
    k = low
    j = mid + 1
    while i <= mid and j <= high:
        if array[i] < array[j]:
            c[k] = array[i]
            k += 1
            i += 1
        else:
            c[k] = array[j]
            k += 1
            j += 1
    while i <= mid:
        c[k] = array[i]
        k += 1
        i += 1
    while j <= high:
        c[k] = array[j]
        k += 1
        j += 1
    for i in range(low, k):
        array[i] = c[i]


a = [14, 7, 3, 12, 9, 11, 6, 2]
print(merge_sort(a, 0, len(a)-1))