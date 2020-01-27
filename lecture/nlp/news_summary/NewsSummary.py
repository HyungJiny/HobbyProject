from gensim.summarization.summarizer import summarize
from newspaper import Article

def getNewsText(url):
    news = Article(url, language='ko')
    news.download()
    news.parse()
    return news.text

def main():
    news = getNewsText('https://steemit.com/dclick/@wonsama/-181023--1540308198584')
    print(summarize(news, ratio=0.1))

if __name__ == "__main__":
    main()

