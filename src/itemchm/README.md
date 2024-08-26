Steps:
    1 - aplicar un algoritmo de clustering para agrupar a los items, asumiendo una cantidad de clusters dada, el input sería una lista de items, con sus posibles atributos / clasificaciones, la salida es una tabla donde a cada item se le asigna una probabilidad / degree of membership de estar en un grupo dado.
    2 - Se calcula una similitud entre cada par de items, ie una matrix cuadrada, para hacerlo se hallan dos matrices, que representan similitudes y se combinan linealmente:
        - con la tabla de item / rating ( el rating que le da cada usuario a un item ) se calcula la similitud entre un par de items k, l usando Pearson correlation based similarity.
        - con la tabla de group / rating ( la que se obtuvo con los clusters ) se calcula la similitud entre un par de items k, l usando Adjusted Cosine Similarity.
        - se escoge un c in [0, 1] y se usa $f * c + (1-c)*g$. Según el paper 0.4 es adecuado, pero eso debe depender de los datos.
    3 - Con esta table ya precomputada para un usuario $u$ y un item $k$ se calcula una predicción, la salida del sistema - recomendador es los $N$ elementos de mayor valor según la predicción anterior.

La complejidad es cuadrática, por lo que la cantidad de usuarios, películas no debe ser mayor que 10^4. Entre 10^4 y 10^5 es crítico. 

Referencias:
    An Approach for Combining Content-based and Collaborative Filters: Qing Li, Byeong Man Kim