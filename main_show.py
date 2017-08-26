import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to YearoneInvest")

class ShowHandler(tornado.web.RequestHandler):
    def get(self):
        file = self.get_argument("file", default=None, strip=False)
        if not file:
            print('no file param')
            return
        print('acquire file {}'.format(file))
        '''
        with open(file, 'r') as f:
            html = f.read()
        self.write(html)
        '''
        self.render(file)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/event/acquire", ShowHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8653)
    print('listening at port 8653')
    tornado.ioloop.IOLoop.current().start()

'''
import tornado.ioloop
import tornado.web

from show import Show

def make_app():
    return tornado.web.Application([
        (r"/event/acquire", Show),
    ])

acquire_app = make_app()
acquire_app.listen(8089)
tornado.ioloop.IOLoop.current().start()
'''

