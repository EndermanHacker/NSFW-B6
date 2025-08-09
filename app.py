from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # ضع توكن Hugging Face هنا في متغير البيئة

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        nsfw_enabled = request.form.get("nsfw") == "on"

        # يمكنك تعديل الـ payload حسب الحاجة وخصائص الـ API، هنا فقط مثال
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }
        # يمكنك إضافة تأثير على NSFW بناءً على nsfw_enabled إذا كان API يدعم ذلك

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # حسب الـ API ستحتاج تعديل الجزء هذا لاستخراج الصورة
            # نفترض أنها base64 مشفرة في result['images'][0]
            # لكن API الرسمي غالباً يرجع رابط أو بيانات أخرى
            # هنا مثال لو كانت base64:
            image_data = result.get('images', [None])[0]
            if image_data:
                img_src = f"data:image/png;base64,{image_data}"
                return render_template("index.html", img_src=img_src, prompt=prompt)
            else:
                return render_template("index.html", error="لم يتم توليد الصورة.", prompt=prompt)
        else:
            return render_template("index.html", error=f"خطأ من السيرفر: {response.status_code}", prompt=prompt)
    return render_template("index.html", img_src=None)

if __name__ == "__main__":
    app.run(debug=True)
