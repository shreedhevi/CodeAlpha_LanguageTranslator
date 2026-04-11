import os
from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "fr": "French",
}


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    src_lang = data.get("src_lang", "en")
    dest_lang = data.get("dest_lang", "fr")

    if not text:
        return jsonify({"error": "Please enter some text to translate."}), 400

    if src_lang == dest_lang:
        return jsonify({"error": "Source and target languages must be different."}), 400

    if src_lang not in LANGUAGES or dest_lang not in LANGUAGES:
        return jsonify({"error": "Invalid language selection."}), 400

    try:
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return jsonify({"translated_text": result.text})
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)
