import os

import pandas as pd
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scripts.utility.data_loader import get_clean_review_df
import logging

from scripts.utility.path_utils import get_path_from_root

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sentiment_analysis(reviews):
    reviews["sentiment"] = reviews["text"].apply(lambda x: TextBlob(x).sentiment.polarity)
    reviews["sentiment_category"] = pd.cut(reviews["sentiment"], bins=3, labels=["negative", "neutral", "positive"])
    return reviews


def plot_sentiment_distribution(reviews, title, file_name):
    sentiment_count = reviews["sentiment_category"].value_counts().reindex(["negative", "neutral", "positive"])
    sentiment_count.plot(kind="bar", color=["red", "grey", "green"])
    plt.title(title)
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.savefig(os.path.join(get_path_from_root("results", "eda"), file_name))
    plt.close()


def keyword_extraction(reviews):
    words = "".join(reviews["text"]).split()
    word_freq = Counter(words)
    return word_freq


def plot_word_cloud(word_freq, title, file_name):
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=10).generate_from_frequencies(word_freq)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title)
    plt.tight_layout(pad=0)
    plt.savefig(os.path.join(get_path_from_root("results", "eda"), file_name))
    plt.close()


def main():
    review_data = get_clean_review_df()

    if not review_data.empty:
        sentiment_reviews = sentiment_analysis(review_data)
        plot_sentiment_distribution(sentiment_reviews, "Sentiment Distribution in Reviews",
                                    "sentiment_distribution.png")

        word_freq = keyword_extraction(sentiment_reviews)
        plot_word_cloud(word_freq, "Common Words in Reviews", "review_wordcloud.png")
    else:
        logger.error("Failed to load review data for analysis.")


if __name__ == "__main__":
    main()
