import openai
import tinify
import requests
from jinja2 import Template

def gen_text(promt, api_key):
    openai.api_key = api_key
    r = openai.Completion.create(
      model="text-davinci-003",
      prompt=promt,
      temperature=0.7,
      max_tokens=400,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    raw_text = r["choices"][0]["text"]
    return raw_text

def gen_image(promt, api_key):
    openai.api_key = api_key
    r = openai.Image.create(prompt=promt,size="512x512")
    image_url = r['data'][0]['url']
    return image_url

def compress_image(image_url, api_key, filename, html_folder):
    tinify.key = api_key
    source = tinify.from_url(image_url)
    source.to_file(f"{html_folder}{filename}.png")

def text_to_html(raw_text):
    lines = raw_text.split('\n')
    html_output = ""
    for line in lines:
        if line.strip():
            html_output += f"<p>{line.strip()}</p>"
    return html_output

def domain_to_name(domain):
    first_word = domain.split('.')[0]
    capitalized_first_word = first_word[0].upper() + first_word[1:]
    return capitalized_first_word

def gen_html(template, name, text, filename, html_folder):
    with open(template) as file_:
        template = Template(file_.read())
    html = template.render(name=name, text=text)
    output_file = f"{html_folder}{filename}.html"
    f = open(output_file, "w")
    f.write(html)

def upload_image_to_bunny(filename, api_key):
    url = f"https://storage.bunnycdn.com/dwarfs/dwarfs/{filename}.png"
    image_file = open(f"/tmp/{filename}.png", 'rb').read()
    headers = {
        "AccessKey": api_key,
        "content-type": "application/octet-stream"
    }
    response = requests.put(url, data=image_file, headers=headers)
    print(response.text)