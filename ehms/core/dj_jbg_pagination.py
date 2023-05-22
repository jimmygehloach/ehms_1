from django.core.paginator import Paginator


class PageMe:
    """
    @author Jimmy Gehloach

    setup pagination in the Django View
    """
    __user_request = None
    __user_modal_obj = None
    __user_pp_limit = None

    __final_modal_obj = None
    __is_paginated = False
    __paginator = None
    __page_obj = None

    def __init__(self, request, modal_obj, pp_limit=None):
        self.__user_request = request
        self.__user_modal_obj = modal_obj
        self.__user_pp_limit = pp_limit

    def __default_sort(self):
        if self.__user_request.GET.get('sort', '') not in ['asc', 'desc']:
            return 'desc'

    def __final_sort(self):
        return self.__default_sort()

    def __set_pp_limit(self):
        if not self.__user_pp_limit:
            self.__user_pp_limit = 30

    def __final_modal_object(self):
        s = self.__final_sort()
        if s == 'asc':
            self.__final_modal_obj = self.__user_modal_obj.order_by('created')
        elif s == 'desc':
            self.__final_modal_obj = self.__user_modal_obj.order_by('-created')

    def __paginator_object(self):
        self.__set_pp_limit()
        self.__paginator = Paginator(self.__final_modal_obj, self.__user_pp_limit)
        page_number = self.__user_request.GET.get('page', 1)
        self.__page_obj = self.__paginator.get_page(page_number)

        if self.__paginator.count > self.__user_pp_limit:
            self.__is_paginated = True

    def do(self):
        self.__final_modal_object()
        self.__paginator_object()

        return {
            'is_paginated': self.__is_paginated,
            'paginator_count': self.__paginator.count,
            'page_obj': self.__page_obj
        }
