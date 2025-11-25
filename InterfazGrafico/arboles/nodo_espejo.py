from arboles.abb import Nodo, ArbolBinario

class NodoEspejo(ArbolBinario):
    

    def generar_espejo(self) -> 'NodoEspejo':      
        nuevo_arbol = NodoEspejo()
        nuevo_arbol.raiz, _ = self._clonar_espejo_y_contar(self.raiz)
        return nuevo_arbol

    def _clonar_espejo_y_contar(self, nodo: Nodo | None) -> tuple[Nodo | None, int]:
        if nodo is None:
            return None, 0
        nuevo = Nodo(nodo.valor)
        nuevo_izq, izq_count = self._clonar_espejo_y_contar(nodo.hijo_derecho)
        nuevo_der, der_count = self._clonar_espejo_y_contar(nodo.hijo_izquierdo)
        nuevo.hijo_izquierdo = nuevo_izq
        nuevo.hijo_derecho = nuevo_der     
        cambio_actual = 1 if (nodo.hijo_izquierdo or nodo.hijo_derecho) else 0
        return nuevo, izq_count + der_count + cambio_actual
    
    def _clonar_espejo_y_contar(self, nodo: Nodo | None, nivel: int = 1, niveles_espejados=None) -> tuple[Nodo | None, int]:
        if nodo is None:
            return None, 0
        if niveles_espejados is None:
            niveles_espejados = set()
        nuevo = Nodo(nodo.valor)
        nuevo_izq, count_izq = self._clonar_espejo_y_contar(nodo.hijo_derecho, nivel + 1, niveles_espejados)
        nuevo_der, count_der = self._clonar_espejo_y_contar(nodo.hijo_izquierdo, nivel + 1, niveles_espejados)
        nuevo.hijo_izquierdo = nuevo_izq
        nuevo.hijo_derecho = nuevo_der
        if nodo.hijo_izquierdo or nodo.hijo_derecho:
            niveles_espejados.add(nivel)
        return nuevo, len(niveles_espejados)