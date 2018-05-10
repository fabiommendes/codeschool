
# Local settings file that can be personalized by each developer.

from codeschool.config.settings import CodeschoolConf


class LocalConf(CodeschoolConf):
    pass
    
LocalConf.save_settings()
