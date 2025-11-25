class NodoAVL:
    """Nodo de un Árbol AVL."""
    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.izquierdo: NodoAVL | None = None
        self.derecho: NodoAVL | None = None
        self.altura: int = 1

    def factor_equilibrio(self) -> int:
        alt_izq = self.izquierdo.altura if self.izquierdo else 0
        alt_der = self.derecho.altura if self.derecho else 0
        return alt_izq - alt_der

    def __repr__(self) -> str:
        return f"NodoAVL(valor={self.valor}, altura={self.altura})"


class ArbolAVL:
    """Árbol AVL (ABB auto-balanceado)."""
    def __init__(self) -> None:
        self.raiz: NodoAVL | None = None

    def _altura(self, nodo: NodoAVL | None) -> int:
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo: NodoAVL) -> None:
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        x = y.izquierdo
        assert x is not None
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        y = x.derecho
        assert y is not None
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo: NodoAVL) -> NodoAVL:
        fe = nodo.factor_equilibrio()

        # LL
        if fe > 1 and nodo.izquierdo and nodo.izquierdo.factor_equilibrio() >= 0:
            return self._rotar_derecha(nodo)
        # LR
        if fe > 1 and nodo.izquierdo and nodo.izquierdo.factor_equilibrio() < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        # RR
        if fe < -1 and nodo.derecho and nodo.derecho.factor_equilibrio() <= 0:
            return self._rotar_izquierda(nodo)
        # RL
        if fe < -1 and nodo.derecho and nodo.derecho.factor_equilibrio() > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        return nodo

    def insertar(self, valor: int) -> None:
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo: NodoAVL | None, valor: int) -> NodoAVL:
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        else:
            nodo.derecho = self._insertar(nodo.derecho, valor)

        self._actualizar_altura(nodo)
        return self._balancear(nodo)

    def eliminar(self, valor: int) -> None:
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo: NodoAVL | None, valor: int) -> NodoAVL | None:
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar(nodo.derecho, valor)
        else:
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            sucesor = self._min_nodo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.valor)

        self._actualizar_altura(nodo)
        return self._balancear(nodo)

    def _min_nodo(self, nodo: NodoAVL) -> NodoAVL:
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

    def buscar(self, valor: int) -> bool:
        n = self.raiz
        while n:
            if valor == n.valor:
                return True
            n = n.izquierdo if valor < n.valor else n.derecho
        return False

    def inorden(self) -> list[int]:
        res: list[int] = []
        def _in(n: NodoAVL | None) -> None:
            if n:
                _in(n.izquierdo)
                res.append(n.valor)
                _in(n.derecho)
        _in(self.raiz)
        return res

    def preorden(self) -> list[int]:
        res: list[int] = []
        def _pre(n: NodoAVL | None) -> None:
            if n:
                res.append(n.valor)
                _pre(n.izquierdo)
                _pre(n.derecho)
        _pre(self.raiz)
        return res

    def postorden(self) -> list[int]:
        res: list[int] = []
        def _post(n: NodoAVL | None) -> None:
            if n:
                _post(n.izquierdo)
                _post(n.derecho)
                res.append(n.valor)
        _post(self.raiz)
        return res

    def amplitud(self) -> list[int]:
        if self.raiz is None:
            return []
        resultado: list[int] = []
        cola: list[NodoAVL] = [self.raiz]
        i = 0
        while i < len(cola):
            actual = cola[i]
            i += 1
            resultado.append(actual.valor)
            if actual.izquierdo is not None:
                cola.append(actual.izquierdo)
            if actual.derecho is not None:
                cola.append(actual.derecho)
        return resultado