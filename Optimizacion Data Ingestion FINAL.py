import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import urllib.request

print("1. Extrayendo la lista oficial y viva del S&P 500 desde Wikipedia")

# Usamos la URL oficial de Wikipedia
url_sp500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Engañamos al servidor agregando un 'User-Agent' para evitar el error 403 Forbidden
peticion = urllib.request.Request(url_sp500, headers={'User-Agent': 'Mozilla/5.0'})

# Pasamos la petición simulada a Pandas para que lea la tabla sin bloqueos
with urllib.request.urlopen(peticion) as respuesta:
    tablas = pd.read_html(respuesta)
    tabla_empresas = tablas[0]

# Extraemos la columna 'Symbol' que contiene los tickers oficiales del mercado
universo_completo = tabla_empresas['Symbol'].tolist()

# Para que el escaneo no tarde demasiado en tu computadora, aislamos las primeras 50 empresas
universo_escaneo = universo_completo[:50]

# Limpieza técnica: Cambiamos puntos por guiones para que yfinance no falle (ej. BRK.B -> BRK-B)
universo_escaneo = [ticker.replace('.', '-') for ticker in universo_escaneo]

print(f"\nLista viva detectada con éxito. Analizando un entorno dinámico de {len(universo_escaneo)} activos.")

# -----------------------------------------------------------------------------------------------
# 2.1 Herramienta de fecha dinámica para que el análisis siempre se ejecute hasta el día de hoy
fecha_hoy = datetime.today().strftime('%Y-%m-%d')

print(f"\nDescargando datos históricos desde el 2021-01-01 hasta hoy ({fecha_hoy})...")
# 2.2 Se descargan los precios de cierre de todo el universo bajo análisis
datos_universo = yf.download(universo_escaneo, start="2021-01-01", end=fecha_hoy, auto_adjust=True)['Close']
print("Datos descargados exitosamente.")

# 3. Se calculan los rendimientos diarios continuamente compuestos
rendimientos_universo = np.log(datos_universo / datos_universo.shift(1)).dropna()

# 4. Calcular el rendimiento anualizado promedio de todo el universo de 50 empresas
rend_anual_universo = rendimientos_universo.mean() * 252

# EL ALGORITMO DE SELECCIÓN DINÁMICA
# Buscamos las 4 acciones con mayor rendimiento anualizado de todo el grupo analizado
rend_anual_filtrado = rend_anual_universo.nlargest(4)

# Guardamos de forma dinámica los nombres (tickers) de esas 4 ganadoras en la variable 'activos'
activos = rend_anual_filtrado.index.tolist()
print("\nALGORITMO DE SELECCIÓN COMPLETO")
print(f" Las 4 acciones líderes del entorno hoy son: {activos}")

# 5. Creamos las variables definitivas usando ÚNICAMENTE los datos de las 4 ganadoras seleccionadas
rend_anual = rend_anual_universo[activos]
cov_anual = rendimientos_universo[activos].cov() * 252

#----------------------------------------------------------------------------

#6. se define una tasa libre de riezgo, osea el rendimiento que se espera de una inversión sin riesgo, en este caso se pone un 4%
#En finanzas no existe una inversión completamente libre de riesgo, pero se suele usar el rendimiento de bonos del gobierno a corto plazo como referencia
tasa_libre_riesgo = 0.04

print("Métricas financieras base calculadas.")
print("\nRendimiento anual esperado por acción:")
print(rend_anual)


from scipy.optimize import minimize
# esto es para optimizar el portafolio, es decir para encontrar la mejor combinación de acciones que maximice el rendimiento esperado y minimice el riesgo

#7. Se crea una funcion para calcular que porcentaje de la inverison iria a cada acción segun el rendimiento anual y riesgo de cada un
#se llama estadisticas_portafolio y recibe como input los pesos de cada acción en el portafolio
def estadisticas_portafolio(pesos):
    rend_opt = np.sum(rend_anual * pesos)
    vol_opt = np.sqrt(np.dot(pesos.T, np.dot(cov_anual, pesos)))
    sharpe_opt = (rend_opt - tasa_libre_riesgo) / vol_opt
    return np.array([rend_opt, vol_opt, sharpe_opt])
# rend_opt es el rendimiento que se espera de la inverison
#vol_opt es la volatilidad o riesgo de la inversión
#sharp_opt es el ratio de sharpe # el ratio de sharpe es (Rendimiento del portafolio - Tasa libre de riesgo) / Volatilidad
#return no.array significa que la fuincion devuelve un array con el rendimiento, volatilidad y ratio de sharpe del portafolio

#8. Se crea una funcion para minimizar el ratio de sharpe, osea minimizar el riesgo ajustado al rendimiento
def minimizar_sharpe(pesos):
    return -estadisticas_portafolio(pesos)[2]
#se usa el [2] para que se tome el 3er elemento del array, osea el sharpe_opt
#se usa el 2 porque se cuenta desde el 0, entonces el 0 es rend_opt, el 1 es vol_opt y el 2 es sharpe_opt
#se pone el negativo porque daria negativo, entonces al minimizar el negativo del sharpe, se esta maximizando el sharpe
print("\nOptimizando el portafolio con sharpe.")

