"""
appserver.py  
- Create an application instance and run the dev server
"""

if __name__ == '__main__':  
    from personal_blog_api.application import create_app
    app = create_app()

    app.app_context().push()
    from personal_blog_api.models import db
    from personal_blog_api.models import User
    admin = User.query.filter(User.username == 'admin').filter(User.role == 'admin').first()
    if admin is None:
        admin = User('admin', '123456')
        admin.role = 'admin'
        db.session.add(admin)
        db.session.commit()

    user = User.query.filter(User.username == 'dq2nd').filter(User.role == 'user').first()
    if user is None:
        user = User('dq2nd', '123456')
        user.role = 'user'
        db.session.add(user)
        db.session.commit()

    app.run()
