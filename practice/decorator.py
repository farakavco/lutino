

def plus_star_basic(count):
    def decorator(func):

        def wrapper(value):
            return '%s/%s/%s' % (value, func(value), '*' * count)

        return wrapper

    return decorator


@plus_star_basic(10)
def string_(value):
    return 'function-%s' % value


####################################################


def plus_star(*args, **kwargs):
    # Set default value for count
    if len(kwargs) == 1:
        star_count = kwargs['count']
    elif len(args) == 0 or (len(args) == 1 and callable(args[0])):
        star_count = 1
    else:
        star_count = args[0]

    def decorator(func):

        def wrapper(*a, **kw):
            return '%s/%s' % (func(*a, **kw), '*' * star_count)
        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator


@plus_star()
def string1_(value):
    return value


@plus_star
def string2_(value):
    return value


@plus_star(20)
def string3_(value):
    return value


@plus_star(count=50)
def string4_(value):
    return value


# if __name__ == '__main__':
#     print(string_('test'))
#     print(string1_('test1'))
#     print(string2_('test2'))
#     print(string3_('test3'))
#     print(string4_('test4'))


class P(object):
    def __init__(self,x):
        self.x = x

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x


if __name__ == '__main__':
    print(string_('test'))
