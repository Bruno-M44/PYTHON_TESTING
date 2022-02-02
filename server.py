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
    return render_template('booking.html', club=foundClub,
                           competition=foundCompetition)


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
    elif int(club["points"]) <= placesRequired:
        message = "Please fill a number of places less than or equal to" +\
            " number of points available (" + club["points"] + " points)"
        return render_template('booking.html', message=message,
                               competition=competition, club=club)
    elif placesRequired > 12:
        message = "Please fill a number of places less than to 12"
        return render_template('booking.html', message=message,
                               competition=competition, club=club)
    else:
        competition["numberOfPlaces"] =\
            str(int(competition["numberOfPlaces"]) - placesRequired)
        club["points"] =\
            str(int(club["points"]) - placesRequired)
        with open('competitions.json', "w") as comps:
            json.dump({"competitions": competitions}, comps)
        with open('clubs.json', "w") as comps:
            json.dump({"clubs": clubs}, comps)

        message = "Great-booking complete!"
        return render_template('welcome.html', alert="success",
                               message=message, club=club,
                               competitions=competitions)


@app.route('/publicBoard', methods=['GET'])
def public_board():
    clubs = loadClubs()
    return render_template('public_board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
