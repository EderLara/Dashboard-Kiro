# 📊 Dashboard Supertienda

Dashboard interactivo construido con **Streamlit** y **Plotly** para analizar datos de ventas, devoluciones, categorías y productos de una supertienda a partir de un archivo Excel.

## 🚀 Características

- Carga dinámica de archivos Excel (`BD_Supertienda.xlsx`)
- Transformaciones automáticas de datos:
  - Conversión de fechas al formato `YYYY-MM-DD`
  - Cálculo del tiempo de envío (días entre pedido y envío)
  - Cálculo del valor unitario por producto
- Visualizaciones interactivas organizadas en 4 pestañas:
  - **Ventas por dimensión**
  - **Devoluciones por dimensión**
  - **Categorías por dimensión**
  - **Productos por dimensión**
- Gráficos de barras con escala de color Viridis para 6 dimensiones:
  - Método de envío, Segmento, Ciudad, Provincia/Estado/Departamento, País/Región, Región

## 🛠️ Requisitos

- Python 3.9 o superior
- Las dependencias listadas en `requirements.txt`

## ⚙️ Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd dashboard
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uso

```bash
streamlit run app.py
```

Luego abre el navegador en `http://localhost:8501`, sube el archivo `BD_Supertienda.xlsx` y explora los gráficos.

## 📁 Estructura del proyecto

```
dashboard/
├── app.py               # Aplicación principal
├── requirements.txt     # Dependencias del proyecto
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

## 📦 Datos esperados

El archivo Excel debe contener una hoja llamada **Compras** con al menos las siguientes columnas:

| Columna | Descripción |
|---|---|
| `Id. del pedido` | Identificador único del pedido |
| `Fecha del pedido` | Fecha en que se realizó el pedido |
| `Fecha de envío` | Fecha en que se envió el pedido |
| `Ventas` | Valor total de la venta |
| `Cantidad` | Cantidad de unidades vendidas |
| `Devuelto Si/NO` | Indica si el producto fue devuelto |
| `Categoría` | Categoría del producto |
| `Nombre del producto` | Nombre del producto |
| `Método de envío` | Tipo de envío utilizado |
| `Segmento` | Segmento de cliente |
| `Ciudad` | Ciudad del pedido |
| `Provincia/Estado/Departamento` | Provincia o estado |
| `País/Región` | País o región |
| `Región` | Región geográfica |
