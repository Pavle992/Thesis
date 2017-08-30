import facebook

token = 'EAAEvqXBRTZBgBAFF9V0KBONpxLmQYZBp2bIWmFxZBSuGTMr2GVxns6IfwyLDFeoZBk0a1sYhu7m77PmFQ60ZCdDWvWMIKh6QW9WYVPrftXkb0RcOIbzNdlsTbH6o2qOxR9rcJZABZCBgIpcDXPAaMtwHhaD38xTfrypFAHZC3zAN6j8SrqLw0KUol9DYEMjZBi7hNTUJk7YWZAogZDZD'

graph = facebook.GraphAPI(token)

ids = ['231541427020961', '353020448134882']

ids_string = ','.join(x for x in ids)

people = graph.request('/?ids='+ids_string+'&fields=birthday,about,business,emails,description,genre,location,season,category,founded')

print(people)