from transformers import pipeline
import gradio as gr
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Emoções via Hugging Face
classificador = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Spotify API
client_id = "21055a6291b94081a7d64c9f4306f574"
client_secret = "14f14b3eebe7407f8ebb0645345c119d"
auth = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth)

# Emoção → Estilo musical
mapa_emocao_query = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "metal",
    "fear": "dark ambient",
    "love": "romantic",
    "optimism": "uplifting",
    "boredom": "lofi",
    "excitement": "party",
    "surprise": "experimental",
    "disgust": "grunge"
}

# Função para detectar emoção
def detectar_emocao(texto):
    resultado = classificador(texto)[0]
    return resultado['label'].lower()

# Função para recomendar músicas
def recomendar_musicas(emocao):
    query = mapa_emocao_query.get(emocao, "chill")
    resultados = sp.search(q=query, type="track", limit=5)

    sugestoes = []
    for item in resultados['tracks']['items']:
        nome = item['name']
        artista = item['artists'][0]['name']
        link = item['external_urls']['spotify']
        imagem = item['album']['images'][0]['url']
        sugestoes.append({
            "nome": nome,
            "artista": artista,
            "link": link,
            "imagem": imagem
        })
    return sugestoes

# Função principal da interface
def interface(texto):
    emocao = detectar_emocao(texto)
    sugestoes = recomendar_musicas(emocao)

    resposta = f"🎭 Emoção detectada: **{emocao}**\n\n🎧 Sugestões musicais:\n\n"
    for s in sugestoes:
        resposta += f"![Capa]({s['imagem']})\n"
        resposta += f"**{s['nome']}** - {s['artista']}\n"
        resposta += f"[🔗 Ouvir no Spotify]({s['link']})\n\n"
    return resposta

# Interface Gradio
gr.Interface(
    fn=interface,
    inputs=gr.Textbox(lines=3, placeholder="Como você está se sentindo hoje?"),
    outputs="markdown",
    title="🎶 Emoções & Músicas",
    description="Digite seu sentimento e receba músicas que combinam com seu estado emocional."
).launch()
