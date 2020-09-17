"""
Example script demonstrating how to create a Spark DataFrame by downloading and 
parsing some example data from the internet.
"""
from pyspark import SparkConf
from pyspark.sql import SparkSession, Row, DataFrame
from pyspark.sql import types as T
import urllib.request
import zipfile
import os
import json
import shutil
from tempfile import TemporaryDirectory
from typing import List
from operator import eq, ne
import click
from examples.utils import compose_es_query

DEMO_ACCOUNTS_DATA_URL='https://download.elastic.co/demos/kibana/gettingstarted/accounts.zip'


def get_from_url(url: str=DEMO_ACCOUNTS_DATA_URL, dest_dir:str='./demo_data/') -> str:
    """Makes a get request to the specified url, saving the resulting file in the specified directory.

    :param url: Url from which to get a file, defaults to DEMO_ACCOUNTS_DATA_URL
    :type url: str, optional
    :param dest_dir: Directory to store the downloaded file, defaults to './demo_data/'
    :type dest_dir: str, optional
    :return: Path to the downloaded file
    :rtype: str
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with urllib.request.urlopen(url) as data:
        basename = os.path.basename(url)
        file_path = os.path.join(dest_dir, basename)
        with open(file_path, 'wb') as f:
            f.write(data.read())
            print('\nDownloaded {url} to {filename}'.format(url=url, filename=file_path))
    return file_path


def extract_data_from_zip(zipfile_path: str):
    """Extracts a zipfile.

    :param zipfile_path: Path to the zipfile.
    :type zipfile_path: str
    """
    with zipfile.ZipFile(zipfile_path, 'r') as zipf:
        zipf.extractall(os.path.dirname(zipfile_path))
        print('\nExtracted {}'.format(zipfile_path))


def load_accounts_data(file_path: str, reverse: bool = False) -> List[Row]:
    """Loads the sample account data, available at DEMO_ACCOUNTS_DATA_URL, from 
    a local filepath. Formats the file by dropping every other row, the set to 
    keep can be toggled using the reverse parameter.

    :param file_path: File path where the demo accounts data lives.
    :type file_path: str
    :param reverse: [description], defaults to False
    :type reverse: bool, optional
    :return: A list of Row objects that can be used to create a spark dataframe.
    :rtype: List[Row]
    """
    data=[]
    with open(file_path, 'r') as f:
        for i, l in enumerate(f):
            op = ne if reverse else eq
            if op(i % 2, 0):
                data.append(Row(**json.loads(l)))

    print("\nParsed data from {}".format(file_path))
    return data


def with_extension(filename: str, extension: str = 'json') -> str:
    """Modifys a file path, pointing to a file with an extension, to have the given extension.

    E.g.:
    fpath = with_extension('/path/to/my/file.txt', 'json')
    fpath == 'path/to/my/file.json'

    :param filename: A path name to be modified.
    :type filename: str
    :param extension: The extension that we want the result to have, defaults to 'json'
    :type extension: str, optional
    :return: The modified path
    :rtype: str
    """
    dir_name = os.path.dirname(filename)
    fname = '.'.join([os.path.basename(filename).split('.')[0], extension])
    return dir_name + '/' + fname


def start_spark_session() -> SparkSession:
    """
    Creates a spark session object and makes the elasticsearch_hadoop jar files 
    available to support indexing data using the dataframe writer api.

    :return: Entry point for spark functionality supporting writing to ES.
    :rtype: SparkSession
    """
    sconf = SparkConf().set('spark.jars', os.environ['ES_HDP_JAR'])
    ss = SparkSession.builder.config(conf=sconf).getOrCreate()
    return ss


def write_df_to_es(dataframe: DataFrame, indexname: str):
    """Writes a dataframe to an ES index.

    :param dataframe: Dataframe containing the data to be written to ES.
    :type dataframe: DataFrame
    :param indexname: The name of the ES index to which data will be written.
    :type indexname: str
    """
    print("Writing dataframe to ES index: {indexname}".format(indexname=indexname))
    dataframe.write\
    .mode('overwrite')\
    .format('org.elasticsearch.spark.sql')\
    .option('es.nodes', 'localhost')\
    .option('es.port', 9200)\
    .option('es.resource', indexname)\
    .save()
    print("Success!")


def search_es_index_for_match(indexname: str, matchfields: dict = None) -> dict:  
    """Searchs an ES index by compiling a query using the provided dictionary.

    :param indexname: Name of the ES index to search
    :type indexname: str
    :param matchfields: A dictionary that should be composed of a field to 
    search and associated value to search for, if None a match_all query is 
    executed, defaults to None
    :type matchfields: dict, optional
    :return: [description]
    :rtype: dict
    """
    if matchfields is None:
        query = {"query": {"match_all": {}}}
    else:
        query = {"query": {"match": matchfields}}
    query = json.dumps(query).encode('utf-8')
    es_url = "http://127.0.0.1:9200/{indexname}/_search?pretty"\
        .format(indexname=indexname)
    print("Making GET request to url: {}".format(es_url))
    print("Payload: {}".format(query))
    req = urllib.request.Request(es_url, data=query, headers = {'Content-Type':'application/json'})
    result = urllib.request.urlopen(req)
    return json.loads(result.read().decode('utf-8'))


@click.group()
def cli():
    pass


@cli.command()
def spark_to_es():
    """
    First, initialises a spark dataframe using 'make-spark-dataframe', then 
    writes the data to an elasticsearch index.
    """
    df = spark_df_init()
    write_df_to_es(df, 'sparkindex')


@cli.command()
def make_spark_dataframe():
    """
    Gets some data from the web, and puts it into a spark dataframe.
    """
    df = spark_df_init()
    print("Successfully created spark df:")
    df.show(5, False)


@cli.command()
@click.option('--indexname', default='sparkindex')
@click.option('--match-all', is_flag=True, help="When this flag is passed, execute a match_all query.")
def search_es_index(indexname, match_all):
    """
    Searches an index by either composing a match query, or executing a match_all.
    """
    if not match_all:
        query = compose_es_query()
    else:
        query = None
    result = search_es_index_for_match(indexname, query)
    _ = input("Hit enter to see results..")
    print(json.dumps(result, indent=4))


def spark_df_init():
    """
    Gets some data from the web, and puts it into a spark dataframe.
    The following steps are executed:
      (1) Start a spark session.
      (2) Download the zipfile containing the data from the url provided.
      (3) Extract the contents of the zipfile.
      (4) Parse the extracted file into a format that can be used to create a Spark DataFrame.
      (5) Create a dataframe from the data parsed from the file.
    """

    # (1)
    ss = start_spark_session()

    # Keep things tidy by using a temporary directory context handler.
    with TemporaryDirectory() as tempdir:
        # (2)
        zipf = get_from_url(dest_dir=tempdir)

        # (3)
        extract_data_from_zip(zipf)

        # (4)
        data = load_accounts_data(with_extension(zipf), True)

        # (5)
        df = ss.createDataFrame(data)

    return df


if __name__ == '__main__':
  cli()
