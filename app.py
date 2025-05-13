import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenAI client setup
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
MODEL = os.getenv("CHAT_MODEL", "gpt-4o")

# Streamlit page config
st.set_page_config(page_title="飲み会話題ジェネレータ", layout="wide")
st.title("飲み会お手伝いAI「宴会トーク君」")
st.write("福岡、長崎、東京の参加者が楽しめる話題を提案します")
st.write("---")

# UI: Region and topic category selection
tab_selection, tab_generate = st.tabs(["設定", "話題を生成"])

with tab_selection:
    st.header("設定")
    regions = st.multiselect(
        "参加者の地域を選択してください",
        options=["福岡", "長崎", "東京"],
        default=["福岡", "長崎", "東京"]
    )
    categories = st.multiselect(
        "話題のカテゴリを選択してください",
        options=["方言", "食文化", "観光スポット", "おすすめの飲み処", "地元の行事"],
        default=["方言", "食文化"]
    )
    st.markdown("選択した地域: **" + ', '.join(regions) + "**")
    st.markdown("選択したカテゴリ: **" + ', '.join(categories) + "**")

with tab_generate:
    st.header("話題を生成")
    if st.button("話題を生成する"):
        if not regions or not categories:
            st.error("地域とカテゴリを両方選択してください。")
        else:
            prompt = (
                f"飲み会で盛り上がる話題を１つ考えて提示してください。最初の話始めも提示してください。"
                f"参加者は{','.join(regions)}出身の人です。"
                f"観点として、{','.join(categories)}を含めてください。"
            )
            with st.spinner("話題を考え中... 🌟"):
                response = openai_client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are a friendly party host who suggests fun conversation topics."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                topics = response.choices[0].message.content
                st.markdown("**生成された話題:**")
                st.write(topics)
