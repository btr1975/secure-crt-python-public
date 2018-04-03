# $language = "python"
# $interface = "1.0"
import logging
# import urllib2 <-- Removed due to SecureCRT not supporting _socket.pyd in windows
from HTMLParser import HTMLParser
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def get_post_url_data(url, method='GET', data=None, headers=None):
    """ <-- Removed due to SecureCRT not supporting _socket.pyd in windows
    Function to send a GET or POST message request http, or https
    :param url: The full url example http://www.python.org, https://www.yahoo.com:500/test
    :param method: Either GET, or POST
    :param data: A dictionary of data for parameters
    :param headers: A dictionary of headers
    :return:
        Returned data

    """
    LOGGER.debug('Starting get_post_url_data')
    if data:
        if not isinstance(data, dict):
            raise AttributeError('data needs to be a dictionary if supplied.')

    if headers:
        if not isinstance(headers, dict):
            raise AttributeError('data needs to be a dictionary if supplied.')

    if method not in ('GET', 'POST'):
        raise AttributeError('method needs to be GET or POST if supplied.')

    if data and method == 'GET':
        for_first = 0
        for key, value in data.items():
            if for_first == 0:
                url = '{url}?{key}={value}'.format(url=url, key=key, value=value)

            else:
                url = '{url}&{key}={value}'.format(url=url, key=key, value=value)

            for_first += 1
        data = None

    if data and headers:
        req = urllib2.Request(url, data=data, headers=headers)

    elif data:
        req = urllib2.Request(url, data=data)

    elif headers:
        req = urllib2.Request(url, headers=headers)

    else:
        req = urllib2.Request(url)

    response = urllib2.urlopen(req)
    response_data = response.read()
    return response_data


class FindDataInHTML(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data


def diff_prettyHtmlTable(diffs):
    """
    Function to convert a diff array into a pretty HTML report

    :param diffs: Array of diff tuples.  From Googles diff_match_patch library
    :return
        HTML Table

    """
    DIFF_DELETE = -1
    DIFF_INSERT = 1
    DIFF_EQUAL = 0
    html_table = list()
    html_table.append('<html>')
    html_table.append(
        """
        <style>
        body {
            background-color: #e8e3e3;
        }
        table {
            width: 100%;
            border-spacing: 1px;
        }
        td {
            border-left: 1px solid black;
            border-right: 1px solid black;
            font-family: "Lucida Console", "Courier New", "Times New Roman";
            padding-top: 0px;
            padding-left: 5px;
            padding-right: 5px;
            text-align: left;
        }
        </style>
        """
    )
    html_table.append('<table>')
    col_a_html = list()
    col_b_html = list()
    col_a_html.append("<td>")
    col_b_html.append("<td>")
    for (op, data) in diffs:
        text = (data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>"))

        if op == DIFF_DELETE:
            col_a_html.append("<del style=\"background:#ff5050;\">{text}</del>".format(text=text))

        elif op == DIFF_INSERT:
            col_b_html.append("<ins style=\"background:#00ff99;\">{text}</ins>".format(text=text))

        elif op == DIFF_EQUAL:
            col_a_html.append("{text}".format(text=text))
            col_b_html.append("{text}".format(text=text))

    col_a_html.append("</td>")
    col_b_html.append("</td>")
    html_table.append('<tr>{col_a}{col_b}</tr>'.format(col_a=''.join(col_a_html), col_b=''.join(col_b_html)))
    html_table.append('</table>')
    html_table.append('</html>')
    return ''.join(html_table)
