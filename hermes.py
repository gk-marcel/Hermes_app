#IMPORT FLASK
from flask import Flask, session, request, render_template, redirect, url_for
import jsonParse

#App instance creation
hermes = Flask(__name__)


#-----PAGE VIEWS-----#
@hermes.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #FORM VALIDATION
        session['username'] = request.form['username']
        return redirect(url_for('calendar'))
    else:
        return render_template('login.html')

@hermes.route('/calendar')
def calendar():
    
    #Importacio de l'arxiu
    JSONfile = jsonParse.getJsonExample()
    
    #Llista de totes les classes amb les seves dades
    llistaClasses = jsonParse.convertJSON(JSONfile)
    
    #Files necessaries del calendari
    filaMax = jsonParse.filesNecessaries(llistaClasses)
    
    #Altura files
    alturaFiles = 30
    
    #Passar dades a Jinja2
    return render_template('calendar.html',
                           username=session['username'],
                           llistaClasses=llistaClasses,
                           filaMax=filaMax,
                           alturaFiles=alturaFiles)

@hermes.route('/help')
def help_page():
    return render_template('help.html')

# secret key
hermes.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

#INIT
if __name__=='__main__':
    hermes.run(debug=True)