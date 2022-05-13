import json
from datetime import date
from flask import Flask, render_template, request, redirect, flash, url_for, abort


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

    CURRENT_DATE = str(date.today())

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        for club in clubs:
            if club["email"] == request.form["email"]:
                return render_template(
                    "welcome.html",
                    club=club,
                    competitions=competitions,
                    clubs=clubs,
                    current_date=CURRENT_DATE,
                )
        return render_template("index.html", message="Email not found, try again")

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        foundClub = [c for c in clubs if c["name"] == club]
        foundCompetition = [c for c in competitions if c["name"] == competition]
        if foundClub and foundCompetition:
            return render_template(
                "booking.html", club=foundClub[0], competition=foundCompetition[0]
            )
        else:
            abort(404)

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        message = ""
        if request.form["places"]:
            placesRequired = int(request.form["places"])
            if placesRequired > 12:
                message = "You can't book more than 12 places per competition"
            elif placesRequired > int(competition["numberOfPlaces"]):
                message = "There is not enought place in this competition"
            elif placesRequired * 3 > int(club["points"]):
                message = "Your club don't have enought points"
            else:
                competition["numberOfPlaces"] = (
                    int(competition["numberOfPlaces"]) - placesRequired
                )
                club["points"] = int(club["points"]) - (placesRequired * 3)
                flash("Great-booking complete!")
                return render_template(
                    "welcome.html",
                    club=club,
                    competitions=competitions,
                    clubs=clubs,
                    current_date=CURRENT_DATE,
                )
        return render_template(
            "booking.html", club=club, competition=competition, message=message
        )

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":  # pragma: no cover
    app.run()
