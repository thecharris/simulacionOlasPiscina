import numpy as np

"""
El plan es simular como afectan las olas a un nadador. La intensión es unicamente comparar si es mejor 
nadar cerca o lejos de las paredes. Estableciendo un sistema de coordenadas en 2d en donde el eje y apunta
del carril con el número más alto al 1 y el eje x apunta desde el bloque de salida hasta el otro lado de 
la piscina. Para construir el modelo, voy a suponer que el nadador es
propulsado constantemente con una fuerza Fs que puede dirigirse en cualquier dirección. Esta fuerza,
claramente, tiene que oponerse a la resistencia que representa moverse a traves del agua. 
Para que todo sea sencillo voy a suponer que contra el nadador solo chochan olas que son perpendiculares a
la dirección del movimiento. Todos los carriles van a crear olas con una fuerza Fo. La olas en se generan en 
dirección y-positivo y y-negativo. Voy a suponer que las olas cada vez que pasan a otro carril, solo conservan 
un porcentaje q de la fuerza que llevaban. Las olas, además interaccionan entre si. Voy a ignorar cuestiones 
como la frecuencia o la amplitud y simplemente voy a trabajar con la fuerza de la ola. Además voy a suponer 
que las paredes reflejan un porcentaje p de la fuerza total que reciben. La clave para que esto sea lo más
preciso posible teniendo en cuenta nuestro objetivo, que es ver si es mejor estar cerca o lejos de las paredes,
es clave que las olas se reflejen. Siguiendo con la simplificación voya a suponer que el nadador absorbe
completamente las olas. Por lo tanto las olas se mueven a lo largo de la piscina y rebotan con las paredes
hasta que llegan al nadador. El nadador al moverse tambien genera olas que se mueven lejos de él y rebotan 
con las paredes. Entonces de la fuerza total que tiene el nadador (Fs) tiene que gastarse,
parcialmente para que mantenga su dirección en linea recta en el eje x.
"""

# nCarriles es el número de carriles de la piscina
# cNadador es el carril en el que se encuentra el nadador
# Fo es la fuerza con la que las olas te pueden empujar
# q es el porcentaje de la ola que logra superar los separadores
# p es el porcentaje de la ola que es reflejado por la pared
"""
Esta función toma todas las fuerzas que causan las olas y las junta. Teninendo en cuenta
que todo carril genera una ola con fuerza Fo hacia la derecha y hacia la izquierda
"""
def olas(nCarriles: int, cNadador: int, Fo: float, q: float, p: float):
    """
    cada vez que una ola pasa de un carril a otro, solo se conserva q*F de la fuerza que llevaba
    (siendo aquí F, la fuerza que tenía antes de cambiar de carril).Por lo tanto si una ola 
    tiene que atravesar n carriles, entonces llegará al nadador, Fo*q^n
    """
    """
    todalD es la suma de todas las fuerzas cuando alcanzan el nadador desde la derecha,
    (carriles cuyo número es mayor que cNadador) es decir Fo*q+Fo*q^2+...+Fo*q^(nCarriles-cNadador)
    las simplificaciones de la suma se pueden usar porque q forma una serie geométrica.
    """
    totalD  = Fo * ((q**(nCarriles-cNadador+1)-q)/(q-1))
    """
    todalD es la suma de todas las fuerzas cuando alcanzan el nadador desde la izquierda,
    (carriles cuyo número es menor que cNadador) es decir Fo*q+Fo*q^2+...+Fo*q^(cNadador-1)
    las simplificaciones de la suma se pueden usar porque q forma una serie geométrica.
    """
    totalI = -Fo * ((q**(cNadador)-q)/(q-1))

    """
    FoN es la otra suma de fuerzas. Estas olas son generadas por el nadador entonces tienen que ir 
    hasta la pared y volver hasta el nadador.
    """
    FoN = (q**(2*nCarriles-2*cNadador) - q**(2*cNadador-2))*Fo*p

    """
    En en la introducción se definió que en cada carril se generan olas en ambas direcciones. Ya tuve
    en cuenta las que se generaron en dirección al nadador. Faltan entonces las que van en el otro sentido
    que avanzan, chocan contra la pared y vuelven.
    """
    """
    en el caso de los carriles que estan a la izquierda (carriles cuyo número es menor que cNadador)
    del nadador sería Fo*p*q^(cNadador-1)+Fo*q*p*q^(cNadador-1)+Fo*q^2*p*q^(cNadador-1)+...+Fo*q^(cNadador-1)
    *p*q^(cNadador-1). Las simplificaciones de la suma se pueden usar porque q forma una serie geométrica.
     """
    FoCi = (totalI-Fo)*p*q**(cNadador-1)
    
    """
    en el caso de los carriles que estan a la derecha (carriles cuyo número es mayor que cNadador)
    del nadador sería Fo*p*q^(nCarriles-cNadador)+Fo*q*p*q^(nCarriles-cNadador)+Fo*q^2*p*
    q^(nCarriles-cNadador)+...+Fo*q^(nCarriles-cNadador)*p*q^(nCarriles-cNadador).
    Las simplificaciones de la suma se pueden usar porque q forma una serie geométrica
    """
    FoCd = (totalD+Fo)*p*q**(nCarriles-cNadador)

    # finalmente total como sunomre lo dice es la suma de todos las fuerzas combinadas.
    total = totalD + totalI + FoN + FoCi+FoCd
    return total
    
# Esta función calcula la fuerza de fricción causada por moverse dentro del agua
def Fr(v: float):
    # P es la densidad del agua en kg/m^3
    P = 1000
    """
    A es el area transversal de una persona si hicieras un corte a la altura de 
    los hombros, con un plano cuya normal es paralela a las piernas. A se calcula
    aproximando la forma a un elipse. A está en m^2
    """
    A = 0.085
    """
    C es el coeficiente de arrastre del nadador. Esto es aproximadamente 1.
    """
    return 0.5*P*A*v**2

"""
Voy a evitar usar ecuaciones diferenciales, pera mantener todo sencillo. Entoces voy a provechar el 
poder de computo y voy a usar intervalos de tiempo super chiquitos para ir actualizando la fuerza de
rozamiento y todas estas cuestiones. Así mismo como el objetivo es no moverse lateralmente, no hay
resistencia causada por el agua.
"""
#Main
for i in range(1,9):
    dt = 0.01
    # la suma de todo lo que generan las olas es
    totalOlas = olas(8,i,25,0.7,0.7)
    # Fs es la velocidad con la que el nadador es impulsado constantemente
    Fs = 180
    # Voy a iniciar con que el nadador inicia desde una posición estática, por lo tanto
    v = 0
    """
    por las propiedades geometricas tenemos que lo que le sobra a Fs de corregir el movimiento
    causado por las olas es sqrt Fs*êx = (|Fs|^2-totalOlas) 
    al unir todas las fuerzas, tanto las de las olas, como las del nadador y la del rosamiento, nos queda Fres
    """
    Fres = np.sqrt((Fs**2) - (totalOlas**2)) - Fr(v)

    s = 0
    t = 0
    # es la masa del nadador en kg
    m = 77
    while s <= 50:
        #aplicando caracteristicas del calculo infinitesimal
        v += dt * Fres/m
        Fres = np.sqrt((Fs**2) - (totalOlas**2)) - Fr(v)
        s += v*dt
        t+=dt

    print(f"Miguel llega con una velocidad de {v}m/s, tras {t}s, estando en el carril {i}")