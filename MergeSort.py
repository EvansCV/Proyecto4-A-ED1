# Código de implementación genérica para el MergeSort con enteros.
# Hay que corregirla porque esto fue una traducción literal de Java hecha por Evans y al parecer no funciona.

class MSort:
    def merge_sort(self, arr):
        # Caso base: una lista con 0 o 1 elementos ya está ordenada
        if len(arr) <= 1:
            return arr

        # Dividir la lista en dos mitades
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        # Combinar las dos mitades ordenadas
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i, j = 0, 0

        # Comparar elementos de ambas listas y agregarlos en orden
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Agregar los elementos restantes, si es que hay
        result.extend(left[i:])
        result.extend(right[j:])
        return result

