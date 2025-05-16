# Documento Técnico: Modelado del Efecto de las Olas en un Nadador en Diferentes Carriles

## 1. Introducción

Este documento explica el marco teórico que se utilizó para simular el impacto de las olas en una piscina sobre el rendimiento de un nadador, dependiendo del carril en que nada.
Así mismo, consulta el [script principal](simulacion.py) para ver el código de la implementación del modelo

---

## 2. Modelo Teórico

### 2.1 Dinámica de Olas

Las olas se generan en todos los carriles y se propagan hacia ambos lados. La fuerza de las olas disminuye al atravesar los separadores y al reflejarse en las paredes.

#### Variables principales:

* $n$: Número total de carriles.
* $c$: Carril del nadador ($1 \leq c \leq n$).
* $F_o$: Fuerza inicial de una ola.
* $q$: Factor de atenuación al cruzar un carril ($0 < q < 1$).
* $p$: Porcentaje de fuerza reflejada por las paredes ($0 < p < 1$).

#### Cálculo de la fuerza neta de las olas que afectan al nadador:

1. **Olas directas:**

  * Desde carriles a la derecha:
    $F_{\text{derecha}} = F_o \cdot (q + q^2 + q^3 + \ldots + q^{n-c})$

  * Desde carriles a la izquierda:
    $F_{\text{izquierda}} = -F_o \cdot (q + q^2 + q^3 + \ldots + q^{c-1})$

2. **Olas reflejadas:**

  * Generadas por el propio nadador:
    $F_{\text{reflejo}} = F_o \cdot p \cdot (q^{2(n-c)} - q^{2(c-1)})$

  * Provenientes de otros carriles:

    * Por la izquierda:
      $F_{\text{reflejo-izq}} = (F_{\text{izquierda}} - F_o) \cdot p \cdot q^{c-1}$

    * Por la derecha:
      $F_{\text{reflejo-der}} = (F_{\text{derecha}} + F_o) \cdot p \cdot q^{n-c}$
      
**Fuerza total de olas**:

$$
F_{\text{total}} = F_{\text{derecha}} + F_{\text{izquierda}} + F_{\text{reflejo}} + F_{\text{reflejo-izq}} + F_{\text{reflejo-der}}
$$

### 2.2 Fuerza de Resistencia Hidrodinámica

La resistencia que ofrece el agua al nadador se modela así:

$$
F_r = \frac{1}{2} \cdot \rho \cdot A \cdot C_d \cdot v^2
$$

donde:

* $\rho$: Densidad del agua,
* $A$: Área frontal del nadador,
* $C_d$: Coeficiente de resistencia,
* $v$: Velocidad del nadador.

### 2.3 Fuerza Neta del Nadador

El nadador aplica una fuerza constante $F_s$. Sin embargo, debe usar una parte de esa fuerza para contrarrestar el movimiento lateral causado por las olas. Por eso, la fuerza efectiva para avanzar en línea recta, después de considerar el efecto de las olas y la resistencia del agua, se calcula como:

$$
F_{\text{res}} = \sqrt{F_s^2 - F_{\text{total}}^2} - F_r
$$

donde:

* $F_{\text{total}}$ representa la fuerza lateral generada por las olas,
* $F_r$ es la resistencia hidrodinámica del agua.

En resumen, la presencia de olas obliga al nadador a emplear parte de su fuerza para mantener la estabilidad lateral, reduciendo la fuerza disponible para avanzar.

---

## 3. Limitaciones

  * Las olas se propagan instantáneamente.
  * No se consideran frecuencia ni amplitud de las olas.
  * No se incluye la turbulencia ni variaciones en la técnica del nadador.
  * El nadador absorbe el 100% de la energia de ola.
  * Se ignoran factores de hidrodinámica como la velocidad critica de un casco (Hull Speed)
