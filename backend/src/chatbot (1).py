import google.generativeai as genai

# Setup Google Generative AI configuration
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample phone numbers for healthcare institutions
healthcare_resources = (
    "If you are facing a mental health crisis, please contact the following helplines:\n"
    "1. National Mental Health Helpline (Kiran): 1800-599-0019 (24/7)\n"
    "2. Snehi Mental Health Helpline: 91-22-2772 6771\n"
    "3. Vandrevala Foundation: 1860-2662-345\n"
    "4. iCall - TISS Helpline: 9152987821\n"
    "5. Sangath COVID-19 Mental Health Helpline: 011-41198666 (Mon-Sat, 10 AM - 6 PM)\n\n"
    "For general health support, you can reach out to:\n"
    "6. National Health Helpline: 1800-180-1104\n"
    "7. Arogya Setu Helpline: 1075 (COVID-19 Queries)\n"
    "8. National AIDS Control Organisation: 1097\n"
    "9. Childline India: 1098 (Support for children in distress)\n"
    "10. Women Helpline: 181 (Support for women facing abuse or health issues)\n"
)

def is_serious_concern(message):
    serious_keywords = [
        'suicide', 'harm', 'self-harm', 'depression', 'anxiety', 'overwhelmed', 'hopeless', 
        'panic', 'panic attack', 'fear', 'loneliness', 'trauma', 'abuse', 'grief', 
        'sadness', 'worthless', 'isolation', 'danger', 'dangerous thoughts', 'anger', 
        'bipolar', 'schizophrenia', 'eating disorder', 'bulimia', 'anorexia', 'PTSD', 
        'self-injury', 'cutting', 'distress', 'crying', 'helpless', 'nightmares', 
        'substance abuse', 'alcoholism', 'drug addiction', 'withdrawal', 'paranoia'
    ]
    return any(keyword in message.lower() for keyword in serious_keywords)

def process_message(last_15_days_history, current_day_history, session_history, user_query):
    # Check for serious concerns in the user query
    if is_serious_concern(user_query):
        prompt = (
            "It sounds like you might be going through a tough time. It's important to talk to someone who can help. "
            "As your mental healthcare assistant, I recommend contacting these resources:\n"
            f"{healthcare_resources}\n"
            "I'm here to support you and offer guidance as well. Feel free to continue talking to me."
        )
        return prompt

    # Generate a response using the user query and histories with appropriate weighting
    prompt = (
        f"You are a mental healthcare assistant. Your role is to provide support to the user, listen carefully, "
        f"and offer empathetic responses. Make sure to give more weight to the user's query first, "
        f"followed by the session history, current day history, and then the last 15 days' history.\n"
        f"User Query: {user_query}\n"
        f"Session History: {session_history}\n"
        f"Current Day History: {current_day_history}\n"
        f"Last 15 Days History: {last_15_days_history}\n"
        f"Chatbot:"
    )

    response = model.generate_content(prompt)
    return response.text

# Exportable function
def main(last_15_days_history, current_day_history, session_history, user_query):
    return process_message(last_15_days_history, current_day_history, session_history, user_query)

