from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

app = Flask(__name__)

# Load model and tokenizer once during the app startup
model_name = "facebook/mbart-large-50-many-to-many-mmt"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

LANGUAGE_MAPPING = {
    "en": "en_XX",
    "de": "de_DE",
    "fr": "fr_XX",
    "it": "it_IT",
    "es": "es_XX",
    "cn": "zh_CN",
    "zh-CN": "zh_CN",
    # Add more mBART-compatible language mappings as needed
}

def translate_text(from_lang: str, to_lang: str, orig_text: str) -> dict: 
    tokenizer.src_lang = from_lang
    encoded_input = tokenizer(orig_text, return_tensors="pt")
    
    # Tokenize the text and generate the translation
    generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.lang_code_to_id[to_lang])
    translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    
    response = {
        "responseData": {
            "translatedText": translated_text,
        }
    }
    
    return response

def fix_spaces(input_string: str) -> str:
    return input_string.replace("%20", " ")

@app.route('/get', methods=['GET'])
def translate():
    orig_text = request.args.get('q')
    orig_text = fix_spaces(orig_text)
    langpair = request.args.get('langpair')

    if not orig_text or not langpair:
        return jsonify({"error": "Please provide 'q' (original text) and 'langpair' (from|to language codes)"}), 400
    
    # Split the langpair into from_lang and to_lang
    try:
        from_lang_code, to_lang_code = langpair.split('|')
    except ValueError:
        return jsonify({"error": "Invalid 'langpair' format. It should be in 'from|to' format."}), 400
    
    from_lang = LANGUAGE_MAPPING.get(from_lang_code)
    to_lang = LANGUAGE_MAPPING.get(to_lang_code)


    if not from_lang or not to_lang:
        return jsonify({"error": "Invalid language codes provided in 'langpair'."}), 400
    
    # Translate the text, print the result on the console and return it
    result = translate_text(from_lang, to_lang, orig_text)
    print (f"{from_lang} -> {to_lang} : {orig_text} -> {result.get('responseData').get('translatedText')}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 