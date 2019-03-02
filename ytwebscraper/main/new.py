from bs4 import BeautifulSoup
import requests,  json

def YoutubeScraper( queryString ):
    
    # # #<----- offline ----->
    # # I suggest you to use this instead of making multiple request in a short duration
    # # with open( 'path_to_any_youtube_search_result_file.html',  encoding="utf-8" ) as f:
    # #     data = f.read(  )
    # # soup = BeautifulSoup( data,  'html.parser' )

    headers = { 'User-Agent': 'Mozilla/5.0 ( Windows NT 6.1 ) AppleWebKit/537.36 ( KHTML,  like Gecko ) Chrome/41 Safari/537.36' }
    url = "https://www.youtube.com/results?search_query={}".format( queryString )
    page = requests.get( url,  headers )
    soup = BeautifulSoup( page.content,  'html.parser' )
    
    all_found_links = soup.select( "a.yt-uix-tile-link" )
    all_found_durations = [ i.get_text(  ) for i in soup.select( "span.video-time" ) ]
    all_found_titles = [ a['title'] for a in all_found_links ]
    all_found_urls = [ a['href'].replace( "https://www.youtube.com", "" ).replace( "/watch?v=", "" ) for a in all_found_links ]
    all_found_ids = [ id if "&list=" not in id else id[:id.index( "&list=" )] for id in all_found_urls ]

    zipped = zip( all_found_urls, all_found_titles, all_found_durations, all_found_ids )
    zipped = [ list( i ) for i in zipped ]
    resulting_collection = []
    for i in range( len( zipped ) ):
        item = {}
        item['url'] = "https://www.youtube.com/watch?v={}".format( zipped[i][0] )
        item['title'] = zipped[i][1]
        item['duration'] = zipped[i][2]
        item['img'] = "https://i.ytimg.com/vi/{}/hqdefault.jpg".format(  zipped[i][3]  )
        resulting_collection.append( item )

    return json.dumps( resulting_collection )

print( YoutubeScraper( 'What is web scraping?' ) )