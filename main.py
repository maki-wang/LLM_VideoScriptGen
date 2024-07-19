# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 22:22
# @Author  : Maki Wang
# @FileName: main.py
# @Software: PyCharm
# !/usr/bin/env python3

import streamlit as st
from utils import generate_script

st.title('Video Script Generator')

with st.sidebar:
    openai_api_key = st.text_input("Please enter the OpenAI API key： ", type='password')
    '*****📮 Contact Xianmu Wang for the key now: wangxianmu@gmail.com*****'
    st.markdown( '[Or click here to get the OpenAI API key yourself](https://platform.openai.com/account/api-keys)')

subject = st.text_input("💡 Please enter the **subject** of the video")
video_length = st.number_input('⏱️ Please enter the approximate length of the video (in minutes)', min_value=0.1, max_value=1.0, step=0.1)
creativity = st.slider("✨ Please select the creativity of the video script (small numbers indicate more rigour, large numbers indicate more variety)",
                       min_value=0.0, max_value=1.0, value=0.2, step=0.1)
submit = st.button('Generate')

if submit and not openai_api_key:
    st.info("Please enter your OpenAI API key!")
    st.stop()
if submit and not subject:
    st.info("Please enter the subject of the video！")
    st.stop()
if submit:
    with st.spinner("AI is thinking on it, please wait..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("The video script has been generated!")
    st.subheader('🔥 Title:')
    st.write(title)
    st.subheader('📝 Video Script:')
    script
    with st.expander(' 👀 Wikipedia search results'):
        st.info(search_result)