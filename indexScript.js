function renderProducts(products) {
    const productList = document.getElementById('product-list');

    products.forEach(product => {
        productList.innerHTML += `
        <li class="product">
            <img
                src="http://localhost:8000/getimage${product.photo}"
                alt="Product 1"
                width=300px
                height=500px
             />
            <h3>${product.title}</h3>
            <p class="product-price">₩${product.price}</p>
            <form action="./product_detail.html" method="GET">
                <input type="hidden" name="product_id" value="${product.id}" />
                <input type="submit" value="더보기" />
            </form>
      </li>
        `;
    });
}


axios.get("http://localhost:8000/example/")
    .then(response => {
        renderProducts(response.data);
        console.log(response)
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });