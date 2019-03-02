


class Module(object):
    """Module base class"""

    def out(self, t):
        raise NotImplementedError

    def __call__(self, t):
        return self.out(t)

    # operators

    # TODO: handle number types
    # TODO: return instance of module instead of function

    def __add__(self, other):
        return lambda t: self(t) + other(t)

    def __sub__(self, other):
        return lambda t: self(t) - other(t)

    def __mul__(self, other):
        return lambda t: self(t) * other(t)

    def __truediv__(self, other):
        return lambda t: self(t) / other(t)
