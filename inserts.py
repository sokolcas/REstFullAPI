from datetime import date

from src import db
from src.database.models import Actor, Film


def populate_films():
    harry_potter = Film(
        title='Harry Potter',
        release_date=date(2001, 11, 4),
        description='bla bla bla',
        distributed_by='warner sisters',
        length=152,
        rating=7.6
    )
    american_pie = Film(
        title='American Pie',
        release_date=date(2002, 5, 18),
        description='sex sex alcohol',
        distributed_by='American Sex Education',
        length=120,
        rating=8.0
    )

    db.session.add(harry_potter)
    db.session.add(american_pie)

    tom_crouse = Actor(
        name='Tom Crouse',
        birthday=date(1953, 4, 15),
        is_active=True
    )
    emma_watson = Actor(
        name='Emma Watson',
        birthday=date(1998, 4, 15),
        is_active=True
    )
    harry_potter.actors = [tom_crouse, emma_watson]
    american_pie.actors = [tom_crouse, emma_watson]

    db.session.add(tom_crouse)
    db.session.add(emma_watson)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    populate_films()
    print('Successfully populated')
