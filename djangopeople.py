from BeautifulSoup import BeautifulSoup
import requests


def parse_djangopeople_profile(user):
    html = requests.get('https://people.djangoproject.com/%s/' % user)
    profile = BeautifulSoup(html.content).find('div', 'finding')

    data = {
        'email': profile.find('a', 'email').text
    }

    possible_finding_values = (
        ('blog', 'blog:'),
        ('google_talk', 'GTalk:'),
        ('irc_nick', '#django IRC:')
    )

    for key, label in possible_finding_values:
        data[key] = get_finding_div_value(profile, label)

    possible_services = (
            ('facebook','facebook'),
            ('github','github'),
            ('google_plus','googleplus'),
            ('linkedin', 'linkedin'),
            ('stack_overflow','stackoverflow'),
            ('twitter','twitter')
    )

    for key, label in possible_services:
        data[key] = get_service_value(profile, label)

    return data

def get_finding_div_value(profile, label):
    try:
        return profile.find('strong', text=label).parent.parent.find(['a','span']).text
    except AttributeError:
        return None

def get_service_value(profile, label):
    try:
        return profile.find('ul', 'services').find('a', label)['href']
    except AttributeError:
        return None

if __name__ == '__main__':
    print repr(parse_djangopeople_profile('lyndsysimon'))