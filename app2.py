import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Netflix", layout="wide", page_icon="🎬")

@st.cache_data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra y prepara solo las películas a partir de un DataFrame ya cargado."""
    movies = df[df['type'] == 'Movie'].copy()
    movies['year_added'] = pd.to_datetime(movies['date_added']).dt.year
    movies['duration_min'] = movies['duration'].str.extract(r'(\d+)').astype(int)
    return movies


def load_and_clean_data() -> pd.DataFrame:
    """
    Intenta cargar 'movies_df.csv' desde disco.
    Si no lo encuentra, muestra un file_uploader para que el usuario lo suba.
    Devuelve el DataFrame limpio o detiene la app si aún no hay datos.
    """
    # 1. Intentar carga desde disco
    try:
        df = pd.read_csv("movies_df.csv")
        return clean_data(df)
    except FileNotFoundError:
        pass

    # 2. Archivo no encontrado → ofrecer carga manual
    st.warning(
        "⚠️ No se encontró `movies_df.csv` en la carpeta del proyecto. "
        "Puedes subir el archivo manualmente:"
    )
    uploaded = st.file_uploader(
        "📤 Subir archivo CSV de Netflix",
        type=["csv"],
        help="Sube el archivo 'movies_df.csv' para continuar.",
    )

    if uploaded is None:
        st.info("Esperando el archivo para generar el dashboard…")
        st.stop()

    df = pd.read_csv(uploaded)
    return clean_data(df)


df_movies = load_and_clean_data()

# ==========================================
# TÍTULO PRINCIPAL
# ==========================================
st.title("🎬 Dashboard de Películas Netflix")
st.markdown("Análisis exploratorio basado en los metadatos de `movies_df.csv`")

# ==========================================
# 1. ¿EN QUÉ AÑO SE CARGARON MÁS PELÍCULAS?
# ==========================================
st.header("📅 1. Año con mayor cantidad de películas cargadas")
year_counts = df_movies['year_added'].value_counts().sort_index().reset_index()
year_counts.columns = ['Año', 'Cantidad']

# Calcular el año máximo
max_year_idx = year_counts['Cantidad'].idxmax()
max_year = year_counts.loc[max_year_idx, 'Año']
max_count = year_counts.loc[max_year_idx, 'Cantidad']

col1, col2 = st.columns([1, 3])
with col1:
    st.metric(label="Año con más uploads", value=int(max_year), delta=f"{max_count} películas")
with col2:
    fig_year = px.bar(year_counts, x='Año', y='Cantidad', 
                      title='Evolución de películas cargadas por año',
                      color='Cantidad', color_continuous_scale='Bluered')
    st.plotly_chart(fig_year, use_container_width=True)

# ==========================================
# 2. ¿CUÁNTAS PELÍCULAS HAY POR DIRECTOR?
# ==========================================
st.header("🎬 2. Cantidad de películas por director")

# Expandir directores: cada fila tendrá un director y su duración correspondiente
directors_df = (
    df_movies[['director', 'duration_min']]
    .dropna(subset=['director'])
    .assign(director=lambda x: x['director'].str.split(','))
    .explode('director')
    .assign(director=lambda x: x['director'].str.strip())
)
directors_df = directors_df[directors_df['director'] != 'Not Given']

# Agregar: cantidad de películas y promedio de duración por director
director_stats = (
    directors_df
    .groupby('director', as_index=False)
    .agg(
        Cantidad=('duration_min', 'count'),
        Duración_promedio_min=('duration_min', 'mean')
    )
    .sort_values('Cantidad', ascending=False)
    .rename(columns={'director': 'Director'})
)
director_stats['Duración_promedio_min'] = director_stats['Duración_promedio_min'].round(1)

st.dataframe(
    director_stats,
    use_container_width=True,
    height=400,
    column_config={
        "Duración_promedio_min": st.column_config.NumberColumn(
            "Duración promedio (min)", format="%.1f min"
        )
    }
)

# Gráfico Top 10 — barras de cantidad con promedio de duración superpuesto
top_10 = director_stats.head(10)

fig_director = px.bar(
    top_10,
    x='Director',
    y='Cantidad',
    title='Top 10 Directores: cantidad de películas y duración promedio',
    color='Cantidad',
    color_continuous_scale='Viridis',
    hover_data={'Duración_promedio_min': True},
    labels={'Duración_promedio_min': 'Duración promedio (min)'},
)

# Línea secundaria con el promedio de duración
fig_director.add_scatter(
    x=top_10['Director'],
    y=top_10['Duración_promedio_min'],
    mode='lines+markers',
    name='Duración promedio (min)',
    yaxis='y2',
    line=dict(color='tomato', width=2),
    marker=dict(size=7),
)

fig_director.update_layout(
    yaxis2=dict(
        title='Duración promedio (min)',
        overlaying='y',
        side='right',
        showgrid=False,
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
)

st.plotly_chart(fig_director, use_container_width=True)

# ==========================================
# 3. ¿CUÁNTAS PELÍCULAS POR RATING?
# ==========================================
st.header("🔞 3. Distribución de películas por Rating")
rating_counts = df_movies['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Cantidad']

col3, col4 = st.columns(2)
with col3:
    fig_rating_pie = px.pie(rating_counts, values='Cantidad', names='Rating', 
                            title='Proporción por Rating', hole=0.4)
    st.plotly_chart(fig_rating_pie, use_container_width=True)
with col4:
    fig_rating_bar = px.bar(rating_counts, x='Rating', y='Cantidad', 
                            title='Cantidad absoluta por Rating',
                            color='Rating', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_rating_bar, use_container_width=True)

# ==========================================
# 4. ¿QUÉ DIRECTOR HIZO LA PELÍCULA MÁS LARGA?
# ==========================================
st.header("⏱️ 4. Director de la película más larga")

# Encontrar la película con mayor duración
idx_max_duration = df_movies['duration_min'].idxmax()
longest = df_movies.loc[idx_max_duration]

st.info("🎞️ **Película más larga del catálogo:**")
col5, col6, col7 = st.columns(3)
col5.metric("Duración", f"{int(longest['duration_min'])} min")
col6.metric("Año de Estreno", int(longest['release_year']))
col7.metric("Rating", str(longest['rating']))

st.markdown(f"### 🏆 `{longest['title']}`")
st.markdown(f"**Director(es):** `{longest['director']}`")
st.markdown(f"**Géneros:** `{longest['listed_in']}`")
st.markdown(f"**País:** `{longest['country']}`")

# Footer
st.divider()
st.caption("Dashboard generado con Streamlit • Datos cargados desde `movies_df.csv`")