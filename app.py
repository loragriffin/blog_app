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

        self.render_template("post.html", {'post': post, 'posts': posts})


class AuthorHandler(TemplateHandler):
    def get(self, author):
        post = Author.select().where(Author.id == author).get()

        # query to pull blog entry where slug from input matches slug of entry
        authors = Author.select().order_by(Author.name.desc())

        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())

        # query to list all blog entries by created field
        # authors = BlogPost.select().order_by(BlogPost.created.desc())

        self.render_template("author.html", {'authors': authors, 'posts': posts, 'post': post})


class CommentHandler(TemplateHandler):
    def post(self, slug):
        comment = self.get_body_argument('comment')

        # query to pull blog entry where slug from input matches slug of entry
        post = BlogPost.select()\
            .where(BlogPost.slug == slug).get()

        # query to list all blog entries by created field
        posts = BlogPost.select().order_by(BlogPost.created.desc())

        # need to figure out code to save comment to database
        post.save()

        self.render_template("post.html", {'post': post, 'posts': posts,
                                           'comment': comment})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/page/(.*)", PageHandler),
        (r"/post/(.*)/comment", CommentHandler),
        (r"/post/(.*)", PostHandler),
        (r"/author/(.*)", AuthorHandler),
        (r"/static/(.*)",
            tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(int(os.environ.get('PORT', '8080')),
               print('Server started on localhost: ' + str(8080)))
    tornado.ioloop.IOLoop.current().start()
