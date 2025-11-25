"""
Módulo ArbolMVias
=================

Implementación de un Árbol M-Vías (árbol de búsqueda multiway).
"""

from typing import Optional, List


class NodoMVias:
    """Nodo de un Árbol M-Vías."""

    def __init__(self, m: int) -> None:
        if m < 3:
            raise ValueError("El grado m debe ser al menos 3")
        
        self.m: int = m
        self.valores: List[int] = []
        self.hijos: List[Optional['NodoMVias']] = [None] * m
    
    def esta_lleno(self) -> bool:
        """Indica si el nodo está lleno (tiene m-1 valores)."""
        return len(self.valores) == self.m - 1
    
    def es_hoja(self) -> bool:
        """Indica si el nodo es una hoja (todos los hijos son None)."""
        return all(hijo is None for hijo in self.hijos)
    
    def cantidad_valores(self) -> int:
        """Retorna la cantidad de valores almacenados en el nodo."""
        return len(self.valores)
    
    def insertar_valor(self, valor: int) -> int:
        """
        Inserta un valor en el nodo manteniendo el orden.
        
        Returns:
            int: Posición donde se insertó el valor
        """
        if self.esta_lleno():
            raise ValueError("El nodo está lleno, no se pueden insertar más valores")
        
        # Encontrar la posición correcta para insertar
        posicion = 0
        while posicion < len(self.valores) and self.valores[posicion] < valor:
            posicion += 1
        
        # Insertar el valor en la posición encontrada
        self.valores.insert(posicion, valor)
        return posicion
    
    def obtener_hijo_para_valor(self, valor: int) -> int:
        """
        Obtiene el índice del hijo apropiado para un valor dado.
        
        Returns:
            int: Índice del hijo donde debería estar el valor
        """
        for i in range(len(self.valores)):
            if valor < self.valores[i]:
                return i
        return len(self.valores)
    
    def __repr__(self) -> str:
        return f"NodoMVias(m={self.m}, valores={self.valores})"


class ArbolMVias:
    """Árbol M-Vías (árbol de búsqueda multiway)."""
    
    def __init__(self, m: int = 3) -> None:
        if m < 3:
            raise ValueError("El grado m debe ser al menos 3")
        
        self.m: int = m
        self.raiz: Optional[NodoMVias] = None
    
    def insertar(self, valor: int) -> None:
        """Inserta un valor en el árbol M-Vías."""
        if self.raiz is None:
            self.raiz = NodoMVias(self.m)
            self.raiz.valores.append(valor)
            return
        
        # Si la raíz está llena, necesitamos dividirla
        if self.raiz.esta_lleno():
            nueva_raiz = NodoMVias(self.m)
            nueva_raiz.hijos[0] = self.raiz
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
        
        self._insertar_no_lleno(self.raiz, valor)
    
    def _insertar_no_lleno(self, nodo: NodoMVias, valor: int) -> None:
        """Inserta un valor en un nodo que no está lleno."""
        i = len(nodo.valores) - 1
        
        # Si es hoja, insertar directamente
        if nodo.es_hoja():
            while i >= 0 and valor < nodo.valores[i]:
                i -= 1
            nodo.valores.insert(i + 1, valor)
        else:
            # Encontrar el hijo apropiado
            while i >= 0 and valor < nodo.valores[i]:
                i -= 1
            i += 1
            
            # Si el hijo está lleno, dividirlo
            if nodo.hijos[i] and nodo.hijos[i].esta_lleno():
                self._dividir_hijo(nodo, i)
                if valor > nodo.valores[i]:
                    i += 1
            
            self._insertar_no_lleno(nodo.hijos[i], valor)
    
    def _dividir_hijo(self, padre: NodoMVias, indice_hijo: int) -> None:
        """Divide un hijo lleno del nodo padre."""
        hijo = padre.hijos[indice_hijo]
        if hijo is None:
            return
        
        nuevo_hijo = NodoMVias(self.m)
        medio = self.m // 2
        
        # Mover valores al nuevo hijo
        nuevo_hijo.valores = hijo.valores[medio + 1:]
        hijo.valores = hijo.valores[:medio]
        
        # Mover hijos si no es hoja
        if not hijo.es_hoja():
            nuevo_hijo.hijos = hijo.hijos[medio + 1:]
            hijo.hijos = hijo.hijos[:medio + 1] + [None] * (self.m - medio - 1)
        
        # Insertar el valor medio en el padre
        valor_medio = hijo.valores.pop()
        padre.valores.insert(indice_hijo, valor_medio)
        padre.hijos.insert(indice_hijo + 1, nuevo_hijo)
        
        # Ajustar la lista de hijos
        padre.hijos = padre.hijos[:self.m]
    
    def buscar(self, valor: int) -> bool:
        """Busca un valor en el árbol M-Vías."""
        return self._buscar(self.raiz, valor)
    
    def _buscar(self, nodo: Optional[NodoMVias], valor: int) -> bool:
        """Búsqueda recursiva de un valor."""
        if nodo is None:
            return False
        
        # Buscar en los valores del nodo actual
        for i, val in enumerate(nodo.valores):
            if valor == val:
                return True
            if valor < val:
                return self._buscar(nodo.hijos[i], valor)
        
        # Buscar en el último hijo
        return self._buscar(nodo.hijos[len(nodo.valores)], valor)
    
    def inorden(self) -> List[int]:
        """Recorrido inorden del árbol M-Vías."""
        resultado: List[int] = []