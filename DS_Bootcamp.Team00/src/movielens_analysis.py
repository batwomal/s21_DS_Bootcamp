#!/usr/bin/env python3

import os
import re
import sys
import json
import pytest
import requests
import datetime
import functools
import collections
from  bs4 import BeautifulSoup

class Links():
    """
    Анализ данных из links.csv
    """
    def __init__(self, f_path: str='') -> None:
        def _set_filepath_(self, f_path) -> None:
            if not (isinstance(f_path, (str))):
                raise AttributeError(f"ValueError: Invalid file path: {type(f_path)}")
            if not f_path:
                raise TypeError("TypeError: read_csv() missing 1 required positional argument: 'filepath'")
            if not os.path.exists(f_path):
                raise FileNotFoundError(f"FileNotFoundError: [Errno 2] No such file or directory: '{f_path}'")

            self.filepath = f_path
                
        def _set_links_file_data(self) -> None:
            file = open(self.filepath, 'r', encoding='UTF-8')
            data = file.read()

            if (data == ''):
                raise ValueError (2, "'File is empty'")
            if (' ' in data) or \
                (len(data.split('\n')[0].split(',')) != 3) or \
                not (''.join(data.split('\n')[1:]).replace(',', '').isnumeric()):
                    raise ValueError (3, "'The file structure is broken'")    
            
            file.seek(0)

            data = file.readlines()
            if (data[0].split(',')[0].isalpha()):
                data = data[1:]

            self.links_file_data = {
                int(nest_list[0]) : nest_list[1:]
                for string in data
                for nest_list in [string.replace('\n', '').split(',')]
                }
            
            file.close()

        try:
            self.base_url_imdb:     str     = 'https://www.imdb.com/'
            self.headers:           dict    = {'User-Agent': ''}
            self.filepath:          str     = ''
            self.links_file_data:   dict    = {}
            self.imdb_content:      list    = []
            _set_filepath_(self, f_path)
            _set_links_file_data(self)

        except (
            AttributeError, TypeError, FileNotFoundError,
            IsADirectoryError, ValueError,
            ) as er_msg:
                sys.stderr.write(f"{er_msg}\n")
                
                if (len(sys.argv) <= 2):
                    return
                raise er_msg

    def get_imdb(
            self, list_of_movies=[],
            list_of_fields=['movieId', 'Gross worldwide', 'imdbId', 'Title',
                            'Runtime', 'Director', 'Budget', 'URL']
            ) -> list:
        """
        Метод возвращает список списков [movieId, field1, field2, field3, ...]
        для списка фильмов, заданного в качестве аргумента (movieId).
        Например, [movieId, Режиссер, Бюджет, Совокупный мировой доход, Время показа].
        Значения следует проанализировать с веб-страниц фильмов IMDB.
        Отсортируйте его по идентификатору фильма по убыванию.
        """
        def _get_field_data(json_soup, field) -> str:
            def get_value(json_dict, keys_list) -> str:
                value = None
                for key in keys_list:
                    if (value := json_dict.get(key)):
                        json_dict = value
                return value

            return {
                'imdbId':   get_value(json_soup, ['id']),
                'Title':    get_value(json_soup, ['originalTitleText', 'text']),
                'Runtime':  get_value(json_soup, ['runtime', 'seconds']),
                'Gross worldwide': get_value(json_soup,
                                        ['worldwideGross', 'total', 'amount']),
                'Budget':   get_value(json_soup,
                                     ['productionBudget', 'budget', 'amount']),
                'Director': [director['name']['nameText']['text'] 
                        if (director) else None
                        for director in (json_soup['directors'][0]['credits']
                                     if (json_soup['directors']) else [None])
                    ],
                'URL':   self.base_url_imdb + 'title/' + get_value(json_soup, ['id']),
                }.get(field)

        if not ('movieId' in list_of_fields):
            list_of_fields = ['movieId'] + list_of_fields

        if (os.path.exists('../datasets/ml-latest-small/imdb_content.txt')) and \
            not list_of_movies:
            with open('../datasets/ml-latest-small/imdb_content.txt', 'r', encoding='UTF-8') as content:
                self.imdb_content = eval(content.read())[:]

        else:
            self.imdb_content = []
            for movieid in list_of_movies:

                if (imdbid := self.links_file_data.get(movieid)):
                    link = self.base_url_imdb + f"title/tt{imdbid[0]}/"
                    response = requests.Response()
                    try:
                        response = requests.get(link, headers=self.headers)
                    except Exception as err:
                        sys.stderr.write(f"HTTP error: {err}\n")
                        if (len(sys.argv) == 2):
                            return
                        break


                else:
                    sys.stderr.write(
                        f"'Get movieid {movieid} - request failed'\n"
                            )
                    continue

                if (response.status_code == 200):
                    imdbid      = [movieid]
                    json_soup   = json.loads(
                            BeautifulSoup(response.text, 'lxml').find(
                                    ['script'], {'type': 'application/json'}
                                    ).text)['props']['pageProps']['mainColumnData']
                    
                    imdbid.extend([_get_field_data(json_soup, elem)
                                    for elem in list_of_fields[1:]
                                    ])
                    self.imdb_content.append(imdbid)
    
                else:
                    sys.stderr.write(
                        f"'Movie with tmdbid {imdbid} was not found!'\n"
                            )
                    
                if (movieid == list_of_movies[-1]):
                    break

        self.imdb_content = [list_of_fields] + self.get_top_sequence(self.imdb_content, 0, None, True)
        
        return self.imdb_content

    def top_highest_grossing_directors(self, top_n=None) -> dict:
        directors:  dict = {None: 0}
        """
        Метод возвращает словарь с топ-n директорами,
        где ключами являются директора и значения представляют собой сумму
        мирового дохода у созданных ими фильмов.
        Словарь отсортирован по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Director' in self.imdb_content[0]) and \
                ('Gross worldwide' in self.imdb_content[0]):
            inx_director = self.imdb_content[0].index('Director')
            inx_gross_ww = self.imdb_content[0].index('Gross worldwide')

            directors = {
                director: 0
                for directors in self.imdb_content[1:]
                for director in directors[inx_director]
                if (director)
                }
            
            for item in self.imdb_content[1:]:
                gross = item[inx_gross_ww]

                for director in item[inx_director]:
                    if (directors.get(director) == 0) and (gross != None):
                        directors[director] += 0 if (not gross) else gross

            directors = self.get_top_sequence(directors.items(), 1, top_n, True)

        return dict(directors)

    def top_directors(self, top_n=None) -> dict:
        directors:  dict = {None: 0}
        """
        Метод возвращает словарь с топ-n директорами,
        где ключами являются директора и значения представляют собой количество
        созданных ими фильмов.
        Отсортируйте его по номерам по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Director' in self.imdb_content[0]):
            directors = [
                director
                for directors in self.imdb_content[1:]
                for director in directors[self.imdb_content[0].index('Director')]
                if (director)
                ]
            directors = dict(collections.Counter(directors))
            directors = self.get_top_sequence(directors.items(), 1, top_n, True)

        return dict(directors)

    def most_expensive(self, top_n=None) -> dict:
        budgets:    dict = {None: 0}
        """
        Метод возвращает словарь с топ-n фильмами,
        где ключами являются названия фильмов и ценности — это их бюджеты.
        Отсортируйте по бюджетам по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Title' in self.imdb_content[0]) and \
                ('Budget' in self.imdb_content[0]):
            budgets = {
                budget[self.imdb_content[0].index('Title')]: \
                    budget[self.imdb_content[0].index('Budget')]
                for budget in self.imdb_content[1:]
            }
            budgets = self.get_top_sequence(budgets.items(), 1, top_n, True)
        
        return dict(budgets)
        
    def most_profitable(self, top_n=None) -> dict:
        profits:    dict = {None: 0}
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов и
        значения представляют собой разницу между совокупным мировым валовым доходом и бюджетом.
        Отсортируйте по разнице по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Title' in self.imdb_content[0]) and \
                ('Budget' in self.imdb_content[0]) and \
                    ('Gross worldwide' in self.imdb_content[0]):
            profits = {
                profit[self.imdb_content[0].index('Title')]: \
                    profit[self.imdb_content[0].index('Gross worldwide')] - \
                    profit[self.imdb_content[0].index('Budget')]
                for profit in self.imdb_content[1:]
                if  profit[self.imdb_content[0].index('Gross worldwide')] and \
                    profit[self.imdb_content[0].index('Budget')]
            }
            profits = self.get_top_sequence(profits.items(), 1, top_n, True)

        return dict(profits)
        
    def longest(self, top_n=None) -> dict:
        runtimes:   dict = {None: 0}
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов и
        значения — это время их выполнения. Если версий несколько – выберите любую.
        Отсортируйте его по времени выполнения по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Title' in self.imdb_content[0]) and \
                ('Runtime' in self.imdb_content[0]):
            runtimes = {
                runtime[self.imdb_content[0].index('Title')]: \
                    runtime[self.imdb_content[0].index('Runtime')]
                for runtime in self.imdb_content[1:]
            }
            runtimes = self.get_top_sequence(runtimes.items(), 1, top_n, True)
        
        return dict(runtimes)
        
    def top_cost_per_minute(self, top_n=None) -> dict:
        costs:      dict = {None: 0}
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов и
        значения представляют собой бюджеты, разделенные на время их выполнения.
        Бюджеты могут быть в разных валютах – не обращайте на это внимания.
        Значения должны быть округлены до двух десятичных знаков. 
        Отсортируйте его по убыванию.
        """
        if (self.imdb_content and self.isint(top_n)) and \
            ('Title' in self.imdb_content[0]) and \
                ('Budget' in self.imdb_content[0]) and \
                    ('Runtime' in self.imdb_content[0]):
            costs = {
                cost[self.imdb_content[0].index('Title')]: \
                    round(
                        cost[self.imdb_content[0].index('Budget')] /
                        (cost[self.imdb_content[0].index('Runtime')] / 60),
                        2
                        )
                for cost in self.imdb_content[1:]
                if  cost[self.imdb_content[0].index('Budget')] and \
                    cost[self.imdb_content[0].index('Runtime')]
            }
            costs = self.get_top_sequence(costs.items(), 1, top_n, True)

        return dict(costs)

    def get_top_sequence(self, sequence, key, top_n, reverse=False) -> dict:
        """
        Метод возвращает отсортированный словарь с топ-n элементами.
        """
        return sorted(
                    sequence,
                    key=lambda val: val[key] if (val[key]) else 0,
                    reverse=reverse,
                )[:top_n]
    
    def isint(self, num) -> True:
        try:
            assert (isinstance(num, (int)) or (num == None)), \
                ('TypeError: slice indices must be integers or None!')
            return True
        except AssertionError as er_msg:
            sys.stderr.write(f"{er_msg}\n")

