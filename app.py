from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

### TODO:
#       - näytä keitä oot tykännyt
#       - näytä keiden kanssa match
#       - cancel like option? or not
#       - oman profiilin muokkaaminen
#       - handle tyhjät/jne/validoi/jne form jne
#       - hakuominaisuutta?
#       - form CSRF fix:
#               <input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">
