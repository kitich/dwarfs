from fastapi import FastAPI
import os
from dotenv import dotenv_values
from ai import gen_text, gen_image, compress_image, text_to_html, domain_to_name, gen_html

app = FastAPI()

config = {**dotenv_values(".env"),  **os.environ}
openai_api_key = config['OPENAI_API_KEY']
tinify_api_key = config['TINIFY_API_KEY']
html_folder = config['HTML_FOLDER']

@app.get("/")
def read_root():
    return {"Dwarf API"}

@app.get("/api/{type}/{domain}")
def read_root(domain: str, type: str):
    if type == "dwarf":
        name = domain_to_name(domain)
        text_promt = f"Short story abou dwarf with surname {name}. Make him some name. Story up to 300 words."
        image_promt = f"Dwarf named {name} pencil drawing"
        template = "templates/dwarf.jinja2"
    if type == "star":
        name = domain_to_name(domain)
        text_promt = f"Tell me what do you know about star {name}. Add details who and when discovered it. Story up to 200 words."
        image_promt = f"Star {name} in deep space"
        template = "templates/star.jinja2"

    print(f"Generating {type} {name} text")
    raw_text = gen_text(text_promt, openai_api_key)
    text_html = text_to_html(raw_text)
    print(f"Generating {type} {name} image")
    image_url = gen_image(image_promt, openai_api_key)
    print(f"Compressing {type} {name} image")
    compress_image(image_url, tinify_api_key, name, html_folder)
    print(f"Generating {type} {name} html")
    gen_html(template, name, text_html, domain, html_folder)

    return {"raw_text": f"{raw_text}",
            "html_text": f"{text_html}",
            "image_url": f"{image_url}",
            }