from flask import Flask, request, render_template_string

import requests, logging

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


# @app.route("/")
# def hello_world():
#     # Make a GET request to google.com
#     req = requests.get("https://www.google.com/")
    
#     # Retrieve the cookies from the response
#     cookies = req.cookies.get_dict()
    
    
#     # Display the cookies in your app
#     cookie_html = "<h2>Cookies from Google:</h2>"
#     for key, value in cookies.items():
#         cookie_html += f"<p>{key}: {value}</p>"
    
#     return cookie_html

# @app.route("/")
# def hello_world():
#     # Spécifiez l'URL à laquelle vous souhaitez effectuer la requête
#     url = "https://analytics.google.com/analytics/web/#/p407448032/reports/intelligenthome?params=_u..nav%3Dmaui"

#     # Effectuez la requête GET vers l'URL
#     req = requests.get(url)

#     # Vérifiez si la requête a réussi
#     if req.status_code == 200:
#         # Affichez le contenu textuel de la réponse
#         result = req.text
#     else:
#         # En cas d'erreur, affichez un message d'erreur
#         result = f"Erreur de requête : Code de statut {req.status_code}"

#     # Renvoyez le résultat comme réponse HTTP
#     return result


@app.route("/logger")
def logger():
    # Log on the server side (Python)
    app.logger.info("This is a server-side log.")

    logging.warning('okay')
    # Log on the browser side
    log_script = """
    <script>
      console.log("This is a browser-side log.");
    </script>
    """
    return "Logger Page" + log_script

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        # Récupérez le texte saisi par l'utilisateur depuis le formulaire
        user_message = request.form.get("message")
        # Vous pouvez faire quelque chose avec le message ici, comme l'afficher dans les logs côté serveur.
        app.logger.info(f"Message from user: {user_message}")
        return f"Message sent: {user_message}"

    # Affichez le formulaire pour que l'utilisateur puisse saisir un message
    return """
    <form method="POST">
        <label for="message">Entrez votre message :</label>
        <input type="text" id="message" name="message">
        <button type="submit">Envoyer</button>
    </form>
    """

if __name__ == "__main__":
    app.run()