class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file) -> None:
        """
        Put here any fields that you think you will need.
        """
        def _set_filepath_(self, path_to_the_file) -> None:
            if not (isinstance(path_to_the_file, (str))):
                raise AttributeError(f"ValueError: Invalid file path: {type(path_to_the_file)}")
            if not path_to_the_file:
                raise TypeError("TypeError: read_csv() missing 1 required positional argument: 'filepath'")
            if not os.path.exists(path_to_the_file):
                raise FileNotFoundError(f"FileNotFoundError: [Errno 2] No such file or directory: '{path_to_the_file}'")

            self.path_to_the_file = path_to_the_file

        def _read_from_file(self) -> None:
            def _check_line(elem) -> str:
                if not elem:
                    raise ValueError('Line is empty')
                if not len(elem) == 4:
                    raise ValueError('Wrong number of columns')
                if (
                    not isinstance(elem[2], str)
                    ):
                    raise ValueError('Invalide file structure')
                try:
                    int(elem[0])
                    int(elem[1])
                    int(elem[3])
                except:
                    raise ValueError('Invalide file structure')
                return elem
                
            with open(self.path_to_the_file, 'r') as file:
                if file.readline() != 'userId,movieId,tag,timestamp\n':
                    raise ValueError('Invalide file structure')
                self.tags = [_check_line(line.strip().split(',')) for line in file]
              
        try:
            self.path_to_the_file: str = ''
            self.tags: list = [[]]
            _set_filepath_(self, path_to_the_file)
            _read_from_file(self)

        except (ValueError, AttributeError, FileNotFoundError, IsADirectoryError, TypeError) as er_msg:
            sys.stderr.write(f"{er_msg}\n")
            if len(sys.argv) == 2:
                return
            raise er_msg

    def _custom_raise(self, er_msg: Exception) -> None:
        sys.stderr.write(f"{er_msg}\n")
        if len(sys.argv) == 2:
            return
        raise er_msg

    def most_words(self, top_n=None) -> dict:
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = None
        try:
            big_tags = functools.reduce(lambda a, b: a | b, map(lambda x: {x[2]: len(x[2].split())}, self.tags))
            big_tags = dict(sorted(set(big_tags.items()), key=lambda item: item[1], reverse=True)[:top_n])
        except (TypeError, ValueError, AttributeError, IndexError) as er_msg:
            self._custom_raise(er_msg)
        return big_tags
        
    def longest(self, top_n=None) -> list:
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        longest_tags = None
        try:
            big_tags =  set(item[2] for item in self.tags)
            longest_tags = sorted(big_tags, key=lambda item: len(item), reverse=True)[:top_n]
        except (TypeError, ValueError, AttributeError, IndexError) as er_msg:
            self._custom_raise(er_msg)
        return longest_tags
    
    def most_words_and_longest(self, top_n=None) -> list:
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        most_words_longest = None
        try:
            most_words = self.most_words(top_n).keys()
            longest = set(self.longest(top_n))
            most_words_longest = list(most_words & longest)
        except Exception as er_msg:
            self._custom_raise(er_msg)
        return most_words_longest
        
    def most_popular(self, top_n=None) -> dict:
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        popular_tags = None
        try:
            popular_tags = dict(collections.Counter(map(lambda x: x[2], self.tags)).most_common(top_n))
        except (TypeError, ValueError, AttributeError, IndexError) as er_msg:
            self._custom_raise(er_msg)
        return popular_tags
        
    def tags_with(self, word='') -> list:
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tags_with_word = None
        try:
            tags = map(lambda x: x[2], self.tags)
            tags_with_word = sorted(set(filter(lambda x: word.lower() in x.lower(), tags)))
        except (TypeError, ValueError, AttributeError, IndexError) as er_msg:
            self._custom_raise(er_msg)
        return tags_with_word


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file
        self.movies = self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.path_to_the_file, 'r') as f:
                if f.readline() != 'movieId,title,genres\n':
                    raise ValueError
                for line in f:
                    yield line
        except ValueError:
            raise ValueError('File structure is incorrect')
        except:
            raise

    def extract_column(self, line, column_number):

        if not line:
            raise ValueError('Line is empty')
        if not isinstance(line, str):
            raise ValueError("First argument must be string")
        if not isinstance(column_number, int):
            raise ValueError("Second argument must be int")

        column = re.split(r',(?=[^"]*(?:"[^"]*"[^"]*)*$)', line)
        if len(column) < column_number:
            raise ValueError('Column number is incorrect')
        column = column[column_number].strip('"')
        if not column:
            raise ValueError('Column is empty')
        return column

    def extract_year(self, line):

        if not isinstance(line, str):
            raise ValueError("Argument must be string")

        year = re.search(r'\((\d{4})\)', line)
        if year:
            year = year.group(1).strip("()")
        else:
            year = "Unknown"
        return year

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = {}
        for movie in self.movies: 
            title = self.extract_column(movie, 1)
            year = self.extract_year(title)
            if year in release_years:
                release_years[year] += 1
            else:
                release_years[year] = 1
        self.movies = self.read_from_file()
        return dict(sorted(release_years.items(), key=lambda x: x[1], reverse=True))
    
    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres_cnt = {}
        for movie in self.movies: 
            genres = self.extract_column(movie, 2).strip('()').split('|')
            for genre in genres:
                genre = genre.strip()
                if genre in genres_cnt:
                    genres_cnt[genre] += 1
                else:
                    genres_cnt[genre] = 1
        self.movies = self.read_from_file()
        return dict(sorted(genres_cnt.items(), key=lambda x: x[1], reverse=True))
        
    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        if not isinstance(n, int):
            raise ValueError("Argument must be int")
        movies = {}
        for movie in self.movies: 
            title = self.extract_column(movie, 1)
            genres = self.extract_column(movie, 2).strip('()').split('|')
            movies[title] = len(genres)
        return dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])

