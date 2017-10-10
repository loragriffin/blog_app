import os
import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
    Environment, PackageLoader, select_autoescape

from models import BlogPost, Author

ENV = Environment(
    loader=PackageLoader('blog', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class TemplateHandler(tornado.web.RequestHandler):
    def render_template(self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))


class MainHandler(TemplateHandler):
    def get(self):
        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())
        self.render_template("home.html", {'posts': posts})


class PageHandler(TemplateHandler):
    def get(self, page):
        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())
        self.render_template(page, {'posts': posts})


class PostHandler(TemplateHandler):
    def get(self, slug):
        # query to pull blog entry where slug from input matches slug of entry
        post = BlogPost.select().where(BlogPost.slug == slug).get()

        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())

        # attempting to query to get author information
        # author = Author.select().where(Author.id == post.author_id).get()

        self.render_template("post.html", {'post': post, 'posts': posts,
                                           })


class CommentHandler(TemplateHandler):
    def post(self, slug):
        comment = self.get_body_argument('comment')

        # query to pull blog entry where slug from input matches slug of entry
        post = BlogPost.select()\
            .where(BlogPost.slug == slug).get()

        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())

        # Save Comment Here

        self.render_template("post.html", {'post': post, 'posts': posts,
                                           'comment': comment})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/page/(.*)", PageHandler),
        (r"/post/(.*)/comment", CommentHandler),
        (r"/post/(.*)", PostHandler),
        (r"/static/(.*)",
            tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')),
               print('Server started on localhost: ' + str(8080)))
    tornado.ioloop.IOLoop.current().start()
