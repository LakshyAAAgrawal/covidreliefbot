def join_entries(entries):
    entries_url = entries[0]

    for i in entries[1:]:
        entries_url += '%20OR%20{}'.format(str(i))
    return entries_url

def get_twitter_link(cities, resources):
    location_text, resources_text = '', ''
    if cities != [] :
        location_text = join_entries(cities)
    if resources != []:
        resources_text = join_entries(resources)

    return 'https://twitter.com/search?q=({})%20({})%20-%22needed%22%20-%22need%22%20-%22needs%22%20-%22required%22%20-%22require%22%20-%22requires%22%20-%22requirement%22%20-%22requirements%22&f=live'.format(location_text, resources_text)


print(get_twitter_link([], ['Plasma', 'oxygen']))