class Ratings:
    """
    Analyzing data from ratings.csv
    """    
    def __init__(self, path_to_the_file):
        """
        Initializes the Ratings class with data from the given file.
        """
        self.path = path_to_the_file

        try:
            with open(path_to_the_file, 'r') as ratings:
                self.ratings = ratings.readlines()

            if not self.ratings:
                raise ValueError(f"File is empty: {path_to_the_file}")
                
            if len(self.ratings) == 1:
                raise ValueError(f"File has only header: {path_to_the_file}")

            for line in self.ratings[1:]:
                try:
                    user_id, movie_id, rating, timestamp = line.strip().split(',')
                    float(rating)
                    int(timestamp)
                    
                except ValueError:
                    raise ValueError(f"Invalid data format in file: {path_to_the_file}")

            self.movies = self.Movies(self.ratings)
            self.users = self.Users(self.ratings)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path_to_the_file}")

        except IsADirectoryError:
            raise IsADirectoryError(f"Is a directory: {path_to_the_file}")
        
        except ValueError as e:
            raise e

    class Movies:

        def __init__(self, data):
            self.data = [
                tuple(i_elem for i_elem in re.split(r'\s*,\s*', i_line.strip())) 
                for i_line in data[1:]
            ]
            
            self.year = [
                self._convert(i_elem[3]) 
                for i_elem in self.data
            ]

            self.ratings = [
                self._convert(i_elem[2])
                for i_elem in self.data
            ]

            self.movie_id = [
                self._convert(i_elem[1])
                for i_elem in self.data
            ]

            self.movieid_rating = [
                (self._convert(i_elem[1]), self._convert(i_elem[2]))
                for i_elem in self.data
            ]

            self.movie_id_title = self._dict_movies_titles()

        def _convert(self, value):
            """
            The method convert value to int or float 
            """
            try:
                return int(value) if "." not in value else float(value)

            except ValueError:
                print(f"Error converting value '{value}' to number")
                raise ValueError(f"Cannot convert '{value}' to int or float")

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly.
            """
            try:
                years = [datetime.datetime.fromtimestamp(i_elem).year for i_elem in self.year]
                ratings_by_year = collections.Counter(years)
                return dict(sorted(ratings_by_year.items()))
                
            except (ValueError, OSError) as e:
                print(f"Error processing timestamps: {e}")
                return {}
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings_distribution = collections.Counter(self.ratings)
            ratings_distribution = dict(sorted(ratings_distribution.items()))

            return ratings_distribution
        
        def _dict_movies_titles(self):
            """
            The method returns a dict where the keys are movies id and the values are movie titles
            """
            try:
                with open("../datasets/ml-latest-small/movies.csv", "r") as movie:
                    movie_data = movie.readlines()
                
                movie_id_title_genre = [re.split(r'\s*,\s*', i) for i in movie_data[1:]]
                
                return {self._convert(i[0]): i[1] for i in movie_id_title_genre}
                
            except FileNotFoundError:
                print("Error: movies.csv file not found")
                return {}
                
            except IsADirectoryError:
                print(f"Error: movies.csv is a directory")
                return {}

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            if not isinstance(n, int) or n <= 0:
                raise ValueError('n must be a positive integer')

            top_movies = self._change_mov_id_to_title(collections.Counter(self.movie_id), n)
            return dict(top_movies)
        
        def top_by_ratings(self, n, metric="average"):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            if not isinstance(n, int) or n <= 0:
                raise ValueError('n must be a positive integer')
            if metric not in ["average", "median"]:
                raise ValueError('metric must be either "average" or "median"')

            dict_mov_id_ratings = self._append_values_to_dict(self.movieid_rating)

            if metric == "average":
                results = self._average_rating(dict_mov_id_ratings)
            elif metric == "median":
                results = self._median_rating(dict_mov_id_ratings)
                
            top_movies = self._change_mov_id_to_title(results, n)
            return dict(top_movies)
        
        def _average_rating(self, dict_ratings):
            """
            The method returns a dict where the keys are movie id and the values are average ratings
            """
            average_ratings = dict()
            try:
                for i_key in dict_ratings:
                    if len(dict_ratings[i_key]) == 0:
                        raise ZeroDivisionError("Empty list in average calculation")
                    average = sum(dict_ratings[i_key]) / len(dict_ratings[i_key])
                    average_ratings[i_key] = round(average, 2)
                return average_ratings

            except ZeroDivisionError:
                print("Error: Division by zero in average calculation")
                return {}
        
        def _median_rating(self, dict_ratings):
            """
            The method returns a dict where the keys are movie id and the values are median ratings
            """
            median_ratings = dict()
            try:
                for i_key in dict_ratings:
                    if len(dict_ratings[i_key]) == 0:
                        raise IndexError("Empty list in median calculation")
                    sort_ratings = sorted(dict_ratings[i_key])
                    mid = len(sort_ratings) // 2
                    med_rating = (sort_ratings[mid] if len(sort_ratings) % 2 != 0
                                  else (sort_ratings[mid-1] + sort_ratings[mid]) / 2)
                    median_ratings[i_key] = round(med_rating, 2)
                return median_ratings
                
            except IndexError:
                print("Error: Empty list in median calculation")
                return {}
        
        def _change_mov_id_to_title(self, mov_id_ratings, n):
            """
            The method returns a dict where the keys movie titles and the values are ratings
            """
            top_movies = [
                (self.movie_id_title[i_key], i_value)
                for i_key, i_value in mov_id_ratings.items()
                if i_key in self.movie_id_title
            ]

            return sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]

        def _append_values_to_dict(self, data):
            """
            The method returns a dict where the keys are movies or users id and the values are the list with ratings
            """
            dict_movieid_ratings = collections.defaultdict(list)

            for i_elem in data:
                dict_movieid_ratings[i_elem[0]].append(i_elem[1])
                
            return dict_movieid_ratings
        
        def _variance_rating(self, dict_movid_ratings):
            """
            The method returns a dict where the keys are movie id and the values are variance of the ratings
            """
            try:
                result = dict()
                for key, values in dict_movid_ratings.items():
                    if len(values) == 0:
                        raise ZeroDivisionError("Division by zero in variance calculation")
                    n = len(values)
                    average_rating = sum(values) / n
                    variance = sum(((x - average_rating) ** 2 for x in values)) / n
                    result[key] = round(variance, 2)
                return result
                
            except ZeroDivisionError:
                print("Error: Division by zero in variance calculation")
                return {}

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            try:
                if not isinstance(n, int) or n <= 0:
                    raise ValueError('n must be a positive integer')

                dict_mov_id_ratings = self._append_values_to_dict(self.movieid_rating)
                result = self._variance_rating(dict_mov_id_ratings)

                top_movies = dict(self._change_mov_id_to_title(result, n))

                return top_movies
                
            except ValueError as e:
                print(f"Error in top_controversial: {e}")
                return {}

        def least_num_of_ratings(self, n):
            """
            The method returns top-n movies with the least ratings.
            It is a dict where the keys are movie titles and the values are counts.
            Sort it by number of ratings ascendingly.
            """
            try:
                if not isinstance(n, int) or n <= 0:
                    raise ValueError('n must be a positive integer')
                
                dict_mov_id_ratings = self._append_values_to_dict(self.movieid_rating)

                movies_rating_counts = {movie_id: len(ratings) for movie_id, ratings in dict_mov_id_ratings.items()}
                
                sorted_movies = sorted(movies_rating_counts.items(), key=lambda x: x[1])[:n]
                
                result = {self.movie_id_title[movie_id]: count 
                         for movie_id, count in sorted_movies 
                         if movie_id in self.movie_id_title}
                
                return result
                
            except ValueError as e:
                print(f"Error in least_rated_movies: {e}")
                return {}
                
        def movies_above_threshold(self, threshold, metric="average"):
            """
            The method returns a dict where the keys are movie titles and the values are the ratings above the threshold.
            Sort it by ratings descendingly.
            """
        
            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 5:
                raise ValueError('threshold must be a number between 0 and 5')
            if metric not in ["average", "median"]:
                raise ValueError('metric must be either "average" or "median"')
            
            dict_mov_id_ratings = self._append_values_to_dict(self.movieid_rating)
            
            if metric == "average":
                results = self._average_rating(dict_mov_id_ratings)
            elif metric == "median":
                results = self._median_rating(dict_mov_id_ratings)

            results = dict(self._change_mov_id_to_title(results, n=len(results)))

            movies_above_threshold = {movie_id: rating 
                                        for movie_id, rating in results.items() 
                                        if rating > threshold}
            
            return dict(sorted(movies_above_threshold.items(), key=lambda x: x[1], reverse=True))


    class Users(Movies):

        def __init__(self, data):
            super().__init__(data)

            self.user_id = [
                self._convert(i_elem[0])
                for i_elem in self.data
            ]

            self.user_id_rating = [
                (self._convert(i_elem[0]), self._convert(i_elem[2]))
                for i_elem in self.data
            ]

        def dist_users_by_num_of_rating(self):
            """
            The method returns a dict where the keys are users id and the values are counts.
            Sort it by ratings ascendingly.
            """
            users_num_of_ratings = collections.Counter(self.user_id)
            return dict(sorted(users_num_of_ratings.items(), key=lambda x: x[1], reverse=True))

        def dist_users_by_rating(self, metric="average"):
            """
            The method returns users id by the average or median of the ratings.
            It is a dict where the keys are users id and the values are metric values.
            Sort it by metric descendingly.
            The values were rounded to 2 decimals.
            """
            if metric not in ["average", "median"]:
                raise ValueError('metric must be either "average" or "median"')

            dict_user_id_ratings = self._append_values_to_dict(self.user_id_rating)

            if metric == "average":
                results = self._average_rating(dict_user_id_ratings)
            elif metric == "median":
                results = self._median_rating(dict_user_id_ratings)

            return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

        def top_users_with_biggest_var(self, n):
            """
            The method returns top-n users id by the variance of their ratings.
            It is a dict where the keys are users id and the values are the variances.
            Sort it by variance descendingly.
            The values were rounded to 2 decimals.
            """
            try:
                if not isinstance(n, int) or n <= 0:
                    raise ValueError('n must be a positive integer')

                dict_user_id_ratings = self._append_values_to_dict(self.user_id_rating)
                result = self._variance_rating(dict_user_id_ratings)

                return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:n])
                
            except ValueError as e:
                print(f"Error in top_users_with_biggest_var: {e}")
                return {}

if __name__ == "__main__":
    pass

class Tests():
    class TestsLinks():
        links_object = Links('../datasets/ml-latest-small/links.csv')
        ttests_params = pytest.mark.parametrize(
                     'wrong,    method_name,              method,                           expectation,            reverse',
                    [
                    (False,     '.get_imdb()',                          links_object.get_imdb,                          list,                   True),
                    (False,     '.top_directors()',                     links_object.top_directors,                     dict,                   True),
                    (False,     '.most_expensive()',                    links_object.most_expensive,                    dict,                   True),
                    (False,     '.most_profitable()',                   links_object.most_profitable,                   dict,                   True),
                    (False,     '.longest()',                           links_object.longest,                           dict,                   True),
                    (False,     '.top_cost_per_minute()',               links_object.top_cost_per_minute,               dict,                   True),
                    (False,     '.get_top_sequence()',                  links_object.get_top_sequence,                  dict,                   True),
                    (False,     '.top_highest_grossing_directors()',    links_object.top_highest_grossing_directors,    dict,                   True),

                    (True,      '.get_imdb()',                          links_object.get_imdb,                          tuple,                  False),
                    (True,      '.top_directors()',                     links_object.top_directors,                     tuple,                  False),
                    (True,      '.most_expensive()',                    links_object.most_expensive,                    float,                  False),
                    (True,      '.most_profitable()',                   links_object.most_profitable,                   list,                   False),
                    (True,      '.longest()',                           links_object.longest,                           set,                    False),
                    (True,      '.top_cost_per_minute()',               links_object.top_cost_per_minute,               BeautifulSoup,          False),
                    (True,      '.get_top_sequence()',                  links_object.get_top_sequence,                  Links,                  False),
                    (True,      '.top_highest_grossing_directors()',    links_object.top_highest_grossing_directors,    Links,                  False),
                    ]
                )
        
        @pytest.mark.parametrize(
                     'wrong,  exception,          filepath',
                    [
                    (False,   None,               '..\\datasets\\ml-latest-small\\links.csv'),
                    (False,   None,               '../datasets/ml-latest-small/links.csv'),
                    (True,    AttributeError,     12345),
                    (True,    IsADirectoryError,  '../datasets/wrong-cases/empty_folder'),
                    (True,    FileNotFoundError,  '../datasets/wrong-cases/ml-latest-empty/link.csv'),
                    (True,    ValueError,         '../datasets/wrong-cases/ml-latest-empty/empty.csv'),
                    (True,    ValueError,         '../datasets/wrong-cases/ml-latest-wrong/links1.csv'),
                    (True,    ValueError,         '../datasets/wrong-cases/ml-latest-wrong/links2.csv'),
                    ]
                )
        def test_init_links_object(self, wrong, exception, filepath):  # тесты на ошибку инициализации Links()
            if (wrong):
                with pytest.raises(exception):
                    Links(filepath)
            else:
                pass

        @ttests_params
        def test_rights_links_methods__returned_right_data_type(self, wrong, method_name, method, expectation, reverse):  # если методы возвращают правильные типы данных
            if      (method_name == '.get_imdb()'):
                list_of_movieId = ['193609', 193600, 2, 6, 200000, 2467, 903, 2176, 930, 2178]
                result = isinstance(method(list_of_movieId), (expectation))
                assert (not result if (wrong) else result)

            elif    (method_name == '.get_top_sequence()'):
                dictionary = {str(num): num for num in range(1, 500 + 1)}
                result = isinstance(dict(method(dictionary.items(), 1, 5, reverse=False)), (expectation))
                assert (not result if (wrong) else result)

            else:
                top_n = 5
                result = isinstance(method(top_n), (expectation))
                assert (not result if (wrong) else result)

        @ttests_params
        def test_links_methods__right_data_type_in_the_list_of_elements(self, wrong, method_name, method, expectation, reverse):  # если элементы списка имеют правильные типы данных
            if      (method_name == '.get_imdb()'):
                result = all(
                    [isinstance(item, (tuple if wrong else list)) 
                     for item in self.links_object.imdb_content[1:]
                     ])
                assert (not result if (wrong) else result)

        @ttests_params
        def test_for_correct_sorting_of_return_data(self, wrong, method_name, method, expectation, reverse):  # если возвращенные данные отсортированы правильно
            if      (method_name == '.get_imdb()'):
                result = self.links_object.imdb_content[1:] == \
                    sorted(self.links_object.imdb_content[1:], key=lambda val: val[0], reverse=reverse)
                assert (not result if (wrong) else result)

            elif    (method_name == '.get_top_sequence()'):
                dictionary = {str(num): num for num in range(1, 15 + 1)}
                result = list(dict(method(dictionary.items(), 1, None, reverse=True)).values()) == \
                    list(dict(sorted(dictionary.items(), key=lambda val: val[1], reverse=reverse)).values())
                assert (not result if (wrong) else result)

            else:
                top_n = 15
                dictionary = method(top_n)
                result = list(dictionary.items()) == \
                    list(dict(sorted(dictionary.items(), key=lambda val: val[1] if (val[1]) else 0, reverse=reverse)).items())
                assert (not result if (wrong) else result)

        @ttests_params
        def test_feedback_values(self, wrong, method_name, method, expectation, reverse):
            if not wrong:
                if (method_name == '.top_directors()'):
                    assert list(method().items())[0] == ('Alfred Hitchcock', 4)

                if (method_name == '.most_expensive:()'):
                    assert list(method().items())[0] == ('The Name of the Rose', 30000000000)

                if (method_name == '.most_profitable::()'):
                    assert list(method().items())[0] == ('Jumanji', 197821940)

                if (method_name == '.longest:()'):
                    assert list(method().items())[0] == ('Heat', 10200)
                
                if (method_name == '.top_cost_per_minute()'):
                    assert list(method().items())[0] == ('The Name of the Rose', 230769230.77)

                if (method_name == '.top_highest_grossing_directors()'):
                    assert list(method().items())[0] == ('Joe Johnston', 262821940)

    class TestsTags:
        class TestsWrongUsage:
            def test_wrong_file(self):
                with pytest.raises(FileNotFoundError):
                    Tags('aaaaa').longest(4)

            def test_empty_file(self):
                with pytest.raises(ValueError):
                    Tags('../datasets/wrong-cases/ml-latest-empty/empty.csv').longest(5)

            def test_wrong_struct(self):
                with pytest.raises(ValueError):
                    Tags('../datasets/wrong-cases/ml-latest-wrong/tags.csv').longest(5)

            def test_only_header(self):
                assert Tags('../datasets/wrong-cases/ml-latest-empty/tags-only-header.csv').longest(5) == []

        t = Tags('../datasets/ml-latest-small/tags.csv')
        def test_most_words(self):
            most_words = self.t.most_words(5)
            assert isinstance(most_words, dict)
            for key in most_words.keys():
                assert key == str(key)
                assert int(most_words[key]) > 0
            assert list(most_words.items()) == sorted(most_words.items(), key=lambda item: item[1], reverse=True)

            with pytest.raises(Exception):
                self.t.most_words('1')

        def test_longest(self):
            longest = self.t.longest(5)
            assert isinstance(longest, list)
            assert len(longest) == 5
            for tag in longest:
                assert isinstance(tag, str)
            assert list(longest) == sorted(longest, key=lambda item: len(item), reverse=True)
            assert len(longest) == len(set(longest))
            longest_empty = self.t.longest(0)
            assert longest_empty == []

            with pytest.raises(Exception):
                self.t.longest('1')

        def test_most_words_and_longest(self):
            most_words_and_longest = self.t.most_words_and_longest(5)
            assert isinstance(most_words_and_longest, list)
            for tag in most_words_and_longest:
                assert isinstance(tag, str)
            most_words_and_longest_empty = self.t.most_words_and_longest(0)
            assert most_words_and_longest_empty == []
            assert len(most_words_and_longest) == len(set(most_words_and_longest))

            with pytest.raises(Exception):
                self.t.most_words_and_longest('1')
        
        def test_most_popular(self):
            most_popular = self.t.most_popular(5)
            assert isinstance(most_popular, dict)
            assert len(most_popular) == 5
            for key in most_popular.keys():
                assert isinstance(key, str)
                assert int(most_popular[key]) > 0
            assert list(most_popular.items()) == sorted(most_popular.items(), key=lambda item: item[1], reverse=True)
            most_popular_empty = self.t.most_popular(0)
            assert most_popular_empty == {}

            with pytest.raises(Exception):
                self.t.most_popular('1')

        def test_tags_with(self):
            tags = self.t.tags_with('comedy')
            assert isinstance(tags, list)
            for tag in tags:
                assert isinstance(tag, str)
            assert len(tags) == len(set(tags))
            assert tags == sorted(tags)

            tags_wrong = self.t.tags_with('aaaaaaaaaaaaa')
            assert isinstance(tags_wrong, list)
            assert len(tags_wrong) == 0

            with pytest.raises(Exception):
                self.t.tags_with(1)

    class TestsMovies:
        class TestsWrongUsage:
            def test_wrong_file(self):
                with pytest.raises(FileNotFoundError):
                    Movies('aaaaa').most_genres(5)

            def test_empty_file(self):
                with pytest.raises(ValueError):
                    Movies('../datasets/wrong-cases/ml-latest-empty/empty.csv').most_genres(5)

            def test_wrong_struct(self):
                with pytest.raises(ValueError):
                    Movies('../datasets/wrong-cases/ml-latest-wrong/movies.csv').most_genres(5)

            def test_only_header(self):
                assert Movies('../datasets/wrong-cases/ml-latest-empty/movies-only-header.csv').most_genres(5) == {}
        
        m = Movies('../datasets/ml-latest-small/movies.csv')
        def test_dist_by_release(self):
            release_years = self.m.dist_by_release()
            assert isinstance(release_years, dict) or isinstance(release_years, collections.OrderedDict)
            for key in release_years.keys():
                try:
                    assert int(key) > 0
                except:
                    assert key == "Unknown"
                assert int(release_years[key]) > 0
            assert list(release_years.items()) == sorted(release_years.items(), key=lambda item: item[1], reverse=True)

        def test_dist_by_genres(self):
            genres_cnt = self.m.dist_by_genres()
            assert isinstance(genres_cnt, dict)
            for key in genres_cnt.keys():
                assert key == str(key)
                assert int(genres_cnt[key]) > 0
            assert list(genres_cnt.items()) == sorted(genres_cnt.items(), key=lambda item: item[1], reverse=True)

        def test_most_genres(self):
            most_genres = self.m.most_genres(5)
            assert isinstance(most_genres, dict)
            for key in most_genres.keys():
                assert key == str(key)
                assert int(most_genres[key]) > 0
            assert list(most_genres.items()) == sorted(most_genres.items(), key=lambda item: item[1], reverse=True)

            with pytest.raises(ValueError):
                self.m.most_genres('1')

        def test_most_genres_empty(self):
            most_genres = self.m.most_genres(0)
            assert most_genres == {}

    
        def test_extract_column(self):
            assert self.m.extract_column('1,2,3', 1) == '2'
            assert self.m.extract_column('1,"222,222",3', 1) == '222,222'
            with pytest.raises(ValueError):
                self.m.extract_column('1,,3', 1)
            with pytest.raises(ValueError):
                self.m.extract_column('1,2,3', 4)
            with pytest.raises(ValueError):
                self.m.extract_column('', 1)
            assert isinstance(self.m.extract_column('1,2,3', 2), str)

            with pytest.raises(ValueError):
                self.m.extract_column(1,1)

            with pytest.raises(ValueError):
                self.m.extract_column('a',';1')

        def test_extract_year(self):

            with pytest.raises(ValueError):
                self.m.extract_year(1234)

            assert int(self.m.extract_year('aaaaa(1991)')) == 1991
            assert self.m.extract_year('aaaaa1991') == 'Unknown'
            assert self.m.extract_year('a') == 'Unknown'

    class TestRatings:
        @classmethod
        def setup_class(cls):
            with open("empty_file.csv", "w") as f:
                f.write("")
                
            with open("only_header.csv", "w") as f:
                f.write("userId,movieId,rating,timestamp\n")
                
            with open("wrong_data_format.csv", "w") as f:
                f.write("userId,movieId,rating,timestamp\n")
                f.write("1,a,invalid,wrong\n")
                
            with open("ratings_test.csv", "w") as f:
                f.write("userId,movieId,rating,timestamp\n")
                f.write("1,1,4.0,1577836800\n")
                
        @classmethod
        def teardown_class(cls):
            test_files = ["empty_file.csv", "only_header.csv", 
                        "wrong_data_format.csv", "invalid_timestamp.csv", "ratings_test.csv"]
            for file in test_files:
                if os.path.exists(file):
                    os.remove(file)

        def test_wrong_path(self):
            with pytest.raises(FileNotFoundError):
                Ratings("wrong_path.csv")

        def test_is_directory(self):
            with pytest.raises(IsADirectoryError):
                Ratings(".")

        def test_empty_file(self):
            with pytest.raises(ValueError):
                Ratings("empty_file.csv")

        def test_wrong_data_format(self):
            with pytest.raises(ValueError):
                Ratings("wrong_data_format.csv")

        def test_only_header(self):
            with pytest.raises(ValueError):
                Ratings("only_header.csv")

        def test_dist_by_year(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            years_dist = result.movies.dist_by_year()
            
            assert isinstance(years_dist, dict)
            
            for year, count in years_dist.items():
                assert isinstance(year, int)
                assert isinstance(count, int)
                assert count > 0
            
            assert list(years_dist.keys()) == sorted(years_dist.keys())

        def test_dist_by_rating(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            ratings_dist = result.movies.dist_by_rating()
            
            assert isinstance(ratings_dist, dict)
            for rating, count in ratings_dist.items():
                assert isinstance(rating, float)
                assert isinstance(count, int)
                assert 0.5 <= rating <= 5.0
                assert count > 0
            
            assert list(ratings_dist.keys()) == sorted(ratings_dist.keys())

        def test_top_by_num_of_ratings(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            top_movies = result.movies.top_by_num_of_ratings(10)
            
            assert isinstance(top_movies, dict)
            assert len(top_movies) <= 10
            
            for title, count in top_movies.items():
                assert isinstance(title, str)
                assert isinstance(count, int)
                assert count > 0
            
            assert list(top_movies.values()) == sorted(top_movies.values(), reverse=True)

        def test_top_by_ratings(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            top_movies = result.movies.top_by_ratings(10)
            
            assert isinstance(top_movies, dict)
            assert len(top_movies) <= 10
            
            for title, rating in top_movies.items():
                assert isinstance(title, str)
                assert isinstance(rating, float)
                assert 0.5 <= rating <= 5.0
                
            assert list(top_movies.values()) == sorted(top_movies.values(), reverse=True)

        def test_top_controversial(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            controversial = result.movies.top_controversial(10)
            
            assert isinstance(controversial, dict)
            assert len(controversial) <= 10
            
            for title, variance in controversial.items():
                assert isinstance(title, str)
                assert isinstance(variance, float)
                assert variance >= 0
                
            assert list(controversial.values()) == sorted(controversial.values(), reverse=True)

        def test_least_num_of_ratings(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            least_rated_movies = result.movies.least_num_of_ratings(10)
            
            assert isinstance(least_rated_movies, dict)
            assert len(least_rated_movies) <= 10

        def test_movies_above_threshold(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            movies_above_threshold = result.movies.movies_above_threshold(3.5, "average")
            
            assert isinstance(movies_above_threshold, dict)
            
            for movie_title, rating in movies_above_threshold.items():
                assert isinstance(movie_title, str)
                assert isinstance(rating, float)
                assert rating > 3.5
            
            assert list(movies_above_threshold.values()) == sorted(movies_above_threshold.values(), reverse=True)
            

        def test_dist_users_by_num_of_rating(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            users_dist = result.users.dist_users_by_num_of_rating()
            
            assert isinstance(users_dist, dict)
            
            for user_id, count in users_dist.items():
                assert isinstance(user_id, int)
                assert isinstance(count, int)
                assert count > 0
            
            assert list(users_dist.keys()) == sorted(users_dist.keys(), key=lambda x: users_dist[x], reverse=True)

        def test_dist_users_by_rating(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            users_ratings = result.users.dist_users_by_rating("median")
            
            assert isinstance(users_ratings, dict)
            
            for user_id, rating in users_ratings.items():
                assert isinstance(user_id, int)
                assert isinstance(rating, float)
                assert 0.5 <= rating <= 5.0
                assert round(rating, 2) == rating
            
            assert list(users_ratings.keys()) == sorted(users_ratings.keys(), key=lambda x: users_ratings[x], reverse=True)
            
            avg_ratings = result.users.dist_users_by_rating("average")
            assert isinstance(avg_ratings, dict)
            assert len(avg_ratings) == len(users_ratings)
            assert list(avg_ratings.keys()) == sorted(avg_ratings.keys(), key=lambda x: avg_ratings[x], reverse=True)

        def test_top_users_with_biggest_var(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            top_users = result.users.top_users_with_biggest_var(10)
            
            assert isinstance(top_users, dict)
            assert len(top_users) <= 10
            
            for user_id, variance in top_users.items():
                assert isinstance(user_id, int)
                assert isinstance(variance, float)
                assert variance >= 0
                assert round(variance, 2) == variance
            
            assert list(top_users.values()) == sorted(top_users.values(), reverse=True)

        def test_invalid_n_parameter(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            with pytest.raises(ValueError):
                result.movies.top_by_num_of_ratings(-1)
            with pytest.raises(ValueError):
                result.movies.top_by_num_of_ratings(0)
            with pytest.raises(ValueError):
                result.movies.top_by_num_of_ratings("10")

        def test_invalid_metric_parameter(self):
            result = Ratings("../datasets/ml-latest-small/ratings.csv")
            with pytest.raises(ValueError):
                result.movies.top_by_ratings(10, metric="invalid")
            with pytest.raises(ValueError):
                result.users.dist_users_by_rating(metric="wrong")

        def test_movies_file_not_found(self):
            if os.path.exists("../datasets/ml-latest-small/movies.csv"):
                os.rename("../datasets/ml-latest-small/movies.csv", 
                        "../datasets/ml-latest-small/movies.csv.bak")
            try:
                result = Ratings("../datasets/ml-latest-small/ratings.csv")
                assert result.movies._dict_movies_titles() == {}
            finally:
                if os.path.exists("../datasets/ml-latest-small/movies.csv.bak"):
                    os.rename("../datasets/ml-latest-small/movies.csv.bak",
                            "../datasets/ml-latest-small/movies.csv")

        def test_timestamp_conversion(self):
            with pytest.raises(ValueError):
                with open("invalid_timestamp.csv", "w") as f:
                    f.write("userId,movieId,rating,timestamp\n")
                    f.write("1,1,5.0,invalid_time\n")
                Ratings("invalid_timestamp.csv")

    class TestRatingsSpecificInput:
        @classmethod
        def setup_class(cls):
            with open("test_first_10.csv", "w") as f:
                f.write("userId,movieId,rating,timestamp\n")
                f.write("1,1,4.0,964982703\n")
                f.write("1,3,4.0,964981247\n")
                f.write("1,6,4.0,964982224\n")
                f.write("1,47,5.0,964983815\n")
                f.write("1,50,5.0,964982931\n")
                f.write("1,70,3.0,964982400\n")
                f.write("1,101,5.0,964980868\n")
                f.write("1,110,4.0,964982176\n")
                f.write("1,151,5.0,964984041\n")
                f.write("1,157,5.0,964984100\n")

        @classmethod
        def teardown_class(cls):
            if os.path.exists("test_first_10.csv"):
                os.remove("test_first_10.csv")

        def test_dist_by_year(self):
            result = Ratings("test_first_10.csv")
            years_dist = result.movies.dist_by_year()
            assert isinstance(years_dist, dict)
            assert len(years_dist) == 1
            assert list(years_dist.keys()) == [2000]
            assert years_dist[2000] == 10

        def test_dist_by_rating(self):
            result = Ratings("test_first_10.csv")
            ratings_dist = result.movies.dist_by_rating()
            assert isinstance(ratings_dist, dict)
            assert len(ratings_dist) == 3
            assert list(ratings_dist.keys()) == [3.0, 4.0, 5.0]
            assert ratings_dist[3.0] == 1
            assert ratings_dist[4.0] == 4
            assert ratings_dist[5.0] == 5

        def test_users_dist_by_num_of_rating(self):
            result = Ratings("test_first_10.csv")
            users_dist = result.users.dist_users_by_num_of_rating()
            assert isinstance(users_dist, dict)
            assert len(users_dist) == 1
            assert list(users_dist.keys()) == [1]
            assert users_dist[1] == 10

        def test_users_dist_by_rating(self):
            result = Ratings("test_first_10.csv")
            users_ratings = result.users.dist_users_by_rating("average")
            assert isinstance(users_ratings, dict)
            assert len(users_ratings) == 1
            assert list(users_ratings.keys()) == [1]
            # Среднее: (3.0 + 4.0 + 4.0 + 4.0 + 4.0 + 5.0 + 5.0 + 5.0 + 5.0 + 5.0) / 10 = 4.4
            assert users_ratings[1] == 4.4

        def test_users_dist_by_rating_median(self):
            result = Ratings("test_first_10.csv")
            users_ratings = result.users.dist_users_by_rating("median")
            assert len(users_ratings) == 1
            assert list(users_ratings.keys()) == [1]
            # Медиана: [3.0, 4.0, 4.0, 4.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0] -> 4.5
            assert users_ratings[1] == 4.5

        def test_invalid_parameters_specific(self):
            result = Ratings("test_first_10.csv")
            with pytest.raises(ValueError):
                result.movies.movies_above_threshold(5.5)
            with pytest.raises(ValueError):
                result.movies.movies_above_threshold(-1)
