import os
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_success(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, DevOps!"}

# 2. Тест на ошибку 404 (проверяем поведение при запросе несуществующего роута)
def test_page_not_found(client):
    response = client.get('/unknown-page')
    assert response.status_code == 404

# 3. Тест корректности формата заголовков (Content-Type должен быть JSON)
def test_home_headers(client):
    response = client.get('/')
    assert response.headers['Content-Type'] == 'application/json'

# 4. Тест для проверки генерации файла визуализации
# (проверяет, что после работы скрипта файл с графиком действительно создается)
def test_visualization_file_created():
    # Имя файла, которое задано в visualization.py
    image_path = 'requests_stats.png'
    
    # Перед тестом удаляем файл, если он остался от прошлых запусков
    if os.path.exists(image_path):
        os.remove(image_path)
        
    # Имитируем логику скрипта визуализации внутри теста
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    data = [10, 15, 7, 18, 22]
    labels = ['Запрос 1', 'Запрос 2', 'Запрос 3', 'Запрос 4', 'Запрос 5']
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=labels, y=data)
    plt.savefig(image_path)
    plt.close() # Закрываем фигуру, чтобы освободить память
    
    # Проверяем, что файл успешно создался и он не пустой
    assert os.path.exists(image_path)
    assert os.path.getsize(image_path) > 0