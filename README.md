# PROYECTO-EDII-RUTAS


RESUMEN

Esta investigación desarrolla una simulación computacional de rutas y conectividad en grafos dirigidos para representar una red de transporte hipotética. El problema consiste en identificar trayectos factibles y de costo mínimo, así como determinar cómo se modifica el acceso entre puntos cuando se interrumpe una conexión. Se construyó un grafo de ocho vértices y trece aristas orientadas, con pesos no negativos expresados como minutos hipotéticos. Se implementaron en Python, utilizando únicamente su biblioteca estándar, la búsqueda en anchura (BFS), la búsqueda en profundidad (DFS), el algoritmo de Dijkstra y el procedimiento de Kosaraju para componentes fuertemente conexas. Se realizaron comparaciones matemáticas y cuatro escenarios reproducibles: red original y eliminación individual de tres aristas. En la red inicial, BFS obtuvo un recorrido de dos aristas y costo 17, mientras que Dijkstra identificó una ruta de costo 10, lo que evidencia la diferencia entre minimizar saltos y minimizar pesos. La eliminación de una conexión elevó el costo mínimo a 13, mientras que la supresión del único enlace entrante hacia el destino imposibilitó el trayecto. Los resultados respaldan el empleo de grafos dirigidos para estudiar rutas, alcanzabilidad y vulnerabilidad estructural, sin pretender describir el tráfico real de Lima.
Palabras clave: grafos dirigidos; rutas mínimas; conectividad; Dijkstra; simulación.

I. INTRODUCCIÓN

Los sistemas de transporte, comunicación y distribución poseen conexiones que no siempre pueden recorrerse en ambos sentidos. Las calles de sentido único, los enlaces de una red informática y las etapas de una cadena logística son ejemplos de relaciones orientadas. Su representación mediante grafos dirigidos permite formalizar preguntas prácticas: ¿se puede llegar desde un punto de origen hasta un destino?, ¿qué trayecto requiere menos conexiones?, ¿cuál consume menos tiempo?, ¿qué cambia si se bloquea una vía? [1], [2].
Una confusión habitual consiste en equiparar el camino con menos aristas al camino de menor costo. Cuando cada desplazamiento posee un peso diferente —tiempo, distancia o gasto—, ambas respuestas pueden ser distintas. Asimismo, verificar que un destino sea alcanzable desde el origen no significa que exista conectividad en ambos sentidos. La orientación de las aristas obliga a analizar el orden de los recorridos y la conectividad fuerte [1], [3].
Se propone una red de transporte abstracta, diseñada exclusivamente para la experimentación, con ocho ubicaciones rotuladas de A a H. Los pesos representan minutos supuestos y no datos levantados en campo. El alcance comprende la formulación del grafo, la programación de algoritmos básicos, el contraste entre sus respuestas y las pruebas de fallos de aristas; se excluyen congestión temporal, semáforos, capacidad vial y rutas georreferenciadas.
Pregunta de investigación: ¿cómo permiten los algoritmos de recorridos y rutas mínimas analizar la alcanzabilidad y la variación del costo de viaje ante interrupciones en una red modelada como grafo dirigido?
El estudio es relevante para Estructuras Discretas II porque articula relaciones binarias, caminos, optimización, complejidad algorítmica y verificación computacional dentro de un modelo que cualquier equipo puede reproducir.


II. ANTECEDENTES HISTÓRICOS Y APORTES DE AUTORES

