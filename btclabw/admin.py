from django.contrib import admin

# Register your models here.
from .models import Exchange, User, UserExchange, Membership, DCAStrategy, DIPStrategy, UserOrder

admin.site.register(Exchange)
admin.site.register(User)
admin.site.register(UserExchange)
admin.site.register(Membership)
admin.site.register(DCAStrategy)
admin.site.register(DIPStrategy)
admin.site.register(UserOrder)
