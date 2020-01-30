
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Repaso de python 3 y analisis de precios OHLC                              -- #
# -- Codigo: principal.py - script principal de proyecto                                  -- #
# -- Rep: https://github.com/ITESOIF/MyST/tree/master/Notas_Python/Notas_RepasoPython     -- #
# -- Autor: Francisco ME                                                                  -- #
# -- ------------------------------------------------------------------------------------ -- #

# -- ------------------------------------------------------------- Importar con funciones -- #

import funciones as fn                              # Para procesamiento de datos
import visualizaciones as vs                        # Para visualizacion de datos
import pandas as pd                                 # Procesamiento de datos
from datos import OA_Ak                             # Importar token para API de OANDA

# -- --------------------------------------------------------- Descargar precios de OANDA -- #

# token de OANDA
OA_In = "EUR_USD"                  # Instrumento
OA_Gn = "D"                        # Granularidad de velas
fini = pd.to_datetime("2019-07-06 00:00:00").tz_localize('GMT')  # Fecha inicial
ffin = pd.to_datetime("2019-12-06 00:00:00").tz_localize('GMT')  # Fecha final

# Descargar precios masivos
df_pe = fn.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                             p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)

# -- --------------------------------------------------------------- Graficar OHLC plotly -- #

vs_grafica1 = vs.g_velas(p0_de=df_pe.iloc[0:120, :])
vs_grafica1.show()

# -- ------------------------------------------------------------------- Conteno de velas -- #

# multiplicador de precios
pip_mult = 10000

# -- 0A.1: Hora
df_pe['hora'] = [df_pe['TimeStamp'][i].hour for i in range(0, len(df_pe['TimeStamp']))]

# -- 0A.2: Dia de la semana.
df_pe['dia'] = [df_pe['TimeStamp'][i].weekday() for i in range(0, len(df_pe['TimeStamp']))]

# -- 0B: Boxplot de amplitud de velas (close - open).
df_pe['co'] = (df_pe['Close'] - df_pe['Open'])*pip_mult

