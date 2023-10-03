from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/")
def hello_world():
    prefix_google = """ <!-- Google tag (gtag.js) -->
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

@app.route("/logger")
def logger():
    # Log on the server side (Python)
    app.logger.info("This is a server-side log.")

    # Log on the browser side
    log_script = """
    <script>
      console.log("This is a browser-side log.");
    </script>
    """
    return "Logger Page" + log_script

if __name__ == "__main__":
    app.run()
