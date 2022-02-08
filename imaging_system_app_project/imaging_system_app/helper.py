# helper functions for searching and filtering entries

class FieldLookup():
    # obj: Databse object
    # field: field name of the object as string
        # foreign key: foreign_key__field_name
    
    # search entries that starts with search_string
    def starts_with(obj, field, search_string, max_results=0):
        obj_list = []
        if search_string:
            filter = field + '__istartswith'
            obj_list = obj.objects.filter(**{ filter: search_string })
        if max_results > 0:
            if len(obj_list) > max_results:
                obj_list = obj_list[:max_results]
        return obj_list
        
    # search entries that contains search_string
    def contains(obj, field, search_string, max_results=0):
        obj_list = []
        if search_string:
            filter = field + '__icontains'
            obj_list = obj.objects.filter(**{ filter: search_string })
        if max_results > 0:
            if len(obj_list) > max_results:
                obj_list = obj_list[:max_results]
        return obj_list
        
    # search entries that is within start_date and end_date
    # uses datetime.date format: datetime.date(yyyy, m , d)
    def daterange(obj, field, start_date, end_date, max_results=0):
        obj_list = []
        if start_date and end_date:
            filter = field + '__range'
            obj_list = obj.objects.filter(**{ filter: (start_date, end_date) })
        if max_results > 0:
            if len(obj_list) > max_results:
                obj_list = obj_list[:max_results]
        return obj_list