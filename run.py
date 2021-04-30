from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"video(name={name}, views={views}, likes={likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of video is required', required=True)
video_put_args.add_argument('likes', type=int, help='Number of likes is required', required=True)
video_put_args.add_argument('views', type=int, help='views of video is required', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of video is required')
video_update_args.add_argument('likes', type=int, help='Number of likes is required')
video_update_args.add_argument('views', type=int, help='views of video is required')


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.get(video_id)
        if video is None:
            abort(404, message="video does not exist")
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        if VideoModel.query.get(video_id) is not None:
            abort(409, message="video already exists")
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        video = VideoModel.query.get(video_id)
        if video is None:
            abort(404, message="video does not exist")
        args = video_update_args.parse_args()

        if args['name']:
            video.name = args['name']
        if args['views']:
            video.views = args['views']
        if args['likes']:
            video.likes = args['likes']

        db.session.commit()
        return video, 201

    def delete(self, video_id):
        del video_id
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)