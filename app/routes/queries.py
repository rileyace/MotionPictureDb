from flask import Blueprint, render_template, request
from app.database import Database

queries_bp = Blueprint("query", __name__)


@queries_bp.route("/list_tables")
def list_tables():
    """List all tables in the database."""

    # >>>> TODO 1: Write a query to list all the tables in the database. <<<<

    query = """show tables;"""

    with Database() as db:
        tables = db.execute(query)
    return render_template("list_tables.html", tables=tables)


@queries_bp.route("/search_movie", methods=["POST"])
def search_movie():
    """Search for movies by name."""
    movie_name = request.form["movie_name"]

    # >>>> TODO 2: Search Motion Picture by Motion picture name. <<<<
    #              List the `name`, `rating`, `production` and `budget`.

    query = """select mp.name, mp.rating, mp.production, mp.budget
                from motionpicture mp
                where mp.name like %s
                ;"""

    with Database() as db:
        movies = db.execute(query, (f"%{movie_name}%",))
    return render_template("search_results.html", movies=movies)


@queries_bp.route("/search_liked_movies", methods=["POST"])
def search_liked_movies():
    """Search for movies liked by a specific user."""
    user_email = request.form["user_email"]

    # >>>> TODO 3: Find the movies that have been liked by a specific user’s email. <<<<
    #              List the movie `name`, `rating`, `production` and `budget`.

    query = """select mp.name, mp.rating, mp.production, mp.budget
                from motionpicture mp, user u, likes l, movie m
                where mp.id = m.mpid and u.email = l.uemail and l.mpid = mp.id and u.email like %s;"""

    with Database() as db:
        movies = db.execute(query, (user_email,))
    return render_template("search_results.html", movies=movies)


@queries_bp.route("/search_by_country", methods=["POST"])
def search_by_country():
    """Search for movies by country using the Location table."""
    country = request.form["country"]

    # >>>> TODO 4: Search motion pictures by their shooting location country. <<<<
    #              List only the motion picture names without any duplicates.

    query = """select distinct mp.name
                from motionpicture mp, location l
                where mp.id = l.mpid and l.country like %s;"""

    with Database() as db:
        movies = db.execute(query, (country,))
    return render_template("search_results_by_country.html", movies=movies)


@queries_bp.route("/search_directors_by_zip", methods=["POST"])
def search_directors_by_zip():
    """Search for directors and the series they directed by zip code."""
    zip_code = request.form["zip_code"]

    # >>>> TODO 5: List all directors who have directed TV series shot in a specific zip code. <<<<
    #              List the director name and TV series name only without duplicates.

    query = """SELECT DISTINCT p.name, mp.name
                FROM people p, motionpicture mp, series s, location l, role r
                WHERE r.role_name = "Director"
                and r.pid = p.id
                and mp.id = s.mpid
                and l.mpid = mp.id
                and l.zip = %s;"""

    with Database() as db:
        results = db.execute(query, (zip_code,))
    return render_template("search_directors_results.html", results=results)


@queries_bp.route("/search_awards", methods=["POST"])
def search_awards():
    """Search for award records where the award count is greater than `k`."""
    k = int(request.form["k"])

    # >>>> TODO 6: Find the people who have received more than “k” awards for a single motion picture in the same year. <<<<
    #              List the person `name`, `motion picture name`, `award year` and `award count`.

    query = """ """

    with Database() as db:
        results = db.execute(query, (k,))
    return render_template("search_awards_results.html", results=results)


@queries_bp.route("/find_youngest_oldest_actors", methods=["GET"])
def find_youngest_oldest_actors():
    """
    Find the youngest and oldest actors based on the difference
    between the award year and their date of birth.
    """

    # >>>> TODO 7: Find the youngest and oldest actors to win at least one award. <<<<
    #              List the actor names and their age (at the time they received the award).
    #              The age should be computed from the person’s date of birth to the award winning year only.
    #              In case of a tie, list all of them.

    query = """ """

    with Database() as db:
        actors = db.execute(query)

    # Filter out actors with null ages (if any)
    actors = [actor for actor in actors if actor[1] is not None]
    if actors:
        min_age = min(actors, key=lambda x: x[1])[1]
        max_age = max(actors, key=lambda x: x[1])[1]
        youngest_actors = [actor for actor in actors if actor[1] == min_age]
        oldest_actors = [actor for actor in actors if actor[1] == max_age]
        return render_template(
            "actors_by_age.html",
            youngest_actors=youngest_actors,
            oldest_actors=oldest_actors,
        )
    else:
        return render_template(
            "actors_by_age.html", youngest_actors=[], oldest_actors=[]
        )


@queries_bp.route("/search_producers", methods=["POST"])
def search_producers():
    """
    Search for American producers based on a minimum box office collection and maximum budget.
    """
    box_office_min = float(request.form["box_office_min"])
    budget_max = float(request.form["budget_max"])

    # >>>> TODO 8: Find the American [USA] Producers who had a box office collection of more than or equal to “X” with a budget less than or equal to “Y”. <<<<
    #              List the producer `name`, `movie name`, `box office collection` and `budget`.

    query = """ """

    with Database() as db:
        results = db.execute(query, (box_office_min, budget_max))
    return render_template("search_producers_results.html", results=results)


@queries_bp.route("/search_multiple_roles", methods=["POST"])
def search_multiple_roles():
    """
    Search for people who have multiple roles in movies with a rating above a given threshold.
    """
    rating_threshold = float(request.form["rating_threshold"])

    # >>>> TODO 9: List the people who have played multiple roles in a motion picture where the rating is more than “X”. <<<<
    #              List the person’s `name`, `motion picture name` and `count of number of roles` for that particular motion picture.

    query = """ """

    with Database() as db:
        results = db.execute(query, (rating_threshold,))
    return render_template("search_multiple_roles_results.html", results=results)


