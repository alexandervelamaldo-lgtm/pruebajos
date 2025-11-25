let arbolData = null;
let tipoArbolActual = 'abb';
let canvas = document.getElementById('treeCanvas');
let ctx = canvas.getContext('2d');

function mostrarMensaje(mensaje, esError = false) {
    const elemento = document.getElementById('mensaje');
    elemento.textContent = mensaje;
    elemento.style.color = esError ? 'red' : 'green';
}

function mostrarRecorrido(recorrido, tipo) {
    const elemento = document.getElementById('recorridoResultado');
    elemento.innerHTML = `<strong>${tipo}:</strong> [${recorrido.join(', ')}]`;
}

function mostrarInfoArbol(info) {
    const elemento = document.getElementById('infoArbol');
    elemento.innerHTML = `
        <strong>${info.tipo}</strong> | 
        Altura: ${info.altura} | 
        Nodos: ${info.cantidad_nodos} | 
        Valores: ${info.cantidad_valores}
    `;

    // Mostrar información adicional si viene del espejo (-1 nodo)
    if (info.cantidad_espejo !== undefined) {
        const cantidadAjustada = info.cantidad_espejo - 1;
        elemento.innerHTML += ` | Nodos Espejo: ${cantidadAjustada}`;
    }
}


let modoEspejo = false;

async function mostrarEspejo() {
    const boton = document.querySelector('button[onclick="mostrarEspejo()"]');
    try {
        if (!modoEspejo) {
            const response = await fetch('/espejo');
            const data = await response.json();

            if (!data.arbol) {
                mostrarMensaje(data.mensaje, true);
                
                return;
            }

            mostrarMensaje(data.mensaje);
            arbolData = data.arbol;
            dibujarArbol();

            // Activar estilo visual espejo
            document.body.classList.add('espejo-activo');
            boton.classList.add('modo-espejo-activo');
            boton.textContent = "Volver al Árbol Original";
            modoEspejo = true;
        } else {
            // Restaurar el árbol original
            await actualizarVisualizacion();
            mostrarMensaje("Árbol original restaurado.");
            document.body.classList.remove('espejo-activo');
            boton.classList.remove('modo-espejo-activo');
            boton.textContent = "Mostrar Espejo";
            modoEspejo = false;
        }
    } catch (error) {
        mostrarMensaje('Error al generar espejo: ' + error.message, true);
    }
}

function cambiarTipoArbol() {
    tipoArbolActual = document.getElementById('tipoArbol').value;
    const configMvias = document.getElementById('configMvias');
    
    if (tipoArbolActual === 'mvias') {
        configMvias.style.display = 'flex';
    } else {
        configMvias.style.display = 'none';
    }
    
    actualizarVisualizacion();
    obtenerInfoArbol();
}

async function configurarMvias() {
    const gradoM = parseInt(document.getElementById('gradoM').value);
    
    if (gradoM < 3) {
        mostrarMensaje('El grado M debe ser al menos 3', true);
        return;
    }
    
    try {
        const response = await fetch('/configurar_mvias', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ m: gradoM })
        });
        
        const data = await response.json();
        mostrarMensaje(data.mensaje);
        await actualizarVisualizacion();
        await obtenerInfoArbol();
    } catch (error) {
        mostrarMensaje('Error al configurar M-Vías: ' + error.message, true);
    }
}

async function insertarValor() {
    const valorInput = document.getElementById('valorInput');
    const valor = parseInt(valorInput.value);
    
    if (isNaN(valor)) {
        mostrarMensaje('Por favor ingrese un valor numérico válido', true);
        return;
    }
    
    try {
        const response = await fetch('/insertar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ valor, tipo_arbol: tipoArbolActual })
        });
        
        const data = await response.json();
        mostrarMensaje(data.mensaje);
        valorInput.value = '';
        await actualizarVisualizacion();
        await obtenerInfoArbol();
    } catch (error) {
        mostrarMensaje('Error al insertar valor: ' + error.message, true);
    }
}

async function eliminarValor() {
    const valorInput = document.getElementById('valorInput');
    const valor = parseInt(valorInput.value);
    
    if (isNaN(valor)) {
        mostrarMensaje('Por favor ingrese un valor numérico válido', true);
        return;
    }
    
    try {
        const response = await fetch('/eliminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ valor, tipo_arbol: tipoArbolActual })
        });
        
        const data = await response.json();
        mostrarMensaje(data.mensaje);
        valorInput.value = '';
        await actualizarVisualizacion();
        await obtenerInfoArbol();
    } catch (error) {
        mostrarMensaje('Error al eliminar valor: ' + error.message, true);
    }
}


async function realizarRecorrido(tipo) {
    try {
        const response = await fetch(`/recorrido/${tipo}?tipo_arbol=${tipoArbolActual}`);
        const data = await response.json();
        mostrarRecorrido(data.recorrido, tipo);
    } catch (error) {
        mostrarMensaje('Error al realizar recorrido: ' + error.message, true);
    }
}

async function mostrarInfo() {
    await obtenerInfoArbol();
}

