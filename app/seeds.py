from datetime import datetime

from app.extensions import db
from app.models import (
    Album,
    Authorization,
    Creator,
    Download,
    Genre,
    Label,
    ProfileCreator,
    ProfileUser,
    Review,
    Song,
    SongHasAlbum,
    SongHasCreator,
    Subscription,
    User,
)


def _get_or_create(model, filters, values=None):
    instance = model.query.filter_by(**filters).one_or_none()
    if instance:
        if values:
            for key, value in values.items():
                setattr(instance, key, value)
        return instance
    data = dict(filters)
    if values:
        data.update(values)
    instance = model(**data)
    db.session.add(instance)
    return instance


def _seed_subscriptions():
    data = [
        {"plan": "basic", "price": 0},
        {"plan": "plus", "price": 9},
        {"plan": "premium", "price": 15},
    ]
    records = {}
    for item in data:
        subscription = _get_or_create(Subscription, {"plan": item["plan"]}, {"price": item["price"]})
        records[item["plan"]] = subscription
    db.session.flush()
    return records


def _seed_authorizations():
    data = [
        {"key": "alice", "email": "alice@example.com", "password": "alicepass"},
        {"key": "bob", "email": "bob@example.com", "password": "bobpass"},
        {"key": "echo", "email": "echo@sonic.io", "password": "echopass"},
        {"key": "luna", "email": "luna@aurora.fm", "password": "lunapass"},
        {"key": "milo", "email": "milo@midnight.fm", "password": "milopass"},
    ]
    records = {}
    for item in data:
        authorization = _get_or_create(Authorization, {"email": item["email"]}, {"password": item["password"]})
        records[item["key"]] = authorization
    db.session.flush()
    return records


def _seed_profile_users():
    data = [
        {"key": "alice", "picture_link": "https://cdn.example.com/profiles/alice.jpg", "bio": "Curator of acoustic playlists."},
        {"key": "bob", "picture_link": "https://cdn.example.com/profiles/bob.jpg", "bio": "Collector of indie vinyl."},
        {"key": "echo", "picture_link": "https://cdn.example.com/profiles/echo.jpg", "bio": "Sound engineer turned artist."},
        {"key": "luna", "picture_link": "https://cdn.example.com/profiles/luna.jpg", "bio": "Synthwave producer and DJ."},
        {"key": "milo", "picture_link": "https://cdn.example.com/profiles/milo.jpg", "bio": "Lo-fi beat maker with jazz roots."},
    ]
    records = {}
    for item in data:
        profile = _get_or_create(ProfileUser, {"picture_link": item["picture_link"]}, {"bio": item["bio"]})
        records[item["key"]] = profile
    db.session.flush()
    return records


def _seed_users(authorizations, subscriptions, profiles):
    data = [
        {"key": "alice", "name": "Alice Harper", "authorization": "alice", "subscription": "basic"},
        {"key": "bob", "name": "Bob Rivera", "authorization": "bob", "subscription": "premium"},
        {"key": "echo", "name": "Echo Nova", "authorization": "echo", "subscription": "plus"},
        {"key": "luna", "name": "Luna Sky", "authorization": "luna", "subscription": "premium"},
        {"key": "milo", "name": "Milo Reed", "authorization": "milo", "subscription": "plus"},
    ]
    records = {}
    for item in data:
        authorization = authorizations[item["authorization"]]
        subscription = subscriptions[item["subscription"]]
        profile = profiles[item["key"]]
        user = User.query.filter_by(authorization_id=authorization.id).one_or_none()
        if user:
            user.name = item["name"]
            user.subscription_id = subscription.id
            user.profile_user_id = profile.id
        else:
            user = User(
                name=item["name"],
                authorization_id=authorization.id,
                subscription_id=subscription.id,
                profile_user_id=profile.id,
            )
            db.session.add(user)
        records[item["key"]] = user
    db.session.flush()
    return records


def _seed_labels():
    data = [
        {"key": "aurora", "name": "Aurora Collective"},
        {"key": "midnight", "name": "Midnight Echo"},
        {"key": "sonata", "name": "Sonata Studios"},
    ]
    records = {}
    for item in data:
        label = _get_or_create(Label, {"name": item["name"]}, {})
        records[item["key"]] = label
    db.session.flush()
    return records


