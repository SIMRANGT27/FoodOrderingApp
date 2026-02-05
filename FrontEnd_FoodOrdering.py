import streamlit as st
import time 
import numpy as np
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import base64
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


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

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "prev_query" not in st.session_state:
    st.session_state.prev_query = "None"

if "prev_response" not in st.session_state:
    st.session_state.prev_response = "None"

if "order" not in st.session_state:
    st.session_state.order = []

if "checkout" not in st.session_state:
    st.session_state.checkout = False

# ---------- User Input ----------
Query = st.chat_input("Hi There! How are You?")

# ---------- Detect ordered items ----------
if Query:
    q = str(Query).lower()

    if "soya" in q:
        st.session_state.order = ["Soya Aalo"]
    elif "thali" in q:
        st.session_state.order = ["Indian Thali"]
    elif "kadhai" in q:
        st.session_state.order = ["Kadhai Chicken"]
    elif "mixed" in q or "veg" in q:
        st.session_state.order = ["Mixed Veg"]
    if "checkout" in q or "place order" in q:
        st.session_state.checkout = True

# ---------- Display chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- Main Chat Logic ----------
if Query:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": Query}
    )

    with st.chat_message("user"):
        st.write(Query)

    # Build conversation history
    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages[-6:]
    )

    # Prompt
    prompt = ChatPromptTemplate.from_template("""
        You are a professional customer care agent for a food delivery platform.

        Menu:
        • Indian Thali
        • Kadhai Chicken
        • Soya Aalo
        • Mixed Veg

        Mention menu only once initially.

        Current confirmed order:
        {order}

        Conversation so far:
        {history}

        Your previous response:
        {previous_response}

        User query:
        {query}
        Checkout status: {checkout}

        If an item already exists in Current confirmed order,
        do NOT ask again what item user wants.
        Also, refrain from adding the role of User/assisstant and previous conversation in response.
        If checkout status is True,stop asking about adding items and proceed to order completion.
        Instead, proceed toward confirmation or checkout naturally.
    """)

    chain = prompt | llm

    response = chain.invoke({
        "query": Query,
        "history": history_text,
        "previous_response": st.session_state.prev_response,
        "order": ", ".join(st.session_state.order) or "None",
        "checkout": st.session_state.checkout
    })

    # Save bot response
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

    with st.chat_message("assistant"):
        st.write(response.content)

    # Update memory
    st.session_state.prev_query = Query
    st.session_state.prev_response = response.content


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
 


# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
#     index=None,
#     placeholder="Select contact method...",
# )

# st.write("You selected:", option)

# st.radio(
#         "Set selectbox label visibility 👉",
#         key="visibility",
#         options=["visible", "hidden", "collapsed"],
#     )

# with st.status("Downloading data..."):
#     st.write("Searching for data...")
#     time.sleep(2)
#     st.write("Found URL.")

# st.button("Rerun")




# _LOREM_IPSUM = """
# Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
# incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
# nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
# """
# def stream_data():
#     for word in _LOREM_IPSUM.split(" "):
#         yield word + " "
#         time.sleep(0.02)

#     yield pd.DataFrame(
#         np.random.randn(5, 10),
#         columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
#     )


# if st.button("Stream data"):
#     st.write_stream(stream_data)