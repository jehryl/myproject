from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    prefix_google = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G2B4QB8XY"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-3G2B4QB8XY');
</script>
"""
    button_html = """
<button onclick="sendEventToGoogleAnalytics()">Send Event to Google Analytics</button>
<script>
  function sendEventToGoogleAnalytics() {
    gtag('event', 'button_click', {
      'event_category': 'Custom Events',
      'event_label': 'Button Clicked'
    });
    alert('Event sent to Google Analytics!');
  }
</script>
"""
    return prefix_google + "Hello World" + button_html

if __name__ == "__main__":
    app.run()
