import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def create_app():
    app = Flask(__name__)
    app.secret_key = "something_special"

    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        for club in clubs:
            if club["email"] == request.form["email"]:
                return render_template(
                    "welcome.html", club=club, competitions=competitions
                )
        return render_template("index.html", message="Email not found, try again")

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        if foundClub and foundCompetition:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        if placesRequired <= int(club["points"]):
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            flash("Great-booking complete!")
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            return render_template(
                "booking.html",
                club=club,
                competition=competition,
                message="Your club don't have enought points",
            )

    # TODO: Add route for points display

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
