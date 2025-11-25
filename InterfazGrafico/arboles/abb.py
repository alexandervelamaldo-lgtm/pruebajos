class Nodo:
    """Clase que representa un nodo de un árbol binario."""

    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.hijo_izquierdo: Nodo | None = None
        self.hijo_derecho: Nodo | None = None

    def __repr__(self) -> str:
        return f"Nodo({self.valor})"


class ArbolBinario:
    """Implementación de un Árbol Binario de Búsqueda (ABB)."""

    def __init__(self) -> None:
        self.raiz: Nodo | None = None

    def insertar(self, valor: int) -> None:
        self.insertar_nodo_recursivo(valor)

    def insertar_nodo_recursivo(self, valor: int) -> None:
        def _insertar(raiz: Nodo | None, valor: int) -> Nodo:
            if raiz is None:
                return Nodo(valor)
            if valor < raiz.valor:
                raiz.hijo_izquierdo = _insertar(raiz.hijo_izquierdo, valor)
            else:
                raiz.hijo_derecho = _insertar(raiz.hijo_derecho, valor)
            return raiz

        self.raiz = _insertar(self.raiz, valor)

    def inorden_recursivo(self) -> list[int]:
        def _in(nodo: Nodo | None, res: list[int]) -> None:
            if nodo:
                _in(nodo.hijo_izquierdo, res)
                res.append(nodo.valor)
                _in(nodo.hijo_derecho, res)

        resultado: list[int] = []
        _in(self.raiz, resultado)
        return resultado

    def preorden_recursivo(self) -> list[int]:
        def _pre(nodo: Nodo | None, res: list[int]) -> None:
            if nodo:
                res.append(nodo.valor)
                _pre(nodo.hijo_izquierdo, res)
                _pre(nodo.hijo_derecho, res)

        resultado: list[int] = []
        _pre(self.raiz, resultado)
        return resultado

    def postorden_recursivo(self) -> list[int]:
        def _post(nodo: Nodo | None, res: list[int]) -> None:
            if nodo:
                _post(nodo.hijo_izquierdo, res)
                _post(nodo.hijo_derecho, res)
                res.append(nodo.valor)

        resultado: list[int] = []
        _post(self.raiz, resultado)
        return resultado

    def amplitud(self) -> list[int]:
        if self.raiz is None:
            return []
        resultado: list[int] = []
        cola: list[Nodo] = [self.raiz]
        i = 0
        while i < len(cola):
            actual = cola[i]
            i += 1
            resultado.append(actual.valor)
            if actual.hijo_izquierdo is not None:
                cola.append(actual.hijo_izquierdo)
            if actual.hijo_derecho is not None:
                cola.append(actual.hijo_derecho)
        return resultado

    def buscar(self, valor: int) -> bool:
        actual = self.raiz
        while actual:
            if valor == actual.valor:
                return True
            if valor < actual.valor:
                actual = actual.hijo_izquierdo
            else:
                actual = actual.hijo_derecho
        return False

    def altura(self) -> int:
        def _h(nodo: Nodo | None) -> int:
            if nodo is None:
                return 0
            return 1 + max(_h(nodo.hijo_izquierdo), _h(nodo.hijo_derecho))

        return _h(self.raiz)

    def cantidad(self) -> int:
        def _contar(nodo: Nodo | None) -> int:
            if nodo is None:
                return 0
            return 1 + _contar(nodo.hijo_izquierdo) + _contar(nodo.hijo_derecho)

        return _contar(self.raiz)
    
    def eliminar(self, valor: int) -> None:
        """Elimina un valor del árbol si existe."""
        def _eliminar(nodo: Nodo | None, valor: int) -> Nodo | None:
            if nodo is None:
                return None

            # Buscar el nodo
            if valor < nodo.valor:
                nodo.hijo_izquierdo = _eliminar(nodo.hijo_izquierdo, valor)
            elif valor > nodo.valor:
                nodo.hijo_derecho = _eliminar(nodo.hijo_derecho, valor)
            else:
                # Encontrado el nodo a eliminar
                if nodo.hijo_izquierdo is None:
                    return nodo.hijo_derecho
                elif nodo.hijo_derecho is None:
                    return nodo.hijo_izquierdo

                # Nodo con dos hijos: reemplazar por el menor del subárbol derecho
                sucesor = self._minimo(nodo.hijo_derecho)
                nodo.valor = sucesor.valor
                nodo.hijo_derecho = _eliminar(nodo.hijo_derecho, sucesor.valor)

            return nodo

        self.raiz = _eliminar(self.raiz, valor)

    def _minimo(self, nodo: Nodo) -> Nodo:
        """Devuelve el nodo con el valor mínimo en un subárbol."""
        actual = nodo
        while actual.hijo_izquierdo is not None:
            actual = actual.hijo_izquierdo
        return actual