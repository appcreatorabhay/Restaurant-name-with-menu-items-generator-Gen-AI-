import streamlit as st
import os
os.environ['google_api_key']="AIzaSyARcccjt1Cn-FV6diAunpjD9aS93rXeRu8"
from langchain.llms import GooglePalm
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
api_key="AIzaSyARcccjt1Cn-FV6diAunpjD9aS93rXeRu8"
llm=GooglePalm(google_api=api_key,temperature=0.6)

st.title("Restaurant Name Generator")
cuisine=st.sidebar.selectbox("Pick a Cuisine",("Indian","Italian","Mexican","Arabic","American"))
def generate_restaurant_name_and_item(cuisine):
    template_1 = "I want to open a restuarant for {cuisine} food.Suggest a fency name for this."
    prompt_1 = ChatPromptTemplate.from_template(template_1)
    chain_1 = LLMChain(
        llm=llm,
        prompt=prompt_1,
        output_key="restaurant_name"
    )

    template_2 = """Suggest some menu items for {restaurant_name}.Return it as a comma separated values"""
    prompt_2 = ChatPromptTemplate.from_template(template_2)
    chain_2 = LLMChain(
        llm=llm,
        prompt=prompt_2,
        output_key="menu_items"
    )
    from langchain.chains import SequentialChain
    seq_chain = SequentialChain(
        chains=[chain_1, chain_2],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items']

    )
    response=seq_chain({'cuisine': 'Arabic'})
    return response


if cuisine:
    response=generate_restaurant_name_and_item(cuisine)
    st.header(response['restaurant_name'].strip())
    menu_items=response['menu_items'].strip().split(",")
    st.write("Menu Items")
    for item in menu_items:
        st.write("-",item)

