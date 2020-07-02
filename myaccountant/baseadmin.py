import csv
from django.contrib import admin
from django.http import HttpResponse


class BaseAdmin(admin.ModelAdmin):

    readonly_fields = ('created_by', 'updated_by', 'created_on', 'updated_on')

    csv_headers = []
    csv_columns = []
    csv_file_name = ""
    
    def export_as_csv(self, request, queryset):
        if self.csv_file_name:
            file_name = self.csv_file_name
        else:
            file_name = self.model.__name__
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename=%s.csv' % file_name
        writer = csv.writer(response)
        writer.writerow(self.csv_headers)
        data = queryset.values_list(*self.csv_columns)
        for d in data:
            writer.writerow(d)
        return response
    export_as_csv.short_description = "Export Selected"

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if 'export_as_csv' in actions and \
            len(self.csv_columns) <= 0 or len(self.csv_headers) <= 0:
            pass
            # raise AssertionError("please add csv_headers & csv_columns if adding export_as_csv as action")
        return actions
