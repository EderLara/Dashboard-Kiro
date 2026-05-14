import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Supertienda", layout="wide")

@st.cache_data
def cargar_datos(archivo):
    """Carga la hoja 'Compras' del Excel."""
    return pd.read_excel(archivo, sheet_name="Compras")

def main():
    st.title("📊 Dashboard de Actividad - Supertienda")
    st.markdown("Sube el archivo `BD_Supertienda.xlsx` para visualizar los resultados de la hoja *Actividad*.")

    uploaded_file = st.file_uploader("📤 Subir archivo Excel", type=["xlsx"])
    if not uploaded_file:
        st.warning("Por favor, sube el archivo para generar el dashboard.")
        return

    # Cargar datos
    df = cargar_datos(uploaded_file)

    # ---------------------------------------------------------
    # ✅ ACTIVIDADES PREVIAS
    # ---------------------------------------------------------
    # 1. Cambiar formatos de fecha a aaaa-mm-dd
    df["Fecha del pedido"] = pd.to_datetime(df["Fecha del pedido"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["Fecha de envío"] = pd.to_datetime(df["Fecha de envío"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    # 2. Calcular tiempo transcurrido entre envío y pedido en días
    df["Tiempo transcurrido (días)"] = (pd.to_datetime(df["Fecha de envío"]) - pd.to_datetime(df["Fecha del pedido"])).dt.days
    
    # 3. Calcular valor unitario (Ventas / Cantidad)
    df["Valor unitario"] = df["Ventas"] / df["Cantidad"]

    # Mostrar vista rápida de las transformaciones
    with st.expander("🔍 Ver transformación de datos (primeras filas)"):
        st.dataframe(df[["Id. del pedido", "Fecha del pedido", "Fecha de envío", 
                         "Tiempo transcurrido (días)", "Ventas", "Cantidad", "Valor unitario"]].head(10))

    # Dimensiones requeridas por la actividad
    dimensiones = [
        "Método de envío", "Segmento", "Ciudad", 
        "Provincia/Estado/Departamento", "País/Región", "Región"
    ]

    # ---------------------------------------------------------
    # 📊 ORGANIZACIÓN POR PESTAÑAS
    # ---------------------------------------------------------
    tab_ventas, tab_devoluciones, tab_categorias, tab_productos = st.tabs([
        "📦 Ventas por dimensión", 
        "↩️ Devoluciones por dimensión", 
        "📂 Categorías por dimensión", 
        "🛒 Productos por dimensión"
    ])

    def generar_graficos(tab, titulo_base, df_filtro, metrica_tipo):
        """Función auxiliar para generar los 6 gráficos por pestaña."""
        with tab:
            st.subheader(titulo_base)
            cols = st.columns(2)  # Disposición en 2 columnas
            
            for i, dim in enumerate(dimensiones):
                with cols[i % 2]:
                    if metrica_tipo == "ventas":
                        # Conteo de filas (líneas de venta)
                        res = df_filtro[dim].value_counts().reset_index()
                        res.columns = [dim, "Cantidad de ventas"]
                        y_col = "Cantidad de ventas"
                        
                    elif metrica_tipo == "devoluciones":
                        # Filtrar solo donde Devuelto == "Sí"
                        df_dev = df_filtro[df_filtro["Devuelto Si/NO"].str.strip().str.lower() == "sí"]
                        res = df_dev[dim].value_counts().reset_index()
                        res.columns = [dim, "Cantidad de devoluciones"]
                        y_col = "Cantidad de devoluciones"
                        
                    elif metrica_tipo == "categorias":
                        # Categorías únicas por dimensión
                        res = df_filtro.groupby(dim)["Categoría"].nunique().reset_index()
                        res.columns = [dim, "Categorías únicas"]
                        y_col = "Categorías únicas"
                        
                    elif metrica_tipo == "productos":
                        # Productos únicos por dimensión
                        res = df_filtro.groupby(dim)["Nombre del producto"].nunique().reset_index()
                        res.columns = [dim, "Productos únicos"]
                        y_col = "Productos únicos"

                    # Crear gráfico
                    fig = px.bar(
                        res, 
                        x=dim, 
                        y=y_col, 
                        title=f"{titulo_base.split(' - ')[0]} por {dim}",
                        height=380,
                        color=y_col,
                        color_continuous_scale="Viridis"
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

    # Generar gráficos para cada sección
    generar_graficos(tab_ventas, "📦 Cantidad de ventas por dimensión", df, "ventas")
    generar_graficos(tab_devoluciones, "↩️ Cantidad de devoluciones por dimensión", df, "devoluciones")
    generar_graficos(tab_categorias, "📂 Cantidad de categorías por dimensión", df, "categorias")
    generar_graficos(tab_productos, "🛒 Cantidad de productos por dimensión", df, "productos")

if __name__ == "__main__":
    main()