from models import db, User, Note

def seed_users():
    usernames = ['alice', 'bob', 'charlie', 'diana', 'eve']
    for username in usernames:
        user = User(username=username)
        user.set_password('password')
        db.session.add(user)
    db.session.commit()

def seed_notes():
    users = User.query.all()
    titles = [
        'Meeting Notes', 'Project Ideas', 'Shopping List', 
        'Book Recommendations', 'Travel Plans', 'Recipe Ideas',
        'Workout Plan',
    ]
    contents = [
        'This is a note about my meeting today.',
        'Here are some ideas for the new project.',
        'Need to buy groceries and household items.',
        'Books I want to read this year.',
        'Planning a trip to the mountains.',
        'New recipes to try this weekend.',
        'My fitness goals for this month.',]
    
    for user in users:
        for i in range(7): 
            note = Note(
                title=titles[i % len(titles)],
                content=contents[i % len(contents)],
                user_id=user.id
            )
            db.session.add(note)
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_users()
        seed_notes()
        print("Database seeded successfully!")