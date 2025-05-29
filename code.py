import streamlit as st
from streamlit_lottie import st_lottie
import requests
import random

st.set_page_config(page_title="MBTI Quiz", page_icon="🧠", layout="centered")

# --- Load Lottie Animation ---
@st.cache_resource
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Character Animation (Duolingo-style consistent avatar with expressive reactions)
character_emotions = {
    "idle": "https://assets4.lottiefiles.com/packages/lf20_touohxv0.json",
    "excited": "https://assets2.lottiefiles.com/packages/lf20_khzniaya.json",
    "surprised": "https://assets4.lottiefiles.com/private_files/lf30_kqshlcsb.json",
    "cheer": "https://assets2.lottiefiles.com/packages/lf20_4kx2q32n.json",
    "wave": "https://assets4.lottiefiles.com/packages/lf20_gjmecwii.json"
}

# Load MBTI animation
mbti_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json")

# --- Personality Avatars ---
avatars = {
    "INTP": "🧠", "ENFP": "🎉", "INFJ": "🌙", "ESTJ": "📈",
    "ENTP": "🧩", "ISFJ": "🛡️", "ESFP": "🎭", "ISTJ": "📘",
    "INFP": "🧚", "ENTJ": "🏆", "ISTP": "🔠️", "ESFJ": "🍱",
    "ISFP": "🎨", "ENFJ": "🤝", "INTJ": "♟️", "ESTP": "🚀"
}

# --- Avatar Images ---
avatar_images = {
    "INTP": "https://static.neris-assets.com/images/personality-types/avatars/intp-logician.png",
    "ENFP": "https://static.neris-assets.com/images/personality-types/avatars/enfp-campaigner.png",
    "INFJ": "https://static.neris-assets.com/images/personality-types/avatars/infj-advocate.png",
    "ESTJ": "https://static.neris-assets.com/images/personality-types/avatars/estj-executive.png",
    "ENTP": "https://static.neris-assets.com/images/personality-types/avatars/entp-debater.png",
    "ISFJ": "https://static.neris-assets.com/images/personality-types/avatars/isfj-defender.png",
    "ESFP": "https://static.neris-assets.com/images/personality-types/avatars/esfp-entertainer.png",
    "ISTJ": "https://static.neris-assets.com/images/personality-types/avatars/istj-logistician.png",
    "INFP": "https://static.neris-assets.com/images/personality-types/avatars/infp-mediator.png",
    "ENTJ": "https://static.neris-assets.com/images/personality-types/avatars/entj-commander.png",
    "ISTP": "https://static.neris-assets.com/images/personality-types/avatars/istp-virtuoso.png",
    "ESFJ": "https://static.neris-assets.com/images/personality-types/avatars/esfj-consul.png",
    "ISFP": "https://static.neris-assets.com/images/personality-types/avatars/isfp-adventurer.png",
    "ENFJ": "https://static.neris-assets.com/images/personality-types/avatars/enfj-protagonist.png",
    "INTJ": "https://static.neris-assets.com/images/personality-types/avatars/intj-architect.png",
    "ESTP": "https://static.neris-assets.com/images/personality-types/avatars/estp-entrepreneur.png"
}

# --- Questions ---
questions = [
    # IE
    {"q": "I prefer large gatherings over intimate conversations.", "dim": "IE", "dir": "E"},
    {"q": "I feel recharged after spending time alone.", "dim": "IE", "dir": "I"},
    {"q": "I enjoy being the center of attention.", "dim": "IE", "dir": "E"},
    {"q": "Too much socializing drains me.", "dim": "IE", "dir": "I"},
    {"q": "I initiate conversations easily.", "dim": "IE", "dir": "E"},
    {"q": "I prefer listening over speaking in groups.", "dim": "IE", "dir": "I"},

    # NS
    {"q": "I trust facts more than theories.", "dim": "NS", "dir": "S"},
    {"q": "I notice patterns and ideas often.", "dim": "NS", "dir": "N"},
    {"q": "I'm more interested in what could be than what is.", "dim": "NS", "dir": "N"},
    {"q": "I prefer concrete examples over abstract ideas.", "dim": "NS", "dir": "S"},

    # TF
    {"q": "I make decisions based on logic.", "dim": "TF", "dir": "T"},
    {"q": "Empathy is more important than being right.", "dim": "TF", "dir": "F"},
    {"q": "I believe fairness means treating everyone the same.", "dim": "TF", "dir": "T"},
    {"q": "Compassion is more important than cold logic.", "dim": "TF", "dir": "F"},

    # JP
    {"q": "I like having a schedule.", "dim": "JP", "dir": "J"},
    {"q": "I prefer to keep things open-ended.", "dim": "JP", "dir": "P"},
    {"q": "I get anxious without a clear plan.", "dim": "JP", "dir": "J"},
    {"q": "I enjoy spontaneity more than planning.", "dim": "JP", "dir": "P"},
]

scale = ["Very Unlikely", "Unlikely", "Neutral", "Likely", "Very Likely"]
weights = [-2, -1, 0, 1, 2]

