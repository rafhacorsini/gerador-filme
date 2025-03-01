import random
import requests
import streamlit as st

# Configuração da página
st.set_page_config(page_title="🎬 Gerador de Filmes e Séries", page_icon="🎥", layout="centered")

st.title("🎬 Gerador de Ideias de Filmes e Séries com Streaming")
st.subheader("Escolha suas preferências para receber uma recomendação real de filme ou série!")

# TMDb API Key (SUBSTITUA AQUI PELA SUA CHAVE)
API_KEY = "3948c9b289ac216da4f76886628891f1"
LANG = "pt-BR"

# Opções de streamings disponíveis
streaming_opcoes = {
    "Netflix": "8",
    "Amazon Prime": "9",
    "Disney+": "337",
    "HBO Max": "384",
    "Apple TV+": "350"
}

# Gêneros disponíveis
generos = {
    "Ação": 28, "Drama": 18, "Suspense": 53, "Ficção Científica": 878, "Comédia": 35,
    "Romance": 10749, "Terror": 27, "Fantasia": 14, "Documentário": 99
}

# Pergunta ao usuário se quer filme ou série
tipo_conteudo = st.radio("📺 Você quer assistir a um Filme ou Série?", ("Filme", "Série"))

# Opção de gênero
genero_escolhido = st.selectbox("🎭 Escolha um gênero ou deixe o app escolher automaticamente:",
                                ["Escolher para mim"] + list(generos.keys()))

# Escolha do serviço de streaming
streaming_escolhido = st.selectbox("🎬 Escolha um serviço de streaming (opcional):",
                                   ["Qualquer um"] + list(streaming_opcoes.keys()))

# Determinar ID do gênero
if genero_escolhido == "Escolher para mim":
    genero_id = None  # Filme em alta sem filtro de gênero
else:
    genero_id = generos[genero_escolhido]


def buscar_conteudo():
    """Busca um filme ou série com base nas escolhas do usuário."""
    tipo_api = "movie" if tipo_conteudo == "Filme" else "tv"
    base_url = f"https://api.themoviedb.org/3/discover/{tipo_api}?api_key={API_KEY}&sort_by=popularity.desc&language={LANG}"

    if genero_id:
        base_url += f"&with_genres={genero_id}"

    if streaming_escolhido != "Qualquer um":
        base_url += f"&with_watch_providers={streaming_opcoes[streaming_escolhido]}&watch_region=BR"

    response = requests.get(base_url)
    if response.status_code == 200:
        conteudos = response.json().get("results", [])
        if conteudos:
            return random.choice(conteudos)
    return None


if st.button("🎥 Gerar Recomendação!"):
    conteudo = buscar_conteudo()
    if conteudo:
        titulo = conteudo["title"] if tipo_conteudo == "Filme" else conteudo["name"]
        sinopse = conteudo["overview"] if conteudo["overview"] else "Sinopse não disponível."
        nota = conteudo["vote_average"]
        poster_url = f"https://image.tmdb.org/t/p/w300{conteudo['poster_path']}" if conteudo.get(
            "poster_path") else None

        st.success(f"🎬 Sua recomendação: **{titulo}**")
        st.write(f"📖 **Sinopse:** {sinopse}")
        st.write(f"⭐ **Nota:** {nota}/10")

        if streaming_escolhido != "Qualquer um":
            st.write(f"🎥 Disponível em: {streaming_escolhido}")

        if poster_url:
            st.image(poster_url, caption=titulo, use_container_width=False, width=300)
    else:
        st.error("Não foi possível encontrar um conteúdo no momento. Tente novamente!")
