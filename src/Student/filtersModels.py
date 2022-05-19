class TypeSearch:
    def __init__(self, name, selected, url):
        self.name = name
        self.selected = selected
        self.url = url 


class ListTypeSearch:
    def __init__(self, listSelected, listUrls):
        self.list = [TypeSearch("Curso", listSelected[0], listUrls[0]), TypeSearch("Universidad", listSelected[1], listUrls[1]), 
            TypeSearch("Tutor", listSelected[2], listUrls[2]), TypeSearch("Recursos públicos", listSelected[3], listUrls[3]), 
            TypeSearch("Sesiones públicas", listSelected[4], listUrls[4])]


class TypeFilter:
    def __init__(self, name, selected):
        self.name = name
        self.selected = selected


class TypeScore:
    def __init__(self, name, selected, url):
        self.name = name
        self.selected = selected
        self.url = url


class ListFilter:
    def __init__(self, allObjects, listValuesFilter = None):
        self.list = []
        for filterObject in allObjects:
            if hasattr(filterObject, 'name'):
                if listValuesFilter and filterObject.name in listValuesFilter:
                    self.list.append(TypeFilter(filterObject.name, 1))
                else:
                    self.list.append(TypeFilter(filterObject.name, 0))
            elif hasattr(filterObject, 'region_name'):
                if listValuesFilter and filterObject.region_name in listValuesFilter:
                    self.list.append(TypeFilter(filterObject.region_name, 1))
                else:
                    self.list.append(TypeFilter(filterObject.region_name, 0))


class ListScore:
    def __init__(self, listValuesFilter = None):
        score = ["1 estrella", "2 estrellas", "3 estrellas", "4 estrellas", "5 estrellas"]
        self.list = []
        for stars in range(len(score)):
            if listValuesFilter and str(stars+1) in listValuesFilter:
                self.list.append(TypeScore(score[stars], 1, stars+1))
            else:
                self.list.append(TypeScore(score[stars], 0, stars+1))


class RequestNode:
    def __init__(self, request, scored):
        self.request = request
        self.scored = scored


class ListRequestNode:
    def __init__(self, query, scored):
        self.list = []
        for request in query:
            if request.id in scored:
                self.list.append(RequestNode(request, 1))
            else:
                self.list.append(RequestNode(request, 0))