import openai
import os
import requests
import tkinter as tk

# Create a function to save the API keys
def save_api_keys():
    # Get the API keys from the user input
    openai_api_key = openai_api_key_input.get()
    plagscan_api_key = plagscan_api_key_input.get()

    # Save the API keys to a file
    with open("api_keys.txt", "w") as f:
        f.write(f"{openai_api_key}\n")
        f.write(f"{plagscan_api_key}\n")

    # Hide the API key input widgets and show the prompt input and generate button
    openai_api_key_label.pack_forget()
    openai_api_key_input.pack_forget()
    plagscan_api_key_label.pack_forget()
    plagscan_api_key_input.pack_forget()
    provide_api_keys_label.pack_forget()
    prompt_label.pack(padx=10, pady=10)
    prompt_input.pack(padx=10, pady=10)
    generate_button.pack(padx=10, pady=10)

# Create a function to generate text and check for plagiarism
def generate_text():
    # Get the prompt from the user input
    prompt = prompt_input.get()

    # Get the API keys from the saved file
    with open("api_keys.txt", "r") as f:
        openai_api_key = f.readline().strip()
        plagscan_api_key = f.readline().strip()

    # Authenticate with the OpenAI API
    openai.api_key = openai_api_key

    # Initialize a variable to keep track of whether the text is plagiarized
    is_plagiarized = True

    # Keep generating text until a non-plagiarized version is obtained
    while is_plagiarized:
        # Send a request to the OpenAI API to generate text
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Get the generated text
        generated_text = response.choices[0].text

        # Check the generated text for plagiarism
        plagiarism_checker_url = "https://api.plagscan.com/v3/searchurl"
        payload = {
            "url": generated_text,
            "exclude_quotes": True,
            "min_percent_match": 0,
            "return_doc_info": False,
            "private_index": False,
            "report_type": "standard",
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {plagscan_api_key}",
        }
        response = requests.post(plagiarism_checker_url, json=payload, headers=headers)

        # If the text is not plagiarized, update the output text and set the is_plagiarized variable to False
        if response.status_code == 200 and response.json()["results"][0]["percent"] == 0:
            output_text.set(generated_text)
            is_plagiarized = False
        # If the text is plagiarized, update the prompt and continue the loop
        else:
            prompt = prompt + " " + generated_text.split()[-1]
# Create a login function
def login():
    # Hide the login widgets and show the API key input widgets
    login_button.pack_forget()
    name_label.pack_forget()
    name_input.pack_forget()
    email_label.pack_forget()
    email_input.pack_forget()
    password_label.pack_forget()
    password_input.pack_forget()
    provide_api_keys_label.pack(padx=10, pady=10)
    openai_api_key_label.pack(padx=10, pady=10)
    openai_api_key_input.pack(padx=10, pady=10)
    plagscan_api_key_label.pack(padx=10, pady=10)
    plagscan_api_key_input.pack(padx=10, pady=10)
    submit_api_keys_button.pack(padx=10, pady=10)

# Create a function to check if the API keys are saved
def check_api_keys():
    if os.path.isfile("api_keys.txt"):
        # Hide the API key input widgets and show the prompt input and generate button
        openai_api_key_label.pack_forget()
        openai_api_key_input.pack_forget()
        plagscan_api_key_label.pack_forget()
        plagscan_api_key_input.pack_forget()
        provide_api_keys_label.pack_forget()
        prompt_label.pack(padx=10, pady=10)
        prompt_input.pack(padx=10, pady=10)
        generate_button.pack(padx=10, pady=10)
    else:
        # Show the API key input widgets
        provide_api_keys_label.pack(padx=10, pady=10)
        openai_api_key_label.pack(padx=10, pady=10)
        openai_api_key_input.pack(padx=10, pady=10)
        plagscan_api_key_label.pack(padx=10, pady=10)
        plagscan_api_key_input.pack(padx=10, pady=10)
        submit_api_keys_button.pack(padx=10, pady=10)

# Create the main window
window = tk.Tk()
window.title("AI Text Generator")

# Create the login widgets
name_label = tk.Label(window, text="Name:")
name_label.pack(padx=10, pady=10)
name_input = tk.Entry(window)
name_input.pack(padx=10, pady=10)
email_label = tk.Label(window, text="Email:")
email_label.pack(padx=10, pady=10)
email_input = tk.Entry(window)
email_input.pack(padx=10, pady=10)
password_label = tk.Label(window, text="Password:")
password_label.pack(padx=10, pady=10)
password_input = tk.Entry(window, show="*")
password_input.pack(padx=10, pady=10)
login_button = tk.Button(window, text="Login", command=login)
login_button.pack(padx=10, pady=10)

# Create the API key input widgets
provide_api_keys_label = tk.Label(window, text="Please provide your OpenAI and PlagScan API keys.")
openai_api_key_label = tk.Label(window, text="OpenAI API key:")
openai_api_key_input = tk.Entry(window)
plagscan_api_key_label = tk.Label(window, text="PlagScan API key:")
plagscan_api_key_input = tk.Entry(window)
submit_api_keys_button = tk.Button(window, text="Submit", command=save_api_keys)

# Create the main widgets
prompt_label = tk.Label(window, text="Please enter a prompt:")
prompt_input = tk.Entry(window)
generate_button = tk.Button(window, text="Generate Text", command=generate_text)
output_text = tk.StringVar()
output_text.set("")
output_label = tk.Label(window, textvariable=output_text, wraplength=500)

# Check if API keys are saved
check_api_keys()

# Pack the widgets
window.mainloop()