def _seed_profile_creators(users):
    data = [
        {"key": "echo", "user": "echo", "picture_link": "https://cdn.example.com/creators/echo.jpg", "bio": "Mixing field recordings with modular synths."},
        {"key": "luna", "user": "luna", "picture_link": "https://cdn.example.com/creators/luna.jpg", "bio": "Exploring cosmic electronica."},
        {"key": "milo", "user": "milo", "picture_link": "https://cdn.example.com/creators/milo.jpg", "bio": "Chasing mellow beats and dusty samples."},
    ]
    records = {}
    for item in data:
        profile = ProfileCreator.query.filter_by(user_id=users[item["user"]].id).one_or_none()
        if profile:
            profile.picture_link = item["picture_link"]
            profile.bio = item["bio"]
        else:
            profile = ProfileCreator(
                user_id=users[item["user"]].id,
                picture_link=item["picture_link"],
                bio=item["bio"],
            )
            db.session.add(profile)
        records[item["key"]] = profile
    db.session.flush()
    return records


def _seed_creators(authorizations, labels, profile_creators):
    data = [
        {
            "key": "echo",
            "name": "Echo Nova",
            "authorization": "echo",
            "label": "aurora",
            "profile": "echo",
            "release_date": datetime(2022, 3, 18),
        },
        {
            "key": "luna",
            "name": "Luna Sky",
            "authorization": "luna",
            "label": "sonata",
            "profile": "luna",
            "release_date": datetime(2021, 11, 5),
        },
        {
            "key": "milo",
            "name": "Milo Reed",
            "authorization": "milo",
            "label": "midnight",
            "profile": "milo",
            "release_date": datetime(2020, 8, 27),
        },
    ]
    records = {}
    for item in data:
        creator = Creator.query.filter_by(authorization_id=authorizations[item["authorization"]].id).one_or_none()
        values = {
            "name": item["name"],
            "release_date": item["release_date"],
            "label_id": labels[item["label"]].id,
            "profile_creator_id": profile_creators[item["profile"]].id,
        }
        if creator:
            for key, value in values.items():
                setattr(creator, key, value)
        else:
            creator = Creator(
                authorization_id=authorizations[item["authorization"]].id,
                **values,
            )
            db.session.add(creator)
        records[item["key"]] = creator
    db.session.flush()
    return records


def _seed_albums(creators):
    data = [
        {"key": "echo_echoes", "name": "Echoes in Transit", "release_date": datetime(2023, 5, 12), "creator": "echo"},
        {"key": "luna_orbits", "name": "Orbits", "release_date": datetime(2022, 7, 29), "creator": "luna"},
        {"key": "milo_afterglow", "name": "Afterglow", "release_date": datetime(2021, 9, 17), "creator": "milo"},
    ]
    records = {}
    for item in data:
        creator = creators[item["creator"]]
        album = Album.query.filter_by(name=item["name"], creator_id=creator.id).one_or_none()
        if album:
            album.release_date = item["release_date"]
        else:
            album = Album(
                name=item["name"],
                release_date=item["release_date"],
                creator_id=creator.id,
            )
            db.session.add(album)
        records[item["key"]] = album
    db.session.flush()
    return records


def _seed_genres():
    names = ["Ambient", "Synthwave", "Lo-fi", "Indie", "Classical"]
    records = {}
    for name in names:
        genre = _get_or_create(Genre, {"name": name}, {})
        records[name] = genre
    db.session.flush()
    return records