# -- ------------------------------------------------------------ Graficar Boxplot plotly -- #
vs_grafica2 = vs.g_boxplot_varios(p0_data=df_pe[['co']], p1_norm=False)
vs_grafica2.show()
#%%
'laboratorio'
'''Este laboratorio sirve para generar nueva información de los precios a partir de los históricos en formato  OHLC (Open, High, Low, Close). Esta nueva información generada, la mayoría almacenada como nuevas columnas dentro del DataFrame que contiene los precios históricos OHLC, puede ser utilizada también como "variables explicativas" en modelos predictivos (ya sean de regresión o de clasificación). El enfóque de los cálculos que deberás de realizar para este laboratorio es "estadístico" utilizando información de las "velas".  También vas a poner en práctica algunos códigos simples para graficar utilizando la librería de Plotly, todo esto utilizando una lógica de organizar el código con base a "funciones" y scripts separados (algo bastante útil para proyectos aplicados de python).

Deberás de incluir en esta entrega sólamente la liga del repositorio donde se encuentra tu laboratorio. El repositorio deberá de contener, por lo menos, dos archivos. El script de tus códigos hechos (un archivo .py) y el notebook con tu versión final, donde escribirás texto y código con comentarios (utilizando el formato de notebooks que te pase).

Las funciones contenidas en el ejemplo visto en clase fueron:

['hora'] : Hora de la vela
La hora expresada en formato de 24hrs, en la que ocurrió la vela.

['dia'] : Dia de la semana de la vela
Día de la semana en formato numérico (0 = domingo, 1 = lunes, etc), en el que ocurrió la vela.

vs.g_boxplot: Boxplot de amplitud de velas (close - open).
Diagrama de caja y bigote para visualizar la dispersión de los "pips" de diferencia entre el precio Close y el precio Open de cada vela. También para resaltar los atípicos de los datos utilizados.


Las funciones a desarrollar individualmente son las siguientes:
(1pt) ['mes'] : Mes en el que ocurrió la vela.
Utilizando la columna de TimeStamp calcula el "Mes" en el que ocurrió la vela.

(1pt) ['sesion'] : Sesion de la vela
Sesión bursátil en la que ocurrió la vela,  el valor dentro de la columna deberás de colocarlo siguiendo la siguiente regla:

'asia':  si en la columna ['hora'] tiene alguno de estos valores -> 22, 23, 0, 1, 2, 3, 4, 5, 6, 7
'asia_europa': si en la columna ['hora'] tiene alguno de estos valores -> 8
'europa': si en la columna ['hora'] tiene alguno de estos valores -> 9, 10, 11, 12 
'europa_america': si en la columna ['hora'] tiene alguno de estos valores -> 13, 14, 15, 16
'america': si en la columna ['hora'] tiene alguno de estos valores -> 17, 18, 19, 20, 21
Recuerda que el ['TimeStamp'] de los precios que están descargándose en el código está en huso horario UTC, así que no aplicará a las horas de Guadalajara", sino, a las horas de cualquier centro bursátil que esté bajo el huso horario UTC, como lo es el caso de Londres que tiene huso horario GMT = 0.

(1pt) ['oc']: Amplitud de vela (en pips).
Calcular la diferencia entre las columnas ['Open'] y ['Close'], expresarla en pips.

(1pt) ['hl']: Amplitud de extremos (en pips).
Calcular la diferencia entre las columnas ['High'] y ['Low'], expresarla en pips.

(.5pt) ['sentido'] : Sentido de la vela (alcista o bajista)
En esta columna debes de asignarle el valor de 'alcista' para cuando ['Close'] >= ['Open'] y 'bajista' en el caso contrario.

(.5pt) ['sentido_c'] Conteo de velas consecutivas alcistas/bajistas.
En el DataFrame de los precios OHLC, para cada renglon, ir acumulando el valor de velas consecutivas ALCISTAS o BAJISTAS e ir haciendo el conteo de ocurrencia para cada caso. Se comienza el conteo a partir de la primera repetición, por ejemplo, ['sentido_c'] tendrá un 2  en el tiempo t cuando en el tiempo t-2 y tiempo t-1 haya sido el mismo valor que en el tiempo t. En este ejemplo ['sentido_c'] tendría un 2 (en el tiempo t-2 fue la primera vela, y la vela en tiempo t-1 y en tiempo t fueron 2 velas fueron consecutivamente en el mismo sentido).

(1pt) Ventanas móviles de volatilidad
Utiliza la columna de ['hl'] como una medida de "volatilidad" en pips de las velas. Con esta columna, genera las siguientes columnas haciendo una "ventana móvil" del máximo de esos últimos n valores. Las columnas serán 3, una para cada valor de la "volatilidad móvil" para 5, 25 y 50 velas de histórico respectivamente.

['volatilidad_5']: Utilizando la información de las 5 anteriores velas.
['volatilidad_25']: Utilizando la información de las 25 anteriores velas.
['volatilidad_50']: Utilizando la información de las 50 anteriores velas.
Recuerda que la "volatilidad" en una serie de tiempo financiera es, usualmente, la desviación estándar de los rendimientos, sin embargo, uno puedeo proponer otros "estadísticos" para representar la "variabilidad" entre los datos. En este caso, probaremos generar esta información sólo tomando en cuenta la columna ['hl']. Así que, no es necesario calcular rendimientos en esta ocasión.

(1pt) Gráfica con Plotly
Realiza una propuesta de gráfica utilizando alguna de las columnas que has generado y la librería plotly. Las reglas son las siguientes:

Tiene que tener título de gráfica
Tiene que tener título de eje x y etiquetas de eje x
Tiene que tener título de eje y y etiquetas de eje y
Se debe de poder visualizar una leyenda (en cualquier posición).'''
