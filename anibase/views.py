from flask import Blueprint, render_template, request
from flask import abort
from flask import current_app

from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Anime, Genre, Studio, AnimeGenre
from .model import engine


views = Blueprint('views', __name__, url_prefix='/')


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/anime')
def anime():
    with Session(engine) as session:
        page = request.args.get('page', 1, type=int)
        offset = page - 1
        per_page = current_app.config['PER_PAGE']
        pagination = session.query(Anime).order_by(Anime.members.desc()) \
                                          .slice(offset * per_page, offset*per_page + per_page)
    return render_template('anime_index.html', anime_titles=pagination, page=page)


@views.route('/anime/<int:mal_id>')
def anime_by_id(mal_id):
    genres = []
    with Session(engine) as session:
        try:
            anime_title = session.get(Anime, mal_id)
            anime_genres = session.execute(select(AnimeGenre).where(AnimeGenre.id_anime == mal_id))
            for ag in anime_genres.scalars():
                genres.append(session.get(Genre, ag.id_genre))
        except Exception as ex:
            print(ex)
            abort(404)

    return render_template('anime_id.html', anime=anime_title, genres=genres)


@views.route('/anime/year/<int:year_val>')
def anime_by_year(year_val):
    with Session(engine) as session:
        anime_titles = session.query(Anime).filter(Anime.year == year_val)
        anime_titles = sorted(anime_titles, key=lambda a: 0 if not a.score else a.score, reverse=True)
    return render_template('anime_year.html', titles=anime_titles, year=year_val)


@views.route('/studios')
def studios():
    with Session(engine) as session:
        page = request.args.get('page', 1, type=int)
        offset = page - 1
        per_page = current_app.config['PER_PAGE']
        pagination = session.query(Studio).slice(offset * per_page,
                                                 offset*per_page + per_page)
    return render_template('studios.html', studios=pagination, page=page)
