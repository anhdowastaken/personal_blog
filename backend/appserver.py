"""
appserver.py  
- Create an application instance and run the dev server
"""

if __name__ == '__main__':  
    from personal_blog_api.application import create_app
    app = create_app()
    app.run()
