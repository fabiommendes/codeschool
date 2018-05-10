from boogie.configurations import TemplatesConf


class BaseConf(TemplatesConf):
    DJANGO_TEMPLATES_DIRS = property(
        lambda self: [self.CONFIG_DIR / 'templates/django'])
    JINJA_TEMPLATES_DIRS = property(
        lambda self: [self.CONFIG_DIR / 'templates/jinja2'])

    def finalize(self, settings):
        settings['TEMPLATES'][1]['OPTIONS'].update(
            environment='codeschool.config.jinja2.environment',
        )
        return settings
