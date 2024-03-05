from langchain.schema import HumanMessage, AIMessage

def generate_chat_history(user_message, ai_message):
    chat_history = []
    user_msg = HumanMessage(content=user_message)
    ai_msg = AIMessage(content=ai_message)
    
    chat_history.append(user_msg)
    chat_history.append(ai_msg)
    
    return chat_history