from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, world!"})


# TODO return an object containing the list and some metadata about the list instead of a list directly
@app.route("/shows/<int:show_id>/episodes", methods=["GET"])
def list_episodes(show_id):
    an_episode = {
        "episode_id": 123456,
        "show_id": show_id,
        "title": "the one where that one band plays live",
        "start_at": "2022-04-01...",
        "file_url": "https://s3.or.something...",
        "created_at": "2022-03-31...",
        "updated_at": "2022-03-31...",
        "description": "some text about the show"}

    return jsonify([an_episode])


@app.route("/episodes/<int:episode_id>", methods=["GET"])
def get_episode(episode_id):
    an_episode = {
        "episode_id": episode_id,
        "show_id": 1234,
        "title": "the one where that one band plays live",
        "start_at": "2022-04-01...",
        "file_url": "https://s3.or.something...",
        "created_at": "2022-03-31...",
        "updated_at": "2022-03-31...",
        "description": "some text about the show"}

    return jsonify(an_episode)


# TODO return an object containing the list and some metadata about the list instead of a list directly
@app.route("/djs/<int:dj_id>/shows", methods=["GET"])
def list_shows(dj_id):
    a_show = {
        "owner_ids": [123, 456],
        "name": "The name of the show",
        "created_at": "2022-03-31...",
        "updated_at": "2022-03-31...",
        "description": "some text about the show"}

    return jsonify([a_show])


@app.route("/djs/<int:dj_id>/profile", methods=["GET"])
def get_profile(dj_id):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        dj_data = {
            "name": "dj mcdjson",
            "email": "dj@gmail.com"}

        return jsonify(dj_data)



if __name__ == '__main__':
    import auth
    app.register_blueprint(auth.bp)

    app.run(debug=True)
