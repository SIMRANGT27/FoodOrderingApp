🍔 Food Ordering ChatBot 🍕
A conversational Food Ordering ChatBot built using Streamlit, LangChain, and LLM APIs.
The chatbot simulates a food delivery customer care assistant that interacts with users, displays menu items, remembers orders, and guides users through the ordering and checkout process.

🚀 Features
Interactive chat interface using Streamlit
Conversational food ordering experience
Menu display inside chat
Order memory & context handling
Multi-turn conversation support
Checkout confirmation flow
Chat history persistence
Natural language responses using LLM

🛠️ Tech Stack
Python
Streamlit
LangChain
OpenAI / LLM API
Session state memory management

📌 Menu Items Available
Indian Thali
Kadhai Chicken
Soya Aalo
Mixed Veg

📂 Project Structure
food-ordering-chatbot/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
└── utils/ or modules     # Optional helper modules


⚙️ Installation & Setup

1. Clone Repository
git clone https://github.com/your-username/food-ordering-chatbot.git
cd food-ordering-chatbot
2. Create Virtual Environment (optional)
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Set API Key
Set your OpenAI API key:
export OPENAI_API_KEY="your_api_key"
or inside Python:
os.environ["OPENAI_API_KEY"] = "your_key"

▶️ Run Application
streamlit run app.py
The chatbot will open in your browser.

💬 Example Conversation
User: Show menu
Bot: Displays menu items

User: Add thali
Bot: Adds Indian Thali to order

User: Checkout
Bot: Confirms and proceeds to checkout


🧠 How It Works
User interacts via chat UI.
Session state stores chat history and order items.
Prompt is dynamically built with conversation context.
LLM generates natural responses.
Order state guides conversation flow.


🔮 Future Improvements
Add quantity handling
Cart management
Payment simulation
Order tracking
Multi-restaurant support
Recommendation system

🤝 Contribution
Contributions are welcome!
Feel free to open issues or submit pull requests.

📜 License
This project is open-source under the MIT License.

👨‍💻 Author
Simranjeet Singh