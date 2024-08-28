#### Introducción: 

Nuestra aplicación es un sistema de recomendador de libros a usuarios, basado en información obtenida de estos usuarios como:
 
    - 
    -
    -

Usamos sobre los libros información como:

    - Año
    - Géneros
    - Títulos
    - Lenguaje


Para recomendar una lista de libros a un usuario, no necesariamente registrado en nuestra aplicación, se usa un enfoque híbrido conocido por *Item-based Clustering Hybrid Method*, este combina *Content-Based and Collaborative Filters*, el resultado final de este algoritmo es una matriz de similitud $M[i][j]$ que representa la similitud que es determinada entre los libros $i, j$. Con esta matriz calculada es posible predecir un rating entre el usuario $u$ y el libro $b$, la salida de la aplicación serían los mejores $N$ ratings.   

El sistema recomendador, después de haber calculado la matriz de similitud $M$ puede hacer recomendaciones a usuarios, por lo que se distinguen dos estados en los que se puede encontrar este:

    - a partir de información nueva sobre los usuarios o nuevos items calcular nuevamente esta matriz $M$.
    - realizar recomendaciones a los usuarios ( registrados o no ).

Para que nuestra aplicación se mantenga interactiva, cada cierto tiempo recalculamos esta matriz en segundo plano, y cuando se haya terminado este proceso, concurrentemente actualizamos la información, para que a partir de este momento se pueda usar la nueva información en la recomendación.

#### Como Predecir Rating : 

Con la matriz de similitud $M$ se usa la siguiente fórmula para predecir el rating $r$ de un usuario $u$ a el libro $b$ :

$$r = P_b + \frac{\sum_{i = 1}^n M[i][k]*(R[u][b] - P_b)}{\sum_{i = 1}^n | M[i][k] | }$$

Donde $n$ representa la cantidad de libros con los que el usuario $u$ ha interactuado y están en nuestra base de datos, $R[u][b]$ representa el rating de el usuario $u$ a el libro $b$ y $P_k$ representa el promedio de los ratings que ha recibido el libro $b$.

Los dos sumandos de la fórmula anterior son interpretados como:

    - Notar que si el usuario no ha interactuado con ningún libro el sistema predeciría solamente usando los promedios de los ratings de los libros existentes, lo que permite hacer recomendaciones a los usuarios sin tener conocimiento de ellos.
    - Con respecto a la segunda fórmula, notar que el segundo factor de cada sumando representa una proporción con respecto a el denominador, en otras palabras representa un promedio ponderado de los valores $(R[u][b] - P_b)$, !!!!!!!!!!

La complejidad de realizar este método sería $O(n)$, pero este es calculado por cada libro que hay en nuestra base de datos, asumiendo que hayan $m$ libros esta sería $O(n * m)$, por esta razón tenemos alrededor de $2000$ libros en nuestra base de datos, cifra que permite realizar la recomendación lo suficientemente rápido.

Dada la explicación anterior quedaría por analizar como es calculada la matriz $M$ de similitud:

Esta matriz es obtenida a través de la combinación linear de otras dos matrices, análogamente de similitud ($A[i][j]$ representa la similitud entre los libros $i, j$), que son halladas a partir de la información que posee el sistema:

#### Se describe como son obtenidas las dos matrices y posteriormente como son combinadas para obtener la matriz $M$:

##### Matriz 1:

Sobre un usuario, en nuestra base de datos , contamos con alguna interacción con ciertos libros, usamos esta información para calcular un *rating* para cada libro con el que interactúa el usuario, la forma en que es calculado este rating puede ser realizado de varias formas siempre que se obtenga un número entre [1, 5], describimos en otra sección el método usado. 

El resultado de el proceso anterior es conocido como *item-rating matrix*, nuestro objetivo es obtener una matriz de similitud a partir de esta *item-rating matrix*. Para hacerlo se usa el *Pearson Correlation Algorithm* ( en otra sección explicamos en que consiste ), en particular la siguiente fórmula:

$$A[k][l] = \frac{ \sum_{u = 1}^m (R_{u,k} - R_k)*(R_{u,l} - R_l) }{ \sqrt{\sum_{u = 1}^m (R_{u,k} - R_k)^2} * \sqrt{\sum_{u = 1}^m (R_{u,l} - R_l)^2} }$$

Donde $k, l$ son dos libros en nuestra base de datos, $m$ es la cantidad de usuarios que interactuaron con ambos libros $k, l$. $R_k,R_l$ son los promedios de los rating recibidos por los libros $k, l$ y $R_{u,k}, R_{u,l}$ son los ratings de los libros $k, l$ dados por el usuario $u$. 

##### Matriz 2:

La matriz anterior usa información obtenida de la interacción usuario-libro, para esta matriz solamente es requerida información de los libros, es posible establecer una medida de similitud entre los libros, esto no es más que una función que toma como argumentos dos libros y devuelve un valor entre $0, 1$ como una medida de que tan similares son. 

Esta ha de cumplir ser reflexiva y simétrica. Hay varias formas de establecer esta similitud, en otra sección explicamos cual medida usamos. Asumiendo una función de similitud $f$, es posible ejecutar un algoritmo de $K-means$ para agrupar a los libros:

