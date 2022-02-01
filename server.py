import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    competitions = loadCompetitions()
    clubs = loadClubs()
    message = ""
    if not request.form["email"]:
        message = "Please fill out this field"
        return render_template('index.html', message=message)
    elif request.form["email"] not in [club["email"] for club in clubs]:
        message = "Please fill mail from an existing club"
        return render_template('index.html', message=message)
    else:
        club = [club for club in clubs if club['email']
                == request.form['email']][0]
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    competitions = loadCompetitions()
    clubs = loadClubs()
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competitions = loadCompetitions()
    clubs = loadClubs()
    competition = [c for c in competitions if c['name'] ==
                   request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    if not request.form['places'].isdigit():
        message = "Please enter a number"
        return render_template('booking.html', message=message,
                               competition=competition, club=club)

    placesRequired = int(request.form['places'])

    if int(competition["numberOfPlaces"]) < placesRequired:
        message = "Please fill a number of places less than or equal to" +\
            " number of places available"
        return render_template('booking.html', message=message,
                               competition=competition, club=club)
    else:
        competition["numberOfPlaces"] =\
            str(int(competition["numberOfPlaces"]) - placesRequired)
        with open('competitions.json', "w") as comps:
            json.dump({"competitions": competitions}, comps)

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club,
                               competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