def _seed_songs(genres):
    data = [
        {"key": "horizon", "name": "Neon Horizon", "genre": "Synthwave", "link": "https://cdn.example.com/audio/neon-horizon.mp3", "download_count": 1280},
        {"key": "dawn", "name": "Dawn Patterns", "genre": "Ambient", "link": "https://cdn.example.com/audio/dawn-patterns.mp3", "download_count": 930},
        {"key": "glow", "name": "City Glow", "genre": "Indie", "link": "https://cdn.example.com/audio/city-glow.mp3", "download_count": 740},
        {"key": "pulse", "name": "Midnight Pulse", "genre": "Synthwave", "link": "https://cdn.example.com/audio/midnight-pulse.mp3", "download_count": 1620},
        {"key": "breeze", "name": "Lo-fi Breeze", "genre": "Lo-fi", "link": "https://cdn.example.com/audio/lofi-breeze.mp3", "download_count": 890},
    ]
    records = {}
    for item in data:
        genre = genres[item["genre"]]
        song = Song.query.filter_by(name=item["name"]).one_or_none()
        if song:
            song.genre_name = genre.name
            song.link = item["link"]
            song.download_count = item["download_count"]
        else:
            song = Song(
                name=item["name"],
                genre_name=genre.name,
                link=item["link"],
                download_count=item["download_count"],
            )
            db.session.add(song)
        records[item["key"]] = song
    db.session.flush()
    return records


def _seed_song_creators(songs, creators):
    pairs = [
        ("horizon", "luna"),
        ("dawn", "echo"),
        ("glow", "milo"),
        ("pulse", "luna"),
        ("breeze", "milo"),
    ]
    for song_key, creator_key in pairs:
        song = songs[song_key]
        creator = creators[creator_key]
        link = SongHasCreator.query.filter_by(song_id=song.id, creator_id=creator.id).one_or_none()
        if not link:
            db.session.add(SongHasCreator(song_id=song.id, creator_id=creator.id))
    db.session.flush()


def _seed_song_albums(songs, albums):
    pairs = [
        ("horizon", "luna_orbits"),
        ("dawn", "echo_echoes"),
        ("pulse", "luna_orbits"),
        ("breeze", "milo_afterglow"),
        ("glow", "milo_afterglow"),
    ]
    for song_key, album_key in pairs:
        song = songs[song_key]
        album = albums[album_key]
        link = SongHasAlbum.query.filter_by(song_id=song.id, album_id=album.id).one_or_none()
        if not link:
            db.session.add(SongHasAlbum(song_id=song.id, album_id=album.id))
    db.session.flush()


def _seed_downloads(users, songs):
    pairs = [
        ("alice", "horizon"),
        ("alice", "dawn"),
        ("bob", "pulse"),
        ("bob", "glow"),
        ("echo", "dawn"),
        ("luna", "pulse"),
        ("milo", "breeze"),
    ]
    for user_key, song_key in pairs:
        user = users[user_key]
        song = songs[song_key]
        download = Download.query.filter_by(user_id=user.id, song_id=song.id).one_or_none()
        if not download:
            db.session.add(Download(user_id=user.id, song_id=song.id))
    db.session.flush()


def _seed_reviews(users, songs):
    data = [
        {"user": "alice", "song": "horizon", "content": "Vibrant synth layers and a perfect driving tempo.", "rating": 5},
        {"user": "bob", "song": "glow", "content": "Feels like walking through a city at night.", "rating": 4},
        {"user": "echo", "song": "dawn", "content": "Soothing textures that evolve effortlessly.", "rating": 5},
        {"user": "luna", "song": "pulse", "content": "A dancefloor staple with atmospheric flourishes.", "rating": 4},
        {"user": "milo", "song": "breeze", "content": "Dusty drums and mellow keys in harmony.", "rating": 5},
    ]
    for item in data:
        user = users[item["user"]]
        song = songs[item["song"]]
        review = Review.query.filter_by(user_id=user.id, song_id=song.id).one_or_none()
        if review:
            review.content = item["content"]
            review.rating = item["rating"]
        else:
            review = Review(
                user_id=user.id,
                song_id=song.id,
                content=item["content"],
                rating=item["rating"],
            )
            db.session.add(review)
    db.session.flush()


def seed_database():
    subscriptions = _seed_subscriptions()
    authorizations = _seed_authorizations()
    profiles = _seed_profile_users()
    users = _seed_users(authorizations, subscriptions, profiles)
    labels = _seed_labels()
    profile_creators = _seed_profile_creators(users)
    creators = _seed_creators(authorizations, labels, profile_creators)
    albums = _seed_albums(creators)
    genres = _seed_genres()
    songs = _seed_songs(genres)
    _seed_song_creators(songs, creators)
    _seed_song_albums(songs, albums)
    _seed_downloads(users, songs)
    _seed_reviews(users, songs)
    db.session.commit()