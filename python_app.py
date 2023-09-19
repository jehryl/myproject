from flask import Flask

app = Flask(__name__)

@app.route("/")

def hello_world():
    prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async
src="https://www.googletagmanager.com/gtag/js?id=G-3G2B4QB8XY"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', ' G-3G2B4QB8XY');
</script>
 """
    return prefix_google + "Hello World"

if __name__ == "__main__":
    app.run()