La teoría de grafos consolidó un lenguaje para describir relaciones entre objetos y estudiar propiedades que no dependen del dibujo de la red. Sus aplicaciones modernas incluyen circuitos, caminos, redes de datos y problemas de planificación. El enfoque algorítmico actual se apoya en representaciones eficientes, como las listas de adyacencia [1].
En 1959, Edsger W. Dijkstra publicó un método para encontrar caminos mínimos entre vértices en grafos con pesos adecuados. Su aporte sustenta la selección iterativa del vértice con menor distancia tentativa y la relajación de aristas, principio aplicado en este informe para minimizar tiempos hipotéticos [2].
En 1972, Robert E. Tarjan demostró el valor del recorrido en profundidad para estudiar propiedades estructurales, entre ellas las componentes fuertemente conexas de grafos dirigidos, mediante procedimientos de complejidad lineal. Este resultado fundamenta el análisis de conectividad de la presente simulación [3].
En la informática contemporánea, textos de algoritmos y bibliotecas de análisis de grafos sistematizan BFS, DFS y Dijkstra para consultas de rutas. La documentación técnica de NetworkX distingue explícitamente los trayectos mínimos en número de saltos de los caminos ponderados, diferencia central en los experimentos desarrollados [1], [4].

III. MARCO TEÓRICO

3.1. Grafo dirigido y ponderado
Un grafo dirigido se define como G = (V, E), donde V es un conjunto finito de vértices y E ⊆ V × V es un conjunto de pares ordenados. Si (u, v) ∈ E, existe una arista desde u hacia v; esto no implica que (v, u) ∈ E. Cuando cada arista tiene un costo, se define w: E → ℝ≥0, donde w(u, v) es su peso no negativo [1].
Una lista de adyacencia asocia a cada vértice sus vecinos de salida y sus pesos. Para grafos dispersos, esta representación requiere espacio proporcional a O(|V| + |E|) y permite visitar las aristas existentes sin recorrer toda una matriz de V × V [1].
3.2. Caminos, costos y alcanzabilidad
Un camino dirigido de s a t es una secuencia s = v₀, v₁, …, vₖ = t tal que (vᵢ, vᵢ₊₁) pertenece a E para cada paso. El número k de aristas es su longitud en saltos, mientras que su costo es C(P) = Σ w(vᵢ, vᵢ₊₁). Un vértice t es alcanzable desde s si existe al menos un camino dirigido s → t. La alcanzabilidad no tiene por qué ser simétrica.
Una red es fuertemente conexa cuando para cada par de vértices u y v existen rutas dirigidas u → v y v → u. Una componente fuertemente conexa (CFC) es un subconjunto maximal de vértices mutuamente alcanzables. Un grafo con una única CFC es fuertemente conexo [3], [5].
3.3. Búsqueda en anchura (BFS) y en profundidad (DFS)
BFS expande primero los vértices más cercanos al origen en número de aristas mediante una cola. Si todas las aristas se consideran de costo unitario, el primer descubrimiento de un vértice determina una ruta con el mínimo número de saltos. Su complejidad en listas de adyacencia es O(|V| + |E|). BFS no minimiza automáticamente la suma de pesos heterogéneos [1], [4].
DFS explora una rama tan profundamente como puede antes de retroceder. Puede implementarse con una pila o recursión y recorre el grafo en O(|V| + |E|). Es útil para calcular el conjunto alcanzable, detectar ciclos y apoyar algoritmos de conectividad; su orden de visita no garantiza una ruta mínima [1], [3].
3.4. Dijkstra y justificación de corrección
Dijkstra mantiene una distancia tentativa d[v] para cada vértice. Inicializa d[s] = 0 y d[v] = ∞ para v ≠ s. En cada iteración extrae el vértice u con menor distancia conocida y relaja sus aristas salientes mediante d[v] ← min(d[v], d[u] + w(u, v)). Usando una cola de prioridad binaria, su complejidad usual es O((|V| + |E|) log |V|) [1], [2], [4].
Idea de demostración: cuando se extrae el vértice u con mínima distancia tentativa, esta ya es óptima. Si existiera un camino más barato hasta u que pasara por algún vértice todavía no procesado, el primer borde que cruzara desde los procesados tendría costo no negativo; su relajación habría generado una distancia tentativa no mayor que la del supuesto camino, contradiciendo la elección de u. La hipótesis de pesos no negativos es indispensable [1], [2].
3.5. Componentes fuertemente conexas
El algoritmo de Kosaraju identifica CFC con dos pasadas de DFS: primero obtiene el orden de finalización en el grafo original; después recorre el grafo traspuesto en el orden inverso de finalización. Cada exploración de la segunda pasada determina una componente. Su complejidad es O(|V| + |E|). Tarjan ofrece otra solución lineal basada en DFS [3], [5].

