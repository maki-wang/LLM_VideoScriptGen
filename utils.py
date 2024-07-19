# -*- coding: utf-8 -*-
# @Time    : 2024/7/12 23:29
# @Author  : Maki Wang
# @FileName: utils.py
# @Software: PyCharm
# !/usr/bin/env python3

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

# 把所有和AI大模型交互的代码都放于此文件中
# 为了对请求进行封装，定义函数：
def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ('human', "请为{subject}这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    model = ChatOpenAI(openai_api_key = api_key, temperature = creativity)

    title_chain = title_template | model
    script_chain = script_template | model
    title = title_chain.invoke({"subject":subject})

    #langchain_community这个库有一个utilities的模块，其下有一个叫WikipediaAPIWrapper的类，其内部会用喂鸡百科官方API进行搜索并返回搜索结果摘要
    #创建这个类的实例，并调用run方法（参数传入搜索词字符串）进行搜索
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke({"title":title, "duration":video_length, "wikipedia_search":search_result}).content

    return search_result, title.content, script

#测试
# print(generate_script("南宁大沙田周阴婷",1.3, 1.3, 'sk-proj-irmQo7yzbyd5O8aXeImUT3BlbkFJVJKThChw1cGRGU23OzbI'))

