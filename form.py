from utils import is_ascii, update_url_params, INPUT_TYPE_DICT, GET, POST
from urlparse import urljoin

class Form(object):
    """beautifulsoup form"""
    def __init__(self, url, document):
        self.document = document
        self.action = urljoin(url, self.document.get('action'))

    @property
    def method(self):
        return self.document.get('method') or GET

    @property
    def is_search_form(self):
        form_id = self.document.get('id') or ""
        form_class = self.document.get('class') or []
        return "search" in form_id.lower() or any("search" in c.lower() for c in form_class)

    def get_parameters(self, filter_type=None):
        for inpt in self.document.find_all('input'):
            name = str(inpt.get('name') or '')
            if not name:
                continue

            itype = inpt.get('type') or 'text'
            value = inpt.get('value')

            if value and is_ascii(value):
                value = value.encode('utf-8')

            if not value:
                value = INPUT_TYPE_DICT[itype]

            if not filter_type or filter_type and itype != filter_type:
                yield name, value

        for txt in self.document.find_all('textarea'):
            name = str(txt.get('name'))
            value = str(txt.text or INPUT_TYPE_DICT['text'])

            yield name, value

    def send(self, client, params, changed_action=None):
        if changed_action:
            action = changed_action
        else:
            action = self.action

        if self.method.lower() == POST.lower():
            res_page = client.post(self.action, data=params)
        else:
            url = update_url_params(self.action, params)
            res_page = client.get(url)

        return res_page