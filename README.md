# Simple Translator

A simple translator API which uses a locally running model (facebook/mbart-large-50-many-to-many-mmt) to translate from one language to another.

# Instructions

1. Clone this repository
2. CD into the directory where the app.py file is located
3. Run `python -m venv venv`
4. Run `source venv/bin/activate`
5. Run `pip install -r requirements.txt`
   _Note: This will download some python packages to the venv folder_
6. Run `python app.py`
   _Note: This will download the facebook/mbart-large-50-many-to-many-mmt model which is about 2.5GB to ~/.cache/huggingface/hub/_

At this points you should see something like:

```
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

# Usage

You can now make GET requests to http://localhost:5000/get like in the following example:

URL:

`http://localhost:5000/get?q=你这疯子，谁会给你十亿韩元？&langpair=zh-CN|e`

Response:

````{
"responseData": {
"translatedText": "Who's going to give you a billion won?"
}
}```
````
