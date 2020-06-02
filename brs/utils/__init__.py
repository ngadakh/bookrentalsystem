# Utility module for Book & Customer module contains base Blueprint class

from flask import Blueprint


class BRSModule(Blueprint):
    """
    This is base blueprint class for books and customer modules
    """
    def __init__(self, name, import_name, **kwargs):
        kwargs.setdefault('template_folder', 'templates')
        kwargs.setdefault('static_folder', 'static')
        self.submodules = []

        super(BRSModule, self).__init__(name, import_name, **kwargs)

    def register(self, app, options, first_registration=False):
        if first_registration:
            self.submodules = list(app.find_submodules(self.import_name))

        super(BRSModule, self).register(app, options, first_registration)

        for module in self.submodules:
            if first_registration:
                module.parentmodules.append(self)
            app.register_blueprint(module)
            app.register_logout_hook(module)