# --- Session State ---
if "current" not in st.session_state:
    st.session_state.current = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"I": 0, "E": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
if "emotion" not in st.session_state:
    st.session_state.emotion = "idle"

# if "header_loaded" not in st.session_state:
#     header_container = st.empty()
#     with header_container:
#         st.title("🧠 MBTI Personality Quiz")
#         if mbti_animation:
#             st_lottie(mbti_animation, height=150, speed=0, loop=True)
#     st.session_state.header_loaded = True
# else:
#     st.title("🧠 MBTI Personality Quiz") 

# st.progress(st.session_state.current / len(questions))

st.title("🧠 MBTI Personality Quiz")
if mbti_animation:
    st_lottie(mbti_animation, height=150, speed=0, loop=True)

st.progress(st.session_state.current / len(questions))

# --- Animated Character ---
char_animation = load_lottieurl(character_emotions[st.session_state.emotion])
if char_animation:
    st_lottie(char_animation, height=120, key="avatar")

# --- Main Quiz Flow ---
if st.session_state.current < len(questions):
    q = questions[st.session_state.current]
    st.subheader(f"Q{st.session_state.current + 1}: {q['q']}")
    choice = st.radio("How true is this for you?", scale, key=f"q{st.session_state.current}")

    if st.button("Next"):
        weight = weights[scale.index(choice)]
        if weight != 0:
            st.session_state.scores[q["dir"]] += weight
        st.session_state.current += 1
        st.session_state.emotion = random.choice(["excited", "surprised", "cheer", "wave"])
        st.rerun()
else:
    def winner(a, b):
        return a if st.session_state.scores[a] >= st.session_state.scores[b] else b

    mbti = ""
    mbti += winner("I", "E")
    mbti += winner("N", "S")
    mbti += winner("T", "F")
    mbti += winner("J", "P")

    st.balloons()
    st.toast("✨ You did it!", icon="✨")
    st.toast("🌟 Discover your personality!", icon="🌟")

    st.success(f"🎉 You are likely an **{mbti}** personality type!")

    img_url = avatar_images.get(mbti)
    if img_url:
        st.markdown(
            f"<div style='text-align:center;'>"
            f"<img src='{img_url}' style='border-radius: 50%; width: 150px; height: 150px;' alt='{mbti} avatar'>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown(f"## Your Avatar: {avatars.get(mbti, '✨')}")

    detailed_descriptions = {
        "INTP": "The Thinker – Analytical, logical, imaginative. Enjoys deep thinking, problem-solving, and independent research. Values logic over emotion and often lost in thought.",
        "ENFP": "The Campaigner – Energetic, creative, sociable. Embraces new experiences, passionate about ideas, and highly empathetic. Loves inspiring and connecting with people.",
        "INFJ": "The Advocate – Insightful, idealistic, and driven by core values. Seeks deeper meaning in relationships and life. Often serves others with empathy and strategy.",
        "ESTJ": "The Executive – Organized, direct, natural leaders. Values tradition and order. Reliable in managing tasks and teams efficiently.",
        "ENTP": "The Debater – Quick-witted, resourceful, and curious. Loves exploring new ideas and debating for fun. Challenges norms and thinks outside the box.",
        "ISFJ": "The Defender – Loyal, detail-oriented, and warm. Cares deeply for others and works behind the scenes to maintain harmony and support.",
        "ESFP": "The Entertainer – Vibrant, fun-loving, and energetic. Lives in the moment and thrives on social interaction. Loves spreading joy.",
        "ISTJ": "The Logistician – Responsible, serious, dependable. Values tradition and logic. Reliable planners and meticulous workers.",
        "INFP": "The Mediator – Deep, introspective, compassionate. Driven by core values and creativity. Empathizes with others and often drawn to the arts.",
        "ENTJ": "The Commander – Strategic, confident, and visionary. Strong-willed leaders who thrive on challenges and goal-setting.",
        "ISTP": "The Virtuoso – Curious, action-oriented, and independent. Tinkers with things to understand how they work. Calm in a crisis.",
        "ESFJ": "The Consul – Social, attentive, and caring. Focuses on others' needs and keeps everyone organized. Values community and tradition.",
        "ISFP": "The Adventurer – Artistic, gentle, and spontaneous. Loves beauty and exploration. Values freedom and living true to self.",
        "ENFJ": "The Protagonist – Inspiring, empathetic, and sociable. Natural leaders with strong ideals and a desire to uplift others.",
        "INTJ": "The Architect – Innovative, perfectionistic, and determined. Future-focused planners who love mastery and efficiency.",
        "ESTP": "The Dynamo – Bold, perceptive, and action-loving. Thrives on excitement, challenge, and making things happen."
    }
    st.info(detailed_descriptions.get(mbti, "You have a unique personality mix!"))

    if st.button("Restart Quiz"):
        del st.session_state.current
        del st.session_state.scores
        del st.session_state.emotion
        st.rerun()
