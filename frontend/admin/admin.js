// Переменные для модального окна
const deleteModal = document.getElementById('delete-modal');
const confirmDeleteBtn = document.getElementById('confirm-delete');
const cancelDeleteBtn = document.getElementById('cancel-delete');
let currentId = null;
let entityType = null;

// Функция открытия модального окна
function openDeleteModal(id, entityName, type) {
    currentId = id;
    entityType = type;
    document.getElementById('delete-message').textContent =
        `Вы уверены, что хотите удалить ${entityName}?`;
    deleteModal.style.display = 'block';
}

// Функция закрытия модального окна
function closeDeleteModal() {
    deleteModal.style.display = 'none';
    currentId = null;
    entityType = null;
}

// Обработчик удаления
async function handleDelete() {
    try {
        const url = `http://localhost:8000/api/v1/${entityType}/${currentId}/`;

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка удаления: ${response.statusText}`);
        }

        // Перезагружаем данные после успешного удаления
        switch(entityType) {
            case 'products':
                loadProducts();
                break;
            case 'stores':
                loadStores();
                break;
            case 'categories':
                loadCategories();
                break;
        }

        closeDeleteModal();
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
    }
}

// Обновляем существующие функции загрузки данных
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
            <button onclick="openDeleteModal(${product.id}, '${product.name}', 'products')">Удалить</button>
        `;
        productsList.appendChild(productItem);
    });
}

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
            <button onclick="openDeleteModal(${store.id}, '${store.name}', 'stores')">Удалить</button>
        `;
        storesList.appendChild(storeItem);
    });
}

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
            <button onclick="openDeleteModal(${category.id}, '${category.name}', 'categories')">Удалить</button>
        `;
        categoriesList.appendChild(categoryItem);
    });
}

// Добавляем обработчики событий для модального окна
confirmDeleteBtn.addEventListener('click', handleDelete);
cancelDeleteBtn.addEventListener('click', closeDeleteModal);

// Закрываем модальное окно при клике вне его области
deleteModal.addEventListener('click', (e) => {
    if (e.target === deleteModal) {
        closeDeleteModal();
    }
});