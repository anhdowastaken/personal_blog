"""
appserver.py  
- Create an application instance and run the dev server
"""

from personal_blog_api.application import create_app
app = create_app()

@app.before_first_request
def create_blog_owner():
    # app.app_context().push()
    from personal_blog_api.config import BaseConfig
    from personal_blog_api.models import db
    from personal_blog_api.models import User
    config = BaseConfig()
    blog_owner = User.query.filter(User.email == config.BLOG_OWNER_EMAIL).filter(User.username == config.BLOG_OWNER_USERNAME).filter(User.role == 'admin').first()

    if blog_owner is None:
        blog_owner = User(config.BLOG_OWNER_EMAIL, config.BLOG_OWNER_USERNAME, config.BLOG_OWNER_PASSWORD)
        blog_owner.role = 'admin'
        db.session.add(blog_owner)
        db.session.commit()

if __name__ == '__main__':
    app.run()
