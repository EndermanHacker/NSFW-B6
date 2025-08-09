from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Simple AI NSFW Toggle</title>
<h1>???? ???? ?????? ??????</h1>
<form method="post">
  <input type="text" name="prompt" placeholder="???? ???..." required>
  <br><br>
  <label><input type="checkbox" name="nsfw" value="true"> ????? NSFW</label>
  <br><br>
  <button type="submit">?????</button>
</form>
{% if image_url %}
  <h2>?????? ???????:</h2>
  <img src="{{ image_url }}" alt="Generated Image" style="max-width:500px;">
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        nsfw_enabled = 'nsfw' in request.form

        # ??? ??? ????? ???? ?????? API ???????? ?????? ?? ???? ????
        if nsfw_enabled:
            image_url = "https://via.placeholder.com/400x300.png?text=NSFW+Image"
        else:
            image_url = "https://via.placeholder.com/400x300.png?text=Safe+Image"

    return render_template_string(HTML, image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
