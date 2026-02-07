import streamlit as st
import time 
import numpy as np
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import base64
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
import re

os.environ["OPENAI_API_KEY"] ="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"
llm = ChatOpenAI(
            temperature=0,
            model = "gpt-3.5-turbo",  # You can use other models too
            openai_api_key = os.environ["OPENAI_API_KEY"],
            base_url="https://openrouter.ai/api/v1"  # This is key to using OpenRouter
        
        )



def image_card(img_path, title, height=350):
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    html = f"""
    <div style="position:relative; width:100%;">
        <img src="data:image/png;base64,{data}"
             style="width:100%; height:{height}px;
                    object-fit:cover; border-radius:12px;">
        <div style="
            position:absolute;
            bottom:0;
            width:100%;
            background:rgba(0,0,0,0.5);
            color:white;
            text-align:center;
            padding:10px;">
            {title}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


with stylable_container(
    key="my_blue_container",
    css_styles="""
        {
            background-color: #262730;  
            border-radius: 10px;
            padding: 15px;
        }
        """
):
    # st.title("Food Delivery ChatBot", width = "content" )
    st.markdown(
        "<h1 style='text-align: center; color: white;'>" \
        "🍔 Food Ordering ChatBot 🍕</h1>", unsafe_allow_html=True)


with st.expander("See our Food Menu"):
    st.write('''
        Menu: \n
        • Indian Thali \n
        • Kadhai Chicken \n
        • Soya Aalo \n
        • Mixed Veg \n
    ''')
    # st.write("🍔")

with stylable_container(
    key="image_container",
    css_styles="""
        {
            border-radius: 10px;
            padding: 15px;
        }
        """
):
    cols = st.columns(4)
    images = [
    ("/Users/simranjeetsingh/Desktop/CPP DSA/ChatBot/FoodPic1.jpg", "Indian Thali"),
    ("/Users/simranjeetsingh/Desktop/CPP DSA/ChatBot/FoodPic2.jpg", "Kadhai Chicken"),
    ("/Users/simranjeetsingh/Desktop/CPP DSA/ChatBot/FoodPic3.jpg", "Soya Aalo"),
    ("/Users/simranjeetsingh/Desktop/CPP DSA/ChatBot/FoodPic4.jpg", "Mixed Veg"),]

    for col, (img, title) in zip(cols, images):
        with col:
            image_card(img, title)



if "message_history" not in st.session_state:
    st.session_state["message_history"] = {
        "user": [],
        "response":[]
    }
if "order_status" not in st.session_state:
    st.session_state["order_status"] = {
        "stage": "WELCOME",      # current step in flow
        "ordered_items": [],             
        "awaiting_input": None,   # what we expect next
        "checkout_confirmed": False,
        "order_complete": False
    }
MENU_MAP = {
    "indian thali": ["thali", "indian thali"],
    "kadhai chicken": ["kadhai chicken", "chicken", "kadhai"],
    "soya aalo": ["soya aalo", "soya", "aalo"],
    "mixed veg": ["mixed veg", "mixed", "veg"]
}


Query = st.chat_input("Hi There! How are You?")



if Query:
    with st.chat_message("human"):
        st.write(Query)
    
    # menu = 'indian|thali|kadhai|chicken|soya|aalo|mixed|veg'
    check_pattern = 'check|checkout|yes|proceed'

    # findings = re.findall(menu, str(Query).lower())
    # order_list = st.session_state["order_status"]["ordered_items"]
    # #if ordered_items is empty
    # if findings : # &order_list
    #     item = [ { str(findings)[i]: 1 } for i,j in enumerate(findings) ]
    #     st.session_state["order_status"]["ordered_items"].append( item )
    #     # updating ADD MORE Stage
    #     st.session_state["order_status"]["stage"] = "ADD MORE"

    found_dish = None
    for dish, aliases in MENU_MAP.items():
        for alias in aliases:
            if alias in str(Query).lower():
                found_dish = dish
                break
        if found_dish:
            break

    if found_dish:
        st.session_state["order_status"]["ordered_items"].append(
            {found_dish: 1}
        )
        st.session_state["order_status"]["stage"] = "ADD MORE"


    # Chekout Stage Updation
    user_checkout = re.search(check_pattern, str(Query).lower())
    bot_checkout_prompt = any(
        re.search( check_pattern, str(resp).lower() ) for resp in st.session_state["message_history"]["response"]
    )
    if user_checkout and bot_checkout_prompt:
        st.session_state["order_status"]["stage"] = "CHECKOUT"

    no_pattern = r"\b(no|nothing|that's all|done|nope)\b"
    if (
        st.session_state["order_status"]["stage"] == "ADD MORE"
        and re.search(no_pattern, str(Query).lower())
    ):
        st.session_state["order_status"]["stage"] = "CHECKOUT"


    history_text = ""



if Query:
    st.session_state["message_history"]["user"].append(Query)
    # st.session_state["order_status"]["stage"] = ""

    pairs = list(zip(st.session_state["message_history"]["user"], st.session_state["message_history"]["response"]))[-2:]
    for u,r in pairs:
        history_text += f"user_input: {u}, response: {r}\n"

    order_status = f"""order stage is: {st.session_state['order_status']['stage']},
    current order items,quantity are: {st.session_state['order_status']['ordered_items']},
    current checkout stage is: {st.session_state['order_status']['checkout_confirmed']}"""

    st.write(st.session_state["order_status"]["stage"])
    stage = st.session_state["order_status"]["stage"]


    prompt = ChatPromptTemplate.from_template("""
        You are a customer care agent for a food delivery platform.
        Your role is ONLY to generate the next assistant reply based strictly on the current conversation stage provided by the system.
        You MUST follow the stage exactly and NEVER change stages on your own.

        -------------------
        AVAILABLE MENU
        -------------------
        • Indian Thali
        • Kadhai Chicken
        • Soya Aalo
        • Mixed Veg

        Customers can order only from this menu.

        If the user asks for unavailable items, politely ask them to choose from the menu.

        -------------------
        CURRENT STAGE
        -------------------
        Stage: {stage}

        This stage is controlled by the system.
        You MUST obey it.

        -------------------
        CURRENT ORDER
        -------------------
        Items currently in order:
        {order_status}

        These items are already confirmed by the system.
        You must NOT change or invent items.

        -------------------
        STAGE BEHAVIOR RULES
        -------------------

        If Stage = WELCOME:
        • Welcome the user.
        • Show the menu.
        • Ask what they want to order.

        If Stage = ADD MORE:
        • Confirm items already added.
        • Ask if the user wants to add anything else.

        If Stage = CHECKOUT:
        • Ask ONLY:
        "Would you like to proceed to checkout?"

        Do NOT ask about adding items again.

        If Stage = ORDER_CONFIRMED:
        Respond ONLY with:
        "Your order is confirmed and is on its way to reach you."

        -------------------
        STRICT RULES
        -------------------
        • Never change stage.
        • Never invent items.
        • Never re-show menu unless stage is WELCOME.
        • Never ask to add items during CHECKOUT.
        • Keep responses short and polite.
        • Do not explain internal logic.

        -------------------
        CONVERSATION HISTORY
        -------------------
        {history_text}

        Generate ONLY the assistant's next reply.

    """)

    chain = prompt | llm

    response = chain.invoke({
        "order_status": order_status,
        "stage": stage,
        "history_text": history_text if history_text else None,
    })

    # Saving bot response
    st.session_state["message_history"]["response"].append(response)
    

    with st.chat_message("assistant"):
        st.write(response.content)