IV. OBJETIVOS

Objetivo general
Diseñar e implementar una simulación reproducible de rutas y conectividad en un grafo dirigido y ponderado, comparando algoritmos de recorrido y evaluando el efecto de interrupciones de enlaces.
Objetivos específicos
•  Modelar una red dirigida mediante conjuntos de vértices y aristas ponderadas, y definir sus condiciones de funcionamiento.
•  Implementar BFS, DFS, Dijkstra y una técnica de identificación de componentes fuertemente conexas, especificando entradas, salidas y complejidad.
•  Validar rutas y conectividad en escenarios base y con aristas eliminadas, interpretando los cambios de costo y alcanzabilidad.


V. METODOLOGÍA Y DISEÑO

5.1. Enfoque y supuestos
El estudio adopta un enfoque aplicado, cuantitativo y experimental por simulación determinista. Se define una única red sintética; no se infieren parámetros de tránsito a partir de observaciones reales. Los nodos A–H representan ubicaciones genéricas y cada peso es un tiempo de recorrido inventado, constante y expresado en minutos. Se supone que los costos son no negativos, que la dirección debe respetarse y que retirar una arista equivale a prohibir su tránsito.
5.2. Representación matemática de la red
Se utiliza V = {A, B, C, D, E, F, G, H} y el conjunto E formado por las 13 conexiones listadas en la Tabla 1. Los arcos están orientados y los pares (u, v) son diferentes de (v, u). La red es débilmente conexa si se ignoran las orientaciones, pero no es fuertemente conexa.

Tabla 1. Conexiones dirigidas y tiempos hipotéticos.

| Arista | Minutos | Arista | Minutos |
| :--- | :---: | :--- | :---: |
| A → B | 2 | D → E | 1 |
| A → C | 5 | D → F | 6 |
| A → G | 15 | E → F | 2 |
| B → C | 1 | F → G | 1 |
| B → D | 2 | G → E | 4 |
| C → E | 3 | G → H | 2 |
| C → G | 12 | — | — |

!Figura 1. Red dirigida hipotética. Aristas naranjas: ruta de tiempo mínimo A → H. Elaboración propia.](Recursos/Figura1.png)

5.3. Variables e indicadores


Variables de entrada: vértices, aristas, pesos, origen A, destino H y arista que se elimina. Indicadores de salida: camino BFS, número de saltos, camino Dijkstra, tiempo mínimo, cantidad de vértices alcanzables desde A y número de CFC. Se emplea un orden alfabético fijo de vecinos para que las trazas sean repetibles.


5.4. Procedimiento y herramientas


La simulación se programó en Python 3 utilizando collections.deque, heapq y estructuras estándar dict/set. El procesamiento tiene cuatro fases: construcción del grafo, consulta de caminos, cálculo de componentes y ejecución de escenarios de interrupción. No requiere bibliotecas externas. Las figuras se elaboraron por separado para ilustrar el modelo y los resultados.


5.5. Algoritmos (pseudocódigo resumido)


BFS(G, s, t): crear cola [s] y predecesor[s] = vacío; mientras haya elementos, extraer u; por cada vecino no visitado, registrar su predecesor y encolarlo; reconstruir el camino hacia t. DFS(G, s): explorar vecinos por pila hasta agotar los alcanzables. Dijkstra(G, s, t): mantener distancias y cola mínima; extraer u con menor distancia; si es vigente, relajar cada arco saliente; reconstruir el trayecto óptimo. CFC(G): calcular orden de finalización por DFS; invertir todas las aristas; explorar el traspuesto según el orden inverso; agrupar nodos visitados en cada exploración.

