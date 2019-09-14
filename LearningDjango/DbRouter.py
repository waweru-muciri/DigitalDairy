class DbRouter:
    """
    A router to control all database operations on models in this application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read  models go to event_company.
        """
        if model._meta.app_label == 'event_management':
            return 'event_company'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'event_management':
            return 'event_company'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the event_company app is involved.
        """
        if obj1._meta.app_label == 'event_management' or \
           obj2._meta.app_label == 'event_management':
           return True
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the event_management app only appears in the 'event_company'
        database.
        """
        if app_label == 'event_management':
            return db == 'event_company'
        return True