@queries_bp.route("/top_thriller_movies_boston", methods=["GET"])
def top_thriller_movies_boston():
    """Display the top 2 thriller movies in Boston based on rating."""

    # >>>> TODO 10: Find the top 2 rates thriller movies (genre is thriller) that were shot exclusively in Boston. <<<<
    #               This means that the movie cannot have any other shooting location.
    #               List the `movie names` and their `ratings`.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template("top_thriller_movies_boston.html", results=results)


@queries_bp.route("/search_movies_by_likes", methods=["POST"])
def search_movies_by_likes():
    """
    Search for movies that have received more than a specified number of likes,
    where the liking users are below a certain age.
    """
    min_likes = int(request.form["min_likes"])
    max_age = int(request.form["max_age"])

    # >>>> TODO 11: Find all the movies with more than “X” likes by users of age less than “Y”. <<<<
    #               List the movie names and the number of likes by those age-group users.

    query = """ """

    with Database() as db:
        results = db.execute(query, (max_age, min_likes))
    return render_template("search_movies_by_likes_results.html", results=results)


@queries_bp.route("/actors_marvel_warner", methods=["GET"])
def actors_marvel_warner():
    """
    List actors who have appeared in movies produced by both Marvel and Warner Bros.
    """

    # >>>> TODO 12: Find the actors who have played a role in both “Marvel” and “Warner Bros” productions. <<<<
    #               List the `actor names` and the corresponding `motion picture names`.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template("actors_marvel_warner.html", results=results)


@queries_bp.route("/movies_higher_than_comedy_avg", methods=["GET"])
def movies_higher_than_comedy_avg():
    """
    Display movies whose rating is higher than the average rating of comedy movies.
    """

    # >>>> TODO 13: Find the motion pictures that have a higher rating than the average rating of all comedy (genre) motion pictures. <<<<
    #               Show the names and ratings in descending order of ratings.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template("movies_higher_than_comedy_avg.html", results=results)


# @queries_bp.route("/top_5_movies_people_roles", methods=["GET"])
# def top_5_movies_people_roles():
#     """
#     Display the top 5 movies that involve the most people and roles.
#     """

#     # >>>> TODO 14: Find the top 5 movies with the highest number of people playing a role in that movie. <<<<
#     #               Show the `movie name`, `people count` and `role count` for the movies.

#     query = """ """

#     with Database() as db:
#         results = db.execute(query)
#     return render_template("top_5_movies_people_roles.html", results=results)


@queries_bp.route("/actors_with_common_birthday", methods=["GET"])
def actors_with_common_birthday():
    """
    Find pairs of actors who share the same birthday.
    """

    # >>>> TODO 14: Find actors who share the same birthday. <<<<
    #               List the actor names (actor 1, actor 2) and their common birthday.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template("actors_with_common_birthday.html", results=results)


@queries_bp.route("/top_production_by_genre", methods=["GET"])
def top_production_by_genre():
    """
    Display the top production companies for each genre based on the number of movies with above-average ratings.
    """
    # >>>> TODO 15: List the productions that have produced more than two movies in a given genre, where each movie has a rating higher than the average rating of that genre. <<<<
    #               List the `production company name`, `genre name` and the `count of movies` that meet the criteria, ordered by the count of movies in descending order.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template(
        "generic_results.html", results=results, title="Consistent Genre Leaders"
    )


@queries_bp.route("/versatile_talent", methods=["GET"])
def versatile_talent():
    """
    Display people who have won awards for acting, directing, and producing.
    """
    # >>>> TODO 16: Find the people who have won awards and performed as an actor, director, and producer. <<<<
    #               List the person’s `name` and `nationality`.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template(
        "generic_results.html",
        results=results,
        title="Versatile Talent (Triple Threats)",
    )


@queries_bp.route("/high_roi_movies", methods=["GET"])
def high_roi_movies():
    """
    Display the top 5 movies shot in the USA with the highest return on investment (ROI) compared to the average ROI of Marvel movies.
    """
    # >>>> TODO 17: Find the top 5 movies shot in the USA with the highest return on investment (ROI), where ROI is defined as box office collection divided by budget. <<<<
    #               Only include movies that have an ROI greater than the average ROI of all Marvel movies
    #               First column should be the movie name, second column should be country, and third column should be the ROI.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template(
        "generic_results.html", results=results, title="Highest ROI (vs Marvel Average)"
    )


# @queries_bp.route("/super_fans", methods=["POST"])
# def super_fans():
#     """
#     Find users who have liked all movies from a specific production company.
#     """
#     # >>>> TODO 19: Find the users who have liked all the movies produced by a specific production company. <<<<
#     #               List the user `name` and `email`.

#     production = request.form["production"]
#     query = """ """

#     with Database() as db:
#         results = db.execute(query, (production,))
#     return render_template(
#         "generic_results.html", results=results, title=f"Super-fans of {production}"
#     )


@queries_bp.route("/awarded_series_growth", methods=["GET"])
def awarded_series_growth():
    """
    Display TV series that have won awards and have a season count above the average, ordered by season count in descending order.
    """
    # >>>> TODO 18: Find the TV series that have won at least one award and have a season count above the average season count of all TV series. <<<<
    #               List the TV series `name`, `season count` and the `number of awards won`, ordered by season count in descending order.

    query = """ """

    with Database() as db:
        results = db.execute(query)
    return render_template(
        "generic_results.html",
        results=results,
        title="Award-Winning Long-Running Series",
    )
