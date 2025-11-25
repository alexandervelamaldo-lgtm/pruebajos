from flask import Flask, render_template, request, jsonify
import json
from arboles.abb import ArbolBinario
from arboles.avl import ArbolAVL
from arboles.mvias import ArbolMVias
from arboles.nodo_espejo import NodoEspejo

app = Flask(__name__)

# Instancias globales de los árboles
arbol_abb = ArbolBinario()
arbol_avl = ArbolAVL()
arbol_mvias = ArbolMVias(m=3)  # Árbol 3-vías por defecto

valores_por_defecto = [100, 50, 150, 25, 175,15,180]
for v in valores_por_defecto:
    arbol_abb.insertar(v)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insertar', methods=['POST'])
def insertar():
    data = request.json
    valor = int(data['valor'])
    tipo_arbol = data['tipo_arbol']
    
    if tipo_arbol == 'abb':
        arbol_abb.insertar(valor)
        return jsonify({'mensaje': f'Valor {valor} insertado en ABB'})
    elif tipo_arbol == 'avl':
        arbol_avl.insertar(valor)
        return jsonify({'mensaje': f'Valor {valor} insertado en AVL'})
    else:  # mvias
        arbol_mvias.insertar(valor)
        return jsonify({'mensaje': f'Valor {valor} insertado en Árbol M-Vías'})

@app.route('/espejo', methods=['GET'])
def obtener_espejo():
    """Genera y retorna el árbol espejo del ABB actual."""
    global arbol_abb
    if arbol_abb.raiz is None:
        return jsonify({'mensaje': 'El ABB está vacío, no hay espejo para generar', 'arbol': None})

    # Crear el árbol espejo y contar los cambios
    espejo = NodoEspejo()
    espejo.raiz = arbol_abb.raiz
    arbol_espejo = NodoEspejo()
    arbol_espejo.raiz, cantidad_cambios = espejo._clonar_espejo_y_contar(arbol_abb.raiz)

    # Convertir el árbol espejo a JSON
    def nodo_a_dict(nodo):
        if nodo is None:
            return None
        return {
            'tipo': 'binario',
            'valor': nodo.valor,
            'izquierdo': nodo_a_dict(nodo.hijo_izquierdo),
            'derecho': nodo_a_dict(nodo.hijo_derecho)
        }

    raiz_dict = nodo_a_dict(arbol_espejo.raiz)

    return jsonify({
        'mensaje': f'Árbol espejo generado correctamente (nodos espejados: {cantidad_cambios})',
        'cantidad': cantidad_cambios,
        'arbol': raiz_dict
    })

@app.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.json
    valor = int(data['valor'])
    tipo_arbol = data['tipo_arbol']

    if tipo_arbol == 'abb':
        arbol_abb.eliminar(valor)
        return jsonify({'mensaje': f'Valor {valor} eliminado del ABB (si existía)'})
    elif tipo_arbol == 'avl':
        arbol_avl.eliminar(valor)
        return jsonify({'mensaje': f'Valor {valor} eliminado del AVL'})
    else:
        return jsonify({'mensaje': 'Eliminación no implementada para M-Vías'})



@app.route('/recorrido/<tipo>', methods=['GET'])
def obtener_recorrido(tipo):
    tipo_arbol = request.args.get('tipo_arbol', 'abb')
    
    if tipo_arbol == 'abb':
        arbol = arbol_abb
    elif tipo_arbol == 'avl':
        arbol = arbol_avl
    else:  # mvias
        arbol = arbol_mvias
    
    if tipo == 'inorden':
        resultado = arbol.inorden_recursivo() if hasattr(arbol, 'inorden_recursivo') else arbol.inorden()
    elif tipo == 'preorden':
        resultado = arbol.preorden_recursivo() if hasattr(arbol, 'preorden_recursivo') else arbol.preorden()
    elif tipo == 'postorden':
        resultado = arbol.postorden_recursivo() if hasattr(arbol, 'postorden_recursivo') else arbol.postorden()
    elif tipo == 'amplitud':
        resultado = arbol.amplitud() if hasattr(arbol, 'amplitud') else []
    else:
        resultado = []
    
    return jsonify({'recorrido': resultado})

@app.route('/estructura', methods=['GET'])
def obtener_estructura():
    tipo_arbol = request.args.get('tipo_arbol', 'abb')
    
    if tipo_arbol == 'abb':
        arbol = arbol_abb
    elif tipo_arbol == 'avl':
        arbol = arbol_avl
    else:  # mvias
        arbol = arbol_mvias
    
    # Convertir el árbol a una estructura JSON para visualización
    def nodo_a_dict(nodo):
        if nodo is None:
            return None
        
        # Para árboles M-Vías
        if hasattr(nodo, 'valores') and hasattr(nodo, 'hijos'):
            return {
                'tipo': 'mvias',
                'valores': nodo.valores,
                'hijos': [nodo_a_dict(hijo) for hijo in nodo.hijos] if hasattr(nodo, 'hijos') else []
            }
        # Para árboles binarios
        else:
            return {
                'tipo': 'binario',
                'valor': nodo.valor,
                'izquierdo': nodo_a_dict(nodo.hijo_izquierdo if hasattr(nodo, 'hijo_izquierdo') else nodo.izquierdo),
                'derecho': nodo_a_dict(nodo.hijo_derecho if hasattr(nodo, 'hijo_derecho') else nodo.derecho)
            }
    
    raiz_dict = nodo_a_dict(arbol.raiz)
    return jsonify({'arbol': raiz_dict, 'tipo': tipo_arbol})

@app.route('/configurar_mvias', methods=['POST'])
def configurar_mvias():
    data = request.json
    m = int(data['m'])
    
    global arbol_mvias
    arbol_mvias = ArbolMVias(m=m)
    
    return jsonify({'mensaje': f'Árbol M-Vías configurado con grado {m}'})

@app.route('/info_arbol', methods=['GET'])
def obtener_info_arbol():
    tipo_arbol = request.args.get('tipo_arbol', 'abb')
    
    if tipo_arbol == 'abb':
        arbol = arbol_abb
        info = {
            'tipo': 'ABB',
            'altura': arbol.altura(),
            'cantidad_nodos': arbol.cantidad(),
            'cantidad_valores': arbol.cantidad()
        }
    elif tipo_arbol == 'avl':
        arbol = arbol_avl
        info = {
            'tipo': 'AVL',
            'altura': arbol.altura(),
            'cantidad_nodos': 'No disponible',  # Podrías implementar esto
            'cantidad_valores': len(arbol.inorden())
        }
    else:  # mvias
        arbol = arbol_mvias
        info = {
            'tipo': f'M-Vías (grado {arbol.m})',
            'altura': arbol.altura(),
            'cantidad_nodos': arbol.cantidad_nodos(),
            'cantidad_valores': arbol.cantidad_valores()
        }
    
    return jsonify(info)

@app.route('/limpiar', methods=['POST'])
def limpiar_arbol():
    data = request.json
    tipo_arbol = data['tipo_arbol']
    
    if tipo_arbol == 'abb':
        arbol_abb.raiz = None
        return jsonify({'mensaje': 'ABB limpiado'})
    elif tipo_arbol == 'avl':
        arbol_avl.raiz = None
        return jsonify({'mensaje': 'AVL limpiado'})
    else:  # mvias
        arbol_mvias.raiz = None
        return jsonify({'mensaje': 'Árbol M-Vías limpiado'})

if __name__ == '__main__':
    app.run(debug=True)