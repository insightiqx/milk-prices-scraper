# Milk Prices Scraper

Proyecto personal para recopilar precios históricos de **productos lácteos en polvo**  
desde fuentes públicas (CLAL.it), mediante **técnicas de web scraping** y **análisis de datos en Python**.

---

## Fuente de datos

**CLAL.it – sección WPC (Whey Protein Concentrate)**  
[https://www.clal.it/en/index.php?section=demi](https://www.clal.it/en/index.php?section=demi)

El script captura las respuestas de red que alimentan los gráficos dinámicos de CLAL,  
extrae las series de precios (`values=`), y genera un CSV con el histórico completo.

---

## Objetivo

- Automatizar la recopilación de precios de **WPC (Whey Protein Concentrate)**,  
  **SMP (Skimmed Milk Powder)** y **WMP (Whole Milk Powder)**.
- Normalizar los datos en formato tabular (`date`, `price`, `unit`).
- Exportar resultados listos para análisis o visualización.

---

## Stack tecnológico

| Tecnología | Uso |
|-------------|-----|
| **Python 3.10+** | Lenguaje principal |
| **Playwright** | Automatización de navegador y captura de red |
| **BeautifulSoup4** | Parsing de HTML |
| **Pandas** | Limpieza y análisis de datos |
| **JupyterLab** | Exploración y visualización |
| **Git / GitHub** | Control de versiones y portfolio |

---

## Estructura del proyecto

milk-prices-scraper/
│
├── data/
│ ├── clal_powders_prices.csv # datos limpios finales
│ └── raw/ # capturas HTML, JSON, binarios
│
├── scraper/
│ ├── scrape_clal.py # scraper principal (Playwright)
│ └── utils.py # utilidades
│
├── notebooks/
│ └── analysis.ipynb # análisis y gráficos
│
├── scripts/
│ └── build_csv.py # (en desarrollo) parser general de fuentes
│
├── requirements.txt
└── README.md

yaml
Code kopieren

---

## Instalación

```bash
git clone https://github.com/<TU_USUARIO>/milk-prices-scraper.git
cd milk-prices-scraper
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
playwright install
Ejecución
1. Captura de datos (scraper)
bash
Code kopieren
python scraper/scrape_clal.py
2️. Parseo de datos
bash
Code kopieren
# convierte los archivos de red (JSON / BIN) a CSV limpio
# salida: data/clal_powders_prices.csv
python notebooks/parse_clal_bin.ipynb
Resultados (WPC)
Fecha	Precio (USD/Ton)
2020-01-01	2206.29
2020-02-01	2235.64
...	...
2025-11-01	4073.61

70 filas (2020–2025)
Unidad: USD/Tons
Periodicidad: mensual

Próximos pasos
 Añadir scraping para SMP y WMP.

 Enriquecer con fuentes FAO / USDA / Eurostat.

 Crear dashboard en Streamlit o Tableau.

 Publicar en GitHub Pages con visualización interactiva.

Licencia y uso ético
Los datos pertenecen a CLAL.it.
Este proyecto tiene fines educativos y de portfolio.
Antes de reutilizar los datos, consulta los Términos de uso de CLAL y respeta el robots.txt.

Autor
Claudia Liehr
📧 insightiqx@gmail.com
🌐 github.com/insightiqx
