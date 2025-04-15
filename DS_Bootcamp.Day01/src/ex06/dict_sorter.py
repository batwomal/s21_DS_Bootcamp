def get_countries_dict():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    return dict(list_of_tuples)


def main():
    countries_dict = get_countries_dict()
    sorted_dict = dict(sorted(countries_dict.items(), key=lambda item: (-int(item[1]), item[0])))

    for country in sorted_dict:
        print(country)

    return 0

if __name__ == '__main__':
    main()
