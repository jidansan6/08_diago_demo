import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("CHAT_MODEL", "gpt-4o")

# Streamlit config
st.set_page_config(page_title="今日のメニュー提案", layout="wide")
st.title("今日の気分＆体調メニュー提案アプリ")
st.write("気分と体調、好みのジャンルを選んで、オススメの食事メニューを提案します！")
st.write("---")

# Dropdown options
moods = ["快調","元気だけど軽め希望","疲れている","ストレス多い","のんびりモード"]
conditions = ["良好","少しだるい","胃もたれ","風邪気味","消化を助けたい"]
cuisines = ["和食","洋食","中華","イタリアン","ヘルシー","スイーツ" ]

# User selections
mood = st.selectbox("今日の気分は？", moods)
condition = st.selectbox("今日の体調は？", conditions)
cuisine = st.selectbox("お好みの料理ジャンルを選択", cuisines)

# Generate button
generate = st.button("メニューを提案する")

if generate:
    prompt = (
        f"あなたは料理のエキスパートです。ユーザーの気分: {mood}、体調: {condition}、"
        f"料理ジャンル: {cuisine} に合わせて、今日の食事メニューを3つ提案してください。"
    )
    with st.spinner("メニューを考案中...🍽️"):
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful chef giving menu suggestions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        menu = response.choices[0].message.content
        st.subheader("今日のメニュー提案")
        st.write(menu)
