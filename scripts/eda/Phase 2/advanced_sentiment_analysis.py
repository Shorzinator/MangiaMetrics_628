import os

import pandas as pd
from nltk import ngrams
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

from scripts.utility.path_utils import get_path_from_root

# nltk.download('vader_lexicon')
output_path = get_path_from_root("results", "eda", "Phase 2", "sentiment_analysis")


def plot_ngrams(ngrams, top_n=10, title="Top N-grams", file_name="ngram_plot.png"):
    top_ngrams = ngrams[:top_n]
    ngram_labels = [' '.join(gram) for gram, _ in top_ngrams]
    counts = [count for _, count in top_ngrams]

    plt.figure(figsize=(10, 5))
    plt.bar(ngram_labels, counts)
    plt.xlabel('N-grams')
    plt.ylabel('Counts')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, file_name))
    plt.show()


def generate_ngrams(reviews, n=2):
    ngram_counts = Counter()

    for review in reviews:
        words = review.split()
        ngram_counts.update(ngrams(words, n))

    return ngram_counts.most_common()


def plot_word_embeddings(embeddings_index, word_list, file_name="word_embeddings_plot.html"):
    # Extract vectors for the specified words
    vectors = [embeddings_index[word] for word in word_list if word in embeddings_index]
    two_dim = PCA().fit_transform(vectors)[:, :2]

    # Create a DataFrame for plotting
    df = pd.DataFrame(two_dim, columns=['x', 'y'])
    df['word'] = [word for word in word_list if word in embeddings_index]

    # Create interactive Plotly scatter plot
    fig = px.scatter(df, x='x', y='y', text='word', size_max=60,
                     title="Word Embeddings Visualization",
                     labels={'x': 'PCA Component 1', 'y': 'PCA Component 2'})

    # Update traces for better visibility
    fig.update_traces(textposition='top center', marker=dict(size=10))

    # Improve the layout
    fig.update_layout(title_font_size=22,
                      xaxis_title_font_size=18,
                      yaxis_title_font_size=18,
                      legend_title_font_size=18)

    # Save the figure as an HTML file
    fig.write_html(file_name)

    # Show the plot
    fig.show()


def load_glove_embeddings(path):
    embeddings_index = {}
    with open(path, encoding='utf-8') as file:
        for line in file:
            values = line.split()
            word = values[0]
            embeddings = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = embeddings
    return embeddings_index


def review_to_feature_vector(review, embeddings_index):
    words = review.split()
    word_count = 0
    feature_vector = np.zeros(300)  # Assuming GloVe vectors are of 300 dimensions
    for word in words:
        if word in embeddings_index:
            feature_vector += embeddings_index[word]
            word_count += 1
    if word_count > 0:
        feature_vector /= word_count
    return feature_vector


def plot_sentiment_scores(sentiment_scores, file_name="sentiment_distribution.png"):
    positive_scores = [score['pos'] for score in sentiment_scores]
    negative_scores = [score['neg'] for score in sentiment_scores]
    neutral_scores = [score['neu'] for score in sentiment_scores]

    plt.figure(figsize=(12, 6))
    plt.hist([positive_scores, negative_scores, neutral_scores], bins=50, label=['Positive', 'Negative', 'Neutral'])
    plt.xlabel('Scores')
    plt.ylabel('Number of Reviews')
    plt.title('Distribution of Sentiment Scores')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, file_name))
    plt.show()


def analyze_sentiment_vader(reviews):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for review in reviews:
        scores = analyzer.polarity_scores(review)
        sentiment_scores.append(scores)

    return sentiment_scores


