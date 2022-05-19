from Tutorship.models import Tutorship

class TutorshipHistory:
    def __init__(self, tutorship_id, request_id, name, date_start, date_end):
        self.tutorship_id = tutorship_id
        self.request_id = request_id
        self.name = name
        self.date_start = date_start
        self.date_end = date_end 

class ListTutorshipHistory:
    def __init__(self, query):

        self.list = []
        for item in query:
            tutorship = Tutorship.objects.get(request_id = item.id)
            self.list.append(TutorshipHistory(tutorship.id, item.id, tutorship.name, item.date_start, item.date_end))
