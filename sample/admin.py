from django.contrib import admin

from .models import Movement
from .models import MovementAnnex
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class MovementAnnexInline(admin.TabularInline):
    model = MovementAnnex
    extra = 1


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    search_fields = ('value', 'remark', 'tags__name', 'movements__remark',)
    list_display = ('id', 'created', 'value', 'remark',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
    inlines = (
        MovementAnnexInline,
    )


@admin.register(MovementAnnex)
class MovementAnnexAdmin(admin.ModelAdmin):
    search_fields = ('movement__remark', 'movement__value', 'remark',)
    list_display = ('id', 'movement', 'remark', 'content')
    list_filter = ('movement__tags',)
