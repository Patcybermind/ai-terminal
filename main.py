import requests

class ChatSession:
    def __init__(self):
        self.url = "https://ai.hackclub.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.messages = [
            {"role": "system", "content": "You are a terminal assitant that helps the user get what they want done in the terminal."}
        ]

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def get_response(self):
        data = {"messages": self.messages}
        response = requests.post(self.url, headers=self.headers, json=data)
        print(self.messages)
        if response.status_code == 200:
            assistant_message = response.json().get('choices')[0].get('message').get('content')
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        else:
            return f"Failed to get a response. Status code: {response.status_code}"
        

def main():
    session = ChatSession()
    print("Chat with the AI. Type 'exit' to end the session.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break 
        elif user_input == '':
            continue
        session.add_user_message(user_input)
        response = session.get_response()
        print(f"AI: {response}")

if __name__ == "__main__":
    main()