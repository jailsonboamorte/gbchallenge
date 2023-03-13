class Flake8Exception(Exception):

    def __str__(self):
        return f'\n{self.args[0]}'