#9. Se definen los limites y restricciones para la optimización
#la restriccion es que la suma de los pesos debe ser 1, osea el 100% de la inversión entre las acciones
restricciones = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
#esto de restricciones es para que la suma de los pesos sea igual a 1, osea el 100% de la inversión entre las acciones
limites = tuple((0, 1) for _ in range(len(activos)))
#esto de limites es para que cada peso este entre 0 y 1, osea que no haya posiciones en corto (no se puede apostar a que una acción baje)
pesos_iniciales = [1 / len(activos)] * len(activos)
#esto es para que la optimización empiece con una asignación igualitaria entre las acciones, osea que las 4 acciones son igual de importantes al inicio

#10. Se lansza el optimizador matemático para encontrar los pesos óptimos que maximizan el ratio de sharpe ya con los limites y restricciones definidos
optimizacion = minimize(minimizar_sharpe, pesos_iniciales, method='SLSQP', bounds=limites, constraints=restricciones)
#se usa el método SLSQP (Sequential Least Squares Programming) que es un algoritmo de optimización que maneja restricciones y límites 
pesos_optimos = optimizacion.x
#esto es para obtener los pesos óptimos que se encontraron con la optimización
rend_opt, vol_opt, sharpe_opt = estadisticas_portafolio(pesos_optimos)
#se crea la existencia de rend_opt, vol_opt y sharpe_opt para obtener el rendimiento, volatilidad y ratio de sharpe del portafolio óptimo encontrado

#FINAL. Se imprimen los resultados del portafolio óptimo, incluyendo la asignación en cada acción, el rendimiento anual esperado, la volatilidad anual y el ratio de sharpe máximo
print("\nResultados de Optimización:")
for activo, peso in zip(activos, pesos_optimos):
    print(f"-Asignación en {activo}: {peso*100:.2f}%")
print(f"-Rendimiento Anual Esperado: {rend_opt*100:.2f}%")
print(f"-Volatilidad Anual (Riesgo): {vol_opt*100:.2f}%")
print(f"-Ratio de Sharpe Máximo: {sharpe_opt:.2f}")

#-------------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
print("\nGenerando simulación de Montecarlo para la Frontera Eficiente...")
#es para generar una simulación de Montecralo, para saber como seria el portafolio con diferentes combinaciones de porcentajes en cada accion

#12. Definir cuantos numeros de simulaciones se quieren hacer, en este caso 5000
num_portafolios = 5000

#se crea una matriz de 3 filas y 5000 columnas para guardr los datos de cada simulacion
#el 3 es de rendimiento, volatilidad y sharpe
#el 5000 es el numero de simulaciones que se quieren hacer
resultados = np.zeros((3, num_portafolios))

#13. Se hace un loop para simular los 5000 enscenarios de portafolios
for i in range(num_portafolios):
    pesos_aleatorios = np.random.random(len(activos))
    pesos_aleatorios /= np.sum(pesos_aleatorios)
    
    rend_p, vol_p, sharpe_p = estadisticas_portafolio(pesos_aleatorios)
    resultados[0,i] = rend_p
    resultados[1,i] = vol_p
    resultados[2,i] = sharpe_p
#se usan pesos aleatorios para cada simulacion, y se normalizan para que sumen 1, y asi se simulan diferentes combinaicones de porcentajes
#se calculan el rendimiento, volatilidad y sharpe de cada portafolio simulado, y se guardan en la matriz de resultados

#14. Se crea el grafico de la matriz de resultados
plt.figure(figsize=(10, 6))
plt.scatter(resultados[1,:], resultados[0,:], c=resultados[2,:], cmap='viridis', marker='o', s=10, alpha=0.5)
#el grafico mostrara un spread de puntos donde el color d elos puntos demuestra el ratio de sharpe, osea cuando rendimiento se obtiene segun cuanto riezgo se toma


#en el eje x se pone la volatilidad, en el eje y se pone el rendimiento, y el color de cada punto representa el ratio de sharpe
#un color más claro (amarillo) significa un ratio de sharpe más alto, osea mejor rendimiento ajustado al riesgo
plt.colorbar(label='Ratio de Sharpe')
#se agrega una barra de color para mostrar el significado de los colores en el gráfico
plt.title('Simulación de Montecarlo para la Frontera Eficiente')
#es el nombre del gráfico
plt.xlabel('Volatilidad Anualizada (Riesgo)')
#es el nombre del eje x
plt.ylabel('Rendimiento Anualizado Esperado')
#es el nombre del eje y

# --- AJUSTE DINÁMICO DE ENCUADRE DE EJES ---
min_vol_sim = np.min(resultados[1,:])
max_vol_sim = np.max(resultados[1,:])
plt.xlim(min(vol_opt, min_vol_sim) - 0.02, max_vol_sim + 0.02)
# --------------------------------------------

plt.scatter(vol_opt, rend_opt, color='red', marker='*', s=250, edgecolor='black', zorder=5, label='Portafolio Óptimo (Máximo Sharpe)')
#se agrega un punto rojo grande para mostrar el portafolio óptimo encontrado con la optimización, y asi facilitar la comparacion
plt.legend()
#se agrega una leyenda para mostrar que el punto rojo es el portafolio óptimo
plt.grid(True)
#se agrega una cuadricula para facilitar la lectura del gráfico
print("¡Proceso completado! Abriendo gráfico...")
plt.show()
#se muestra el gráfico con la simulación de Montecarlo y el portafolio óptimo destacado en rojo del entorno líder


#La estrella roja está ahí porque es el punto de máxima eficiencia. Moverse más a la derecha para ganar más rendimiento implica dormir mucho peor por las noches debido al riesgo exagerado; y moverse más abajo implica dejar dinero sobre la mesa sin necesidad.