async function obtenerInfoArbol() {
    try {
        const response = await fetch(`/info_arbol?tipo_arbol=${tipoArbolActual}`);
        const data = await response.json();
        mostrarInfoArbol(data);
    } catch (error) {
        console.error('Error al obtener información del árbol:', error);
    }
}

async function limpiarArbol() {
    try {
        const response = await fetch('/limpiar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tipo_arbol: tipoArbolActual })
        });
        
        const data = await response.json();
        mostrarMensaje(data.mensaje);
        await actualizarVisualizacion();
        await obtenerInfoArbol();
    } catch (error) {
        mostrarMensaje('Error al limpiar árbol: ' + error.message, true);
    }
}

async function actualizarVisualizacion() {
    try {
        const response = await fetch(`/estructura?tipo_arbol=${tipoArbolActual}`);
        const data = await response.json();
        arbolData = data.arbol;
        dibujarArbol();
    } catch (error) {
        console.error('Error al obtener estructura del árbol:', error);
        // Mostrar mensaje de error en el canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.font = '20px Arial';
        ctx.fillStyle = '#999';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Error al cargar el árbol', canvas.width / 2, canvas.height / 2);
    }
}

function dibujarArbol() {
    // Limpiar canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (!arbolData) {
        // Mostrar mensaje cuando el árbol está vacío
        ctx.font = '20px Arial';
        ctx.fillStyle = '#999';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Árbol vacío', canvas.width / 2, canvas.height / 2);
        return;
    }
    
    // Determinar el tipo de árbol y dibujar apropiadamente
    if (arbolData.tipo === 'mvias') {
        dibujarArbolMVias(arbolData);
    } else {
        dibujarArbolBinario(arbolData);
    }
}

function dibujarArbolMVias(nodoRaiz) {
    const config = {
        radio: 25,
        verticalEspacio: 100,
        horizontalEspacio: 80,
        anchoNodo: 150,
        altoNodo: 60
    };
    
    // Calcular posiciones de todos los nodos
    const posiciones = new Map();
    calcularPosicionesMVias(nodoRaiz, 0, canvas.width / 2, posiciones, config);
    
    // Dibujar conexiones primero
    dibujarConexionesMVias(nodoRaiz, posiciones, config);
    
    // Dibujar nodos después
    for (const [nodoId, posicion] of posiciones.entries()) {
        dibujarNodoMVias(posicion.x, posicion.y, posicion.valores, config);
    }
}

function calcularPosicionesMVias(nodo, nivel, x, posiciones, config) {
    if (!nodo) return;
    
    const y = nivel * config.verticalEspacio + 80;
    const nodoId = nodo.valores ? nodo.valores.join('-') : 'raiz';
    
    posiciones.set(nodoId, {
        x: x,
        y: y,
        valores: nodo.valores || [],
        nivel: nivel
    });
    
    // Si no tiene hijos, terminar
    if (!nodo.hijos || nodo.hijos.every(h => h === null)) {
        return;
    }
    
    // Filtrar hijos no nulos
    const hijosNoNulos = nodo.hijos.filter(h => h !== null);
    const cantidadHijos = hijosNoNulos.length;
    
    if (cantidadHijos === 0) return;
    
    // Calcular el ancho total necesario para los hijos
    const anchoTotal = cantidadHijos * config.horizontalEspacio * 2;
    let xInicio = x - anchoTotal / 2 + config.horizontalEspacio;
    
    // Calcular posiciones para cada hijo
    for (let i = 0; i < nodo.hijos.length; i++) {
        if (nodo.hijos[i] !== null) {
            calcularPosicionesMVias(nodo.hijos[i], nivel + 1, xInicio, posiciones, config);
            xInicio += config.horizontalEspacio * 2;
        }
    }
}

function dibujarConexionesMVias(nodo, posiciones, config) {
    if (!nodo || !nodo.hijos) return;
    
    const nodoId = nodo.valores ? nodo.valores.join('-') : 'raiz';
    const posPadre = posiciones.get(nodoId);
    
    if (!posPadre) return;
    
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    
    for (let i = 0; i < nodo.hijos.length; i++) {
        if (nodo.hijos[i] !== null) {
            const hijoId = nodo.hijos[i].valores.join('-');
            const posHijo = posiciones.get(hijoId);
            
            if (posHijo) {
                // Dibujar línea desde el padre al hijo
                ctx.beginPath();
                ctx.moveTo(posPadre.x, posPadre.y + config.altoNodo / 2);
                ctx.lineTo(posHijo.x, posHijo.y - config.altoNodo / 2);
                ctx.stroke();
                
                // Dibujar conexiones recursivamente para los hijos
                dibujarConexionesMVias(nodo.hijos[i], posiciones, config);
            }
        }
    }
}

