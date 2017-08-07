import datetime

class EasterDate(object):
    def __init__(self, year):
        self.year = year

    def c(self):
        return int(self.year / 100)

    def n(self):
        return int(self.year - 19 * (self.year / 19))

    def k(self):
        return int((self.c() - 17) / 25)

    def i(self):
        i = self.c() - self.c() / 4 - ( self.c() - self.k() ) / 3 + 19 * self.n() + 15
        i = i - 30 * ( i / 30 )
        return int(i - ( i / 28 ) * ( 1 - ( i / 28 ) * ( 29 / ( i + 1 ) )* ( ( 21 - self.n() ) / 11 ) ))

    def j(self):
        j = self.year + self.year / 4 + self.i() + 2 - self.c() + self.c() / 4
        return int(j - 7 * ( j / 7 ))

    def l(self):
        return int(self.i() - self.j())

    @property
    def month(self):
        return int(3 + ( self.l() + 40 ) / 44)

    @property
    def day(self):
        return int(self.l() + 28 - 31 * ( self.month / 4 ))

    def __str__(self):
        a = datetime.date(year=self.year, month=self.month, day=self.day)
        return a.strftime("%A, %B %d, %Y")

if __name__ == "__main__":
    import sys
    try:
        year = sys.argv[1]
    except:
        sys.exit(0)
    try:
        year = int(year)
        print EasterDate(year)
    except:
        print "%r is not an integer, please Pass an INT!" % year
        raise
