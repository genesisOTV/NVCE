import feedparser
import regex

#Checks provided RSS URL for new headlines
def checkFeed(rawFeed):
    
    parsedFeed = feedparser.parse(rawFeed)
    Title = parsedFeed.entries[0].title
    print(Title)
    print(parsedFeed.entries[1].title)

    #Accesses last headline compiled
    f_read = open("lastHeadline.txt", "r")
    f_read.seek(0)
    oldHl = f_read.read()
    newHl = Title

    print (oldHl)
    f_read.close()

    newArticles = []
    if(newHl == oldHl):
        print("Feed not recently updated")
    else:
        #Compiles new headlines
        #print("New article(s) detected, refreshing list")
        f_write = open("lastHeadline.txt", "w")

        i = 0
        moreArticles = True
        while(moreArticles):
            if(parsedFeed.entries[i].title != oldHl):
                newArticle = parsedFeed.entries[i].title
                newArticles.append(newArticle)

                print("New article added: " + newArticle)
                i += 1
            else:
                print("Found")
                moreArticles = False

            if(i == len(parsedFeed.entries)):
                moreArticles = False
            elif(len(newArticles) >= 5):
                #Halt update after 10 iterations
                moreArticles = False
            
        print(newHl)
        f_write.write(newHl)

        f_write.close()

    return newArticles

