#IMPORT FLASK
from flask import Flask, request, render_template, redirect, url_for
import hermesJSON

#App instance creation
hermes = Flask(__name__)


#-----PAGE VIEWS-----#
@hermes.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #FORM VALIDATION
        username = request.form['username']
        return redirect(url_for('calendar', username=username))
    else:
        return render_template('login.html')

@hermes.route('/calendar/<username>')
def calendar(username):
    
    JSONfile = hermesJSON.getJsonExample()
    
    #Obtinc una llista de totes les classes i amb les seves caracteristiques
    llistaClasses = hermesJSON.convertJSON(JSONfile)
    
    #files necessaries
    filaMax = 0
    for classe in llistaClasses:
        if classe['startRow'] > filaMax:
            filaMax = classe['startRow']
        if classe['endRow'] > filaMax:
            filaMax = classe['endRow']
    
    #Pass to Jinja2
    return render_template('calendar.html',
                           username=username,
                           llistaClasses=llistaClasses,
                           filaMax=filaMax)

@hermes.route('/help')
def help_page():
    return render_template('help.html')


#INIT
if __name__=='__main__':
    hermes.run(debug=True)