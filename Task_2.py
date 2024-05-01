import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
import matplotlib.pyplot as plt

def get_text(url):
    """Завантажує текст за вказаною URL-адресою."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None

def remove_punctuation(text):
    """Видаляє всю пунктуацію з тексту."""
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    """Виконує мапування для кожного слова."""
    return word, 1

def shuffle_function(mapped_values):
    """Виконує перемішування значень для кожного ключа."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    """Виконує редукцію для кожного ключа."""
    key, values = key_values
    return key, sum(values)

def map_reduce(text, search_words=None):
    """Виконує MapReduce для аналізу частоти використання слів у тексті."""
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ-слова з найвищою частотою використання."""
    top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 5))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Частота')
    plt.ylabel('Слова')
    plt.title('Топ-' + str(top_n) + ' найчастіше вживаних слів')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks06/0606641.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)  # Повний аналіз без обмеження пошуку
        print("Результат підрахунку слів:", result)
        visualize_top_words(result, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
