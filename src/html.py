# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re


class codeforces:
    def parse_codeforces_problem(self, url):
        r = requests.get(url)
        html = BeautifulSoup(r.content, 'html.parser')

        def get(type):
            data = html.find_all('div', {'class': type})
            arr = []
            for item in data:
                arr.append(item.find('pre').get_text('\n'))
            return arr

        inputs = get(type='input')
        outputs = get(type='output')

        return {
            'in': inputs,
            'out': outputs
        }


    def parse_codeforces_contest(self, url):
        """
        return variable looks like:
        {
            site: 'codeforces',
            problems:
              [
                /contest/665/problem/A
                /contest/665/problem/B
                /contest/665/problem/C
                /contest/665/problem/D
                /contest/665/problem/E
                /contest/665/problem/F
              ]
        }
        """
        r = requests.get(url)
        html = BeautifulSoup(r.content, 'html.parser')

        links = []
        aux = html.find_all('td', {'class': 'id'})

        for item in aux:
            links.append(item.find('a').get('href'))

        return {
            'site': 'codeforces',
            'problems': links
        }


    def is_codeforces(self, url):
        """
        check if URL belongs to codeforces
        """
        return False

class uri:
    def parse_uri_contest(self, url):
        return None

    def parse_uri_problem(self, url):
        
        # <200b> hidden char found in uri1300
        undesired_characters = [u'', u'​']
        
        def cleanup(arr):
            # remove spaces
            arr = map (lambda x: x.strip(), arr);
            
            # replace undesired characters with ''
            for char in undesired_characters:
                for i, w in enumerate(arr):
                    arr[i] = arr[i].replace (char, '')
            
            # remove '' from array arr
            arr = filter (lambda x: x not in undesired_characters, arr)
            
            # append all with \n
            return ['\n'.join (arr)]
            
        r = requests.get(url)
        html = BeautifulSoup(r.content, 'html.parser')

        data = html.find_all('td')
        
        input = data[2].get_text().split('\n')
        output = data[3].get_text().split('\n')
       
        inputs = cleanup(input)
        outputs = cleanup(output)

        return {
            'in': inputs,
            'out': outputs
        }


    def is_uri(self, url):
        """
        check if URL belongs to URI
        """
        return False

if __name__ == '__main__':
    uri = uri()
    uri.parse_uri_problem(
        'https://www.urionlinejudge.com.br/repository/UOJ_1400_en.html')
