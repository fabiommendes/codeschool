from codeschool.api import router
from . import views

router.register(r'users', views.UserViewSet,base_name="users")
router.register(r'profile', views.ProfileViewSet)
