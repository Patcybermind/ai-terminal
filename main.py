import requests
import json
import os
import time
import copy




class ChatSession:
    def __init__(self):
        self.url = "https://ai.hackclub.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.messages = [
            {"role": "system", "content": "You are a terminal assitant that helps the user get what they want done in the terminal."}
        ]
        self.existing_session = False
        
    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def get_messages(self):
        return self.messages

    def get_response(self):
        data = {"messages": self.messages}
        response = requests.post(self.url, headers=self.headers, json=data)
        #print(self.messages)
        if response.status_code == 200:
            assistant_message = response.json().get('choices')[0].get('message').get('content')
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        else:
            return f"Failed to get a response. Status code: {response.status_code}"
        
    
        

def main():
    session = ChatSession()
    print('Type "exit" to exit session.\n')
    valid_input = False
    while valid_input == False:
        continue_last_session = input("do you wish to continue with the last session? (y/n): ").lower()
        if continue_last_session == 'y' or continue_last_session == 'yes':
            with open("data/data.json", 'r') as json_file:
                data = json.load(json_file)
                last_session = data.get("last_session")
                if last_session:
                    with open("sessions/" + last_session, 'r') as json_file:
                        session.messages = json.load(json_file)
                        print("Continuing last session...")
                else:
                    print("No last session found.")
                valid_input = True
        
        elif continue_last_session == 'n' or continue_last_session == 'no':
            print("Starting a new session...")
            valid_input = True
        else:
            print("Invalid input.")

    while True:
        user_input = input("\n  you: ")
        if user_input.lower() == 'exit':
            exit_sequence(session)
            break 

        session.add_user_message(user_input)
        response = session.get_response()
        print(f"\n  AI: {response}")





def exit_sequence(session):
    json_data = copy.deepcopy(session.get_messages())

    session.add_user_message("The user has ended the session. Choose a name that represents the session and that the user will be able to associate with this session when he sees it. Only respond with the name you chose, put space between words, do NOT end it with .json and make sure that if the user asks a question center the answer around the main idea and make it recoginsable..")
 
    ai_decided_name = session.get_response() + ".json"

    

    with open( "sessions/" + ai_decided_name, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print("\n   Session saved as " + ai_decided_name + "\n")
    json_data = {"last_session": ai_decided_name}
    
    with open("data/data.json", 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    





if __name__ == "__main__":
    main()