def plot_sarcasm_detection(reviews, sarcastic_keywords, file_name="sarcasm_detection.png"):
    sarcasm_counts = {'Sarcastic': 0, 'Non-Sarcastic': 0}

    for review in reviews:
        if detect_sarcasm(review, sarcastic_keywords):
            sarcasm_counts['Sarcastic'] += 1
        else:
            sarcasm_counts['Non-Sarcastic'] += 1

    plt.figure(figsize=(6, 6))
    plt.pie(sarcasm_counts.values(), labels=sarcasm_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Sarcasm Detection in Reviews')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, file_name))
    plt.show()


def detect_sarcasm(text, sarcastic_keywords):
    words = text.split()
    for word in words:
        if word in sarcastic_keywords:
            return True
    return False


def plot_aspect_sentiment(aspect_sentiments, file_name="aspect_sentiment.png"):
    average_sentiments = {aspect: np.mean(sentiments) for aspect, sentiments in aspect_sentiments.items() if sentiments}

    # Sort aspects by sentiment score for better visualization
    sorted_aspects = dict(sorted(average_sentiments.items(), key=lambda item: item[1], reverse=True))

    # Determine the figure size dynamically based on the number of aspects
    fig_width = max(10, len(sorted_aspects) * 0.5)
    fig_height = 5
    plt.figure(figsize=(fig_width, fig_height))

    bars = plt.bar(sorted_aspects.keys(), sorted_aspects.values())

    # Rotate aspect labels to prevent overlap
    plt.xticks(rotation=45, ha="right")

    plt.xlabel('Aspect')
    plt.ylabel('Average Sentiment Score')
    plt.title('Aspect-Based Sentiment Analysis')

    # Add value labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()

    # Check if the output path exists, create if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    plt.savefig(os.path.join(output_path, file_name))
    plt.show()


def analyze_aspect_sentiment(reviews, aspect_keywords):
    analyzer = SentimentIntensityAnalyzer()
    aspect_sentiments = {aspect: [] for aspect in aspect_keywords}

    for review in reviews:
        for aspect in aspect_keywords:
            if aspect in review:
                score = analyzer.polarity_scores(review)
                aspect_sentiments[aspect].append(score['compound'])  # Using compound score for overall sentiment

    return aspect_sentiments


def main(cleaned_reviews_path):
    # Load the cleaned reviews data
    cleaned_reviews_df = pd.read_csv(cleaned_reviews_path)
    reviews = cleaned_reviews_df['text'].astype(str).tolist()

    # N-gram Analysis
    # bigrams = generate_ngrams(reviews, n=2)
    # plot_ngrams(bigrams, top_n=10, title="Top Bi-grams", file_name="bigram_plot.png")

    # trigrams = generate_ngrams(reviews, n=3)
    # plot_ngrams(trigrams, top_n=10, title="Top Tri-grams", file_name="trigram_plot.png")

    # Word Embeddings
    glove_path = get_path_from_root("data", "interim", "glove.6B.300d.txt")
    embeddings_index = load_glove_embeddings(glove_path)

    # Visualize Word Embeddings
    words_to_visualize = [
        'pasta', 'pizza', 'risotto', 'tiramisu', 'espresso', 'gelato', 'antipasto', 'prosciutto',
        'mozzarella', 'parmigiano', 'ricotta', 'gourmet', 'authentic', 'traditional', 'innovative',
        'atmosphere', 'cozy', 'romantic', 'family-friendly', 'casual', 'elegant', 'rustic', 'charming',
        'service', 'welcoming', 'attentive', 'professional', 'friendly', 'knowledgeable', 'slow',
        'affordable', 'expensive', 'value', 'overpriced', 'reasonable', 'portions', 'generous', 'hearty',
        'flavorful', 'savory', 'spicy', 'sweet', 'bitter', 'rich', 'creamy', 'crispy', 'tender',
        'fresh', 'local', 'seasonal', 'organic', 'imported', 'homemade', 'signature', 'recommend',
        'reservation', 'waitstaff', 'chef', 'sommelier', 'patio', 'view', 'ambience', 'decor',
        'cleanliness', 'hygiene', 'location', 'accessible', 'parking', 'reservations', 'booking',
        'wine', 'vineyard', 'pairing', 'appetizer', 'entree', 'dessert', 'course', 'cuisine',
        'dining', 'experience', 'review', 'rating', 'favorite', 'popular', 'crowded', 'quiet',
        'lively', 'noisy', 'intimate', 'exclusive', 'innovation', 'tradition', 'culture', 'heritage'
    ]

    plot_word_embeddings(embeddings_index, words_to_visualize)

    # Sentiment Analysis with VADER
    # sentiment_scores = analyze_sentiment_vader(reviews)
    # plot_sentiment_scores(sentiment_scores, file_name="sentiment_distribution.png")

    # Sarcasm Detection
    sarcastic_keywords = [
        'yeah right', 'sure', 'as if', 'oh great', 'really', 'wow', 'thanks a lot',
        'what a surprise', 'how nice', 'like I care', 'tell me about it', 'big deal',
        'so impressed', 'very helpful', 'what a joy', 'so excited', 'just what I wanted',
        'overjoyed', 'thrilled', 'fantastic'
    ]

    # plot_sarcasm_detection(reviews, sarcastic_keywords, file_name="sarcasm_detection.png")

    # Aspect-Based Sentiment Analysis
    aspect_keywords = [
        'food', 'service', 'ambiance', 'price', 'menu', 'location', 'cleanliness',
        'staff', 'atmosphere', 'quality', 'taste', 'presentation', 'variety',
        'portion', 'value', 'experience', 'comfort', 'decor', 'seating', 'wait time'
    ]

    # aspect_sentiments = analyze_aspect_sentiment(reviews, aspect_keywords)
    # plot_aspect_sentiment(aspect_sentiments, file_name="aspect_sentiment.png")


if __name__ == "__main__":
    path = get_path_from_root("data", "interim", "cleaned_reviews.csv")
    main(path)
