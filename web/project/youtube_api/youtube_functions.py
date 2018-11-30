def getYoutubeThumbnailUrl(url):
    start_string = "youtube.com/embed/"
    end_string = "?rel="
    start_index = url.find(start_string)+len(start_string)
    end_index = url.find(end_string)
    if ( start_index == len(start_string)-1 or end_index == -1):
        #return placeholder
        return False
    video_id = url[start_index:end_index]
    thumbnail_url = "https://i.ytimg.com/vi/%s/default.jpg" % video_id
    return thumbnail_url