Este asigna inicialmente al azar $k$ grupos, representados cada uno por un libro.

En base a la similitud se calcula a cual grupo debe pertenecer cada libro, una vez realizado esto, es posible cambiar a el representante de cada grupo por otro libro en el grupo, que se encuentre más al *centro* con respecto a los libros en su grupo, teniendo en cuenta esto, el algoritmo es de punto fijo hasta que se logren centros de cada grupo *estables*. ( no cambiarían en una próxima iteración). 

Para cambiar a el representante de el grupo,  hay varias formas, en nuestro caso , por cada elemento de el grupo  hallamos su similitud con los restantes y multiplicamos esos valores, se mantiene como un número entre $[0, 1]$, escogemos como nuevo representante el que maximice ese valor.

Una vez que tenemos el *grouping* realizado se crea una matriz $T$ donde las filas son libros, y las columnas son los representantes de los grupos, en las casillas estaría la similitud entre el libro *fila* y el representante *columna* , esto puede ser visto como la *membership* de cada elemento a un conjunto, en términos de *fuzzy logic*.

Finalmente a partir de esta matriz $T$ se calcula la matriz de similitud, notar que la matriz de similitud es indexada con dos libros cualesquiera, mientras que esta $T$ es entre un libro y un libro representante de algún grupo.

Para hallar la matriz de similitud es usada una variación de la similitud de coseno, la idea es que las filas de la matriz ( libros ) representan un vector, y sus valores son los que están a lo largo de la fila, o sea, cada componente es uno de los grupos. La razón de la variación de la similitud de coseno es una cuestión de escalas: si un usuario siempre marca con $5$ su mejor película, $1$ una mala película a su juicio, mientras que otro, por costumbre, nunca marca con $5$ ni siquiera a su pélicula preferida, sino con 4, y análogamente con $2$ a una película mala, ocurre una diferencia de escalas que no es manejada correctamente por la similitud de coseno estándar. La fórmula sería : 

$$A[k][l] = \frac{ \sum_{u = 1}^m (R_{k, u} - R_u)*(R_{l, u} - R_u) }{ \sqrt{\sum_{u = 1}^m (R_{k, u} - R_u)^2} * \sqrt{\sum_{u = 1}^m (R_{l, u} - R_u)^2} }$$

Donde $k, l$ son dos libros, $m$ es la cantidad de clusters, $R_{k,u}, R_{l,u}$ representa la similitud entre el libro $k$ y el representante del cluster $u$, análogamente $R_{l, u}$, $R_u$ es el promedio de las similitud respecto a el libro representante del cluster $u$, o ( sea el promedio de los valores en esa columna).

##### Combinación:

Una vez calculadas las dos matrices $A_1, A_2$ entonces:

$$M = c * A_1 + (1-c) * A_2$$

La cantidad de clusters, y el coeficiente en la combinación linear son parámetros que deben estimarse de forma que minimizen alguna métrica como *Mean Absolute Error*.

#### Complejidad :

La complejidad de todos estos pasos es al menos cuadrática : 

    - el algoritmo de $K-Means$ divide a los libros en grupos, pero dentro de un  grupo es hallada la similitud entre cada par de libros, esto es O(it * l^2) donde $it$ es la cantidad de iterciones que hace el algoritmo, y $l$ es la cantidad de libros.

    - el algoritmo para calcular la *item - rating matrix* usa las interacciones entre libros y usuarios en el peor caso tiene que analizar $O(l * u)$ donde $l$ es la cantidad de libros, y $u$ es la cantidad de usuarios.

    - construir la segunda matrix de similitud itera por cada par de libros, y después por los clusters, por tanto sería $O( k * l^2)$, donde $k$ es la cantidad de clusters.

Por las razones anteriores este cálculo es cacheado, y precomputado en segundo plano en caso de que se necesite actualizar la información del sistema recomendador.

#### Como se calcula el rating del usuario:

#### Como calculamos la similitud entre dos libros:
    Se calculan dos proporciones y se multiplican:
        - la razón entre la intersección e unión de sus géneros.
        - la razón ponderada ( coincidencia en Autor debe constribuir mucho más que coincidencia en Año) de en cuantos atributos coinciden, Año, Lenguaje, etc

#### Test : 

Realizamos dos tests:

##### Velocidad : 

Ejecutamos el algoritmo de recomendar con algunos usuario al azar de nuestra base de datos, mostramos un resumen estadístico de los resultados.

##### Precisión :

Para evaluar la precisión de el sistema, generamos $100$ usuarios nuevos, que interactuan con los libros actuales en nuestro sistema, comparamos sus *rating* predecidos con los actuales, usando *Mean Absolute Error*, mostramos un resumen estadístico de los resultados.

#### Referencias:

    - An Approach for Combining Content-based and Collaborative Filters: Qing Li, Byeong Man Kim
    Resnick, P., Iacovou, N., Suchak, M., et al. (1994) GroupLens: An Open Architecture for Collaborative Filtering of Netnews.