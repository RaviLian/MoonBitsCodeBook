class Document():
    # 在类中使用self.WELCOME_STR ，
    # 或者在类外使用Entity.WELCOME_STR
    WELCOME_STR = 'Welcome! The context for this book is {}.'

    def __init__(self, title, author, context):
        print('init function called')
        self.title = title
        self.author = author
        self.__context = context

    # 类函数
    # 类函数的第一个参数一般为 cls，表示必须传一个类进来。
    # 类函数最常用的功能是实现不同的 init 构造函数，
    # 比如使用 create_empty_book 类函数，来创造新的书籍对象，其 context 一定为 'nothing'。
    @classmethod
    def create_empty_book(cls, title, author):
        return cls(title=title, author=author, context='nothing')

    # 成员函数
    def get_context_length(self):
        return len(self.__context)

    # 静态函数
    # 一般而言，静态函数可以用来做一些简单独立的任务，既方便测试，也能优化代码结构
    @staticmethod
    def get_welcome(context):
        return Document.WELCOME_STR.format(context)


empty_book = Document.create_empty_book('What Every Man Thinks About Apart from Sex', 'Professor Sheridan Simove')

print(empty_book.get_context_length())
print(empty_book.get_welcome('indeed nothing'))