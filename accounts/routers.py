class SharedAuthRouter:
    """
    A router to control all database operations on users and groups
    """
    route_app_labels = {
        'accounts': 'accounts',
        'auth': 'auth',
        'admin': 'admin',
        'contenttypes': 'contenttypes',
        'sessions': 'sessions',
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'shared_auth'
        return 'default'

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'shared_auth'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow two models to involve a relation
        :param obj1:
        :param obj2:
        :param hints:
        :return:
        """
        if (
                obj1._meta.app_label in self.route_app_labels and
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'shared_auth'
        return db == 'default'