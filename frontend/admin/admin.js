// Переключение вкладок
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        // Убираем активный класс у всех кнопок и контента
        document.querySelectorAll('.tab-button, .tab-content').forEach(element => {
            element.classList.remove('active');
        });

        // Добавляем активный класс к выбранной кнопке и контенту
        const tabId = button.getAttribute('data-tab');
        button.classList.add('active');
        document.getElementById(tabId).classList.add('active');

        // Загружаем данные для активной вкладки
        if (tabId === 'products') {
            loadProducts();
        } else if (tabId === 'stores') {
            loadStores();
        } else if (tabId === 'categories') {
            loadCategories();
        }
    });
});

// Загрузка продуктов
async function loadProducts() {
    const response = await fetch('http://localhost:8000/api/v1/products/');
    const products = await response.json();
    const productsList = document.getElementById('products-list');

    productsList.innerHTML = '';
    products.forEach(product => {
        const productItem = document.createElement('div');
        productItem.innerHTML = `
            <strong>${product.name}</strong><br>
            Описание: ${product.description}<br>
            Цена: ${product.price} руб.
            <button onclick="editProduct(${product.id})">Редактировать</button>
            <button onclick="deleteProduct(${product.id})">Удалить</button>
        `;
        productsList.appendChild(productItem);
    });
}

// Загрузка магазинов
async function loadStores() {
    const response = await fetch('http://localhost:8000/api/v1/stores/');
    const stores = await response.json();
    const storesList = document.getElementById('stores-list');

    storesList.innerHTML = '';
    stores.forEach(store => {
        const storeItem = document.createElement('div');
        storeItem.innerHTML = `
            <strong>${store.name}</strong><br>
            Адрес: ${store.address}, ${store.city}
            <button onclick="editStore(${store.id})">Редактировать</button>
            <button onclick="deleteStore(${store.id})">Удалить</button>
        `;
        storesList.appendChild(storeItem);
    });
}

// Загрузка категорий
async function loadCategories() {
    const response = await fetch('http://localhost:8000/api/v1/categories/');
    const categories = await response.json();
    const categoriesList = document.getElementById('categories-list');

    categoriesList.innerHTML = '';
    categories.forEach(category => {
        const categoryItem = document.createElement('div');
        categoryItem.innerHTML = `
            <strong>${category.name}</strong>
            <button onclick="editCategory(${category.id})">Редактировать</button>
            <button onclick="deleteCategory(${category.id})">Удалить</button>
        `;
        categoriesList.appendChild(categoryItem);
    });
}

// Загрузка данных при открытии страницы
document.addEventListener('DOMContentLoaded', () => {
    // По умолчанию активируем вкладку "Продукты"
    document.querySelector('.tab-button').click();
});