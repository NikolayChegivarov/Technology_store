// Загрузка филиалов
async function loadBranches() {
    const response = await fetch('http://localhost:8000/api/v1/stores/');  // Путь к API
    const branches = await response.json();
    const branchesList = document.getElementById('branches-list');

    branches.forEach(branch => {
        const branchItem = document.createElement('div');
        branchItem.className = 'branch-item';
        branchItem.innerHTML = `
            <strong>${branch.name}</strong><br>
            Адрес: ${branch.address}, ${branch.city}
        `;
        branchesList.appendChild(branchItem);
    });
}

// Загрузка товаров
async function loadProducts() {
    const response = await fetch('http://localhost:8000/api/v1/products/');  // Путь к API
    const products = await response.json();
    const productsList = document.getElementById('products-list');

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <strong>${product.name}</strong><br>
            Описание: ${product.description}<br>
            Цена: ${product.price} руб.
        `;
        productsList.appendChild(productCard);
    });
}

// Вызов функций загрузки
if (window.location.pathname.includes('branches.html')) {
    loadBranches();
}

if (window.location.pathname.includes('showcase.html')) {
    loadProducts();
}