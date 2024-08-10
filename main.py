import requests
import os
import json
import datetime
import webbrowser

from flask import Flask, render_template, request, jsonify

cai_token = ""

if not os.path.isfile("TOKEN.txt"):
    print("Character.AI token could not be found! Please provide one below:")
    cai_token = input()
    with open("TOKEN.txt", "w") as file:
        file.write(cai_token)
else:
    with open("TOKEN.txt", "r") as file:
        cai_token = file.read().strip()

app = Flask(__name__)

def create_outputs_dir() -> None:
    if not os.path.isdir("outputs"):
        os.mkdir("outputs")

def send_req(token : str, prompt : str, save : bool = True) -> list:
    print("Sending request to Character.AI servers...")

    cai_req = requests.post("https://plus.character.ai/chat/character/generate-avatar-options", headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Priority": "u=3, i",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
    }, json={
        "prompt" : prompt, "num_candidates" : 4, "model_version" : "v1"
    })

    if cai_req.status_code == 200:
        print("Request successful! Downloading images...")
        converted_json : dict = json.loads(cai_req.text)
        urls : list = []
        if "result" in converted_json.keys():
            outputs : list = converted_json["result"] 
            for sub_json in outputs:
                urls.append(sub_json["url"])
        if save:
            download_urls(urls)
        print("Images downloaded!")
        return urls
    else:
        print("Request failed. Please check your internet connection, as well as the validity of the token (it can expire!)")
        return []

def download_urls(urls : list) -> None:
    create_outputs_dir()
    for i, url in enumerate(urls):
        img_req = requests.get(url)

        if img_req.status_code == 200:
            filename = f"{i}"
            with open(f"outputs/{filename}.webp", "wb") as file:
                file.write(img_req.content)
        else:
            print(f"Failed to retrieve a certain image! Status code: {img_req.status_code}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate/", methods=["POST"])
def generate():
    payload = request.get_json()
    if "prompt" in payload:
        prompt = payload["prompt"]
        if type(prompt) is str:
            return jsonify(send_req(cai_token, prompt, False))
    
    return "none"

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run()
