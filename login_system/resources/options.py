from dataclasses import dataclass


@dataclass
class Option:

    start_options: list
    dashboard_options: list
    admin_dashboard_options: list
    admin_options: list

    def _add_option(self, option, value):
        _options = getattr(self, option)
        _options.append(value)
    
    def _set_options(self):
        start = ["Login", "Sign Up"]
        dashboard = ["Home", "My Profile", "Logout"]
        admin_dashboard = ["Home", "My Profile", "Administrative", "Logout"]
        admin = []
        return {
            'start_options': start,
            'dashboard_options': dashboard,
            'admin_dashboard_options': admin_dashboard,
            'admin_options': admin
        }

    @classmethod
    def _init_option(cls):
        return cls(**cls._set_options(cls))
    
    def set_admin_options(self, options):
        self.admin_options = options
