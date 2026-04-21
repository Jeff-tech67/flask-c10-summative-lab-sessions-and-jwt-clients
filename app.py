from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from models import db, User, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key-that-is-longer-than-32-chars-for-security'  # Change this in production

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password is required'}, 400
        
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400
        

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username') 
        password = data.get('password')
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=str(user.id)) # This line 
        return {'access_token': access_token}, 200  

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

class Notes(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        notes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
        return {
            'notes': [note.to_dict() for note in notes.items],
            'total': notes.total,
            'pages': notes.pages,
            'current_page': notes.page
        }, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            return {'error': 'Title and content required'}, 400
        note = Note(title=title, content=content, user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return note.to_dict(), 201

class NoteById(Resource):
    @jwt_required()
    def get(self, id):
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return {'error': 'Note not found'}, 404
        return note.to_dict(), 200

    @jwt_required()
    def patch(self, id):
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return {'error': 'Note not found'}, 404
        data = request.get_json()
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        db.session.commit()
        return note.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return {'error': 'Note not found'}, 404
        db.session.delete(note)
        db.session.commit()
        return {'message': 'Note deleted'}, 200

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/me')
api.add_resource(Notes, '/notes')
api.add_resource(NoteById, '/notes/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)