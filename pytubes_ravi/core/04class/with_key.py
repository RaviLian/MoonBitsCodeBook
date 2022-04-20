"""
上下文管理器协议
"""

class Movie:
    def __init__(self, name):
        self.name = name
        self.on = True

    def __enter__(self):
        print("open a movie..")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("close..")

    def watch(self):
        print("watching {} ...".format(self.name))

    def switch(self):
        self.on = not self.on
        print("current status: {}".format(self.on))

    def __repr__(self):
        return self.name

if __name__ == '__main__':
    with Movie("Spider Man II") as movie:
        print(movie)
        movie.watch()
        movie.switch()
        movie.switch()
    print("end")