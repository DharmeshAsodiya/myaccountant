from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    readonly_fields = ('created_by', 'updated_by', 'created_on', 'updated_on')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