function dibujarNodoMVias(x, y, valores, config) {
    const cantidadValores = valores.length;
    const anchoTotal = Math.max(config.anchoNodo, cantidadValores * 30 + 40);
    
    // Dibujar rectángulo del nodo
    ctx.fillStyle = '#2196F3';
    ctx.strokeStyle = '#1976D2';
    ctx.lineWidth = 3;
    
    // Rectángulo con bordes redondeados
    ctx.beginPath();
    ctx.roundRect(x - anchoTotal / 2, y - config.altoNodo / 2, anchoTotal, config.altoNodo, 10);
    ctx.fill();
    ctx.stroke();
    
    // Dibujar valores
    ctx.fillStyle = 'white';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    valores.forEach((valor, index) => {
        const spacing = anchoTotal / (cantidadValores + 1);
        const xPos = x - anchoTotal / 2 + (index + 1) * spacing;
        ctx.fillText(valor.toString(), xPos, y);
    });
}

function dibujarArbolBinario(nodoRaiz) {
    const config = {
        radio: 25,
        verticalEspacio: 100,
        horizontalEspacio: 60
    };
    
    // Calcular posiciones
    const posiciones = new Map();
    calcularPosicionesBinario(nodoRaiz, 0, canvas.width / 2, posiciones, config);
    
    // Dibujar conexiones
    dibujarConexionesBinario(nodoRaiz, posiciones, config);
    
    // Dibujar nodos
    for (const [valor, posicion] of posiciones.entries()) {
        dibujarNodoBinario(posicion.x, posicion.y, valor, config.radio);
    }
}

function calcularPosicionesBinario(nodo, nivel, x, posiciones, config) {
    if (!nodo) return;
    
    const y = nivel * config.verticalEspacio + 80;
    posiciones.set(nodo.valor, { x: x, y: y });
    
    // Calcular espacio para subárboles
    const alturaSubarbol = calcularAlturaBinario(nodo);
    const espacioHorizontal = Math.pow(2, alturaSubarbol - 1) * config.horizontalEspacio;
    
    // Hijo izquierdo
    const hijoIzq = nodo.izquierdo || nodo.hijo_izquierdo;
    if (hijoIzq) {
        calcularPosicionesBinario(hijoIzq, nivel + 1, x - espacioHorizontal, posiciones, config);
    }
    
    // Hijo derecho
    const hijoDer = nodo.derecho || nodo.hijo_derecho;
    if (hijoDer) {
        calcularPosicionesBinario(hijoDer, nivel + 1, x + espacioHorizontal, posiciones, config);
    }
}

function calcularAlturaBinario(nodo) {
    if (!nodo) return 0;
    
    const alturaIzq = calcularAlturaBinario(nodo.izquierdo || nodo.hijo_izquierdo);
    const alturaDer = calcularAlturaBinario(nodo.derecho || nodo.hijo_derecho);
    
    return 1 + Math.max(alturaIzq, alturaDer);
}

function dibujarConexionesBinario(nodo, posiciones, config) {
    if (!nodo) return;
    
    const posNodo = posiciones.get(nodo.valor);
    if (!posNodo) return;
    
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    
    // Conexión con hijo izquierdo
    const hijoIzq = nodo.izquierdo || nodo.hijo_izquierdo;
    if (hijoIzq) {
        const posHijoIzq = posiciones.get(hijoIzq.valor);
        if (posHijoIzq) {
            ctx.beginPath();
            ctx.moveTo(posNodo.x, posNodo.y + config.radio);
            ctx.lineTo(posHijoIzq.x, posHijoIzq.y - config.radio);
            ctx.stroke();
            dibujarConexionesBinario(hijoIzq, posiciones, config);
        }
    }
    
    // Conexión con hijo derecho
    const hijoDer = nodo.derecho || nodo.hijo_derecho;
    if (hijoDer) {
        const posHijoDer = posiciones.get(hijoDer.valor);
        if (posHijoDer) {
            ctx.beginPath();
            ctx.moveTo(posNodo.x, posNodo.y + config.radio);
            ctx.lineTo(posHijoDer.x, posHijoDer.y - config.radio);
            ctx.stroke();
            dibujarConexionesBinario(hijoDer, posiciones, config);
        }
    }
}

function dibujarNodoBinario(x, y, valor, radio) {
    // Círculo del nodo
    ctx.fillStyle = '#4CAF50';
    ctx.strokeStyle = '#388E3C';
    ctx.lineWidth = 3;
    
    ctx.beginPath();
    ctx.arc(x, y, radio, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    
    // Texto del valor
    ctx.fillStyle = 'white';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(valor.toString(), x, y);
}

// Polyfill para roundRect (para navegadores más antiguos)
if (!CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function(x, y, width, height, radius) {
        if (width < 2 * radius) radius = width / 2;
        if (height < 2 * radius) radius = height / 2;
        
        this.beginPath();
        this.moveTo(x + radius, y);
        this.arcTo(x + width, y, x + width, y + height, radius);
        this.arcTo(x + width, y + height, x, y + height, radius);
        this.arcTo(x, y + height, x, y, radius);
        this.arcTo(x, y, x + width, y, radius);
        this.closePath();
        return this;
    };
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('treeCanvas');
    ctx = canvas.getContext('2d');
    
    cambiarTipoArbol();
    actualizarVisualizacion();
    obtenerInfoArbol();
    
    // Redibujar cuando cambia el tamaño de la ventana
    window.addEventListener('resize', function() {
        actualizarVisualizacion();
    });
 
});