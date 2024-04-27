const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('product_id');

axios.get(`http://localhost:8000/detail/?product_id=${productId}`)
.then((response)=>{
    const data = response.data;

    const detailDIV=document.getElementById('product-detail');

    detailDIV.innerHTML=`
        <img src="http://localhost:8000/getimage${data.photo}" 
            alt="${data.title}" 
            width=300px
            height=500px
        />
        <h2>${data.title}</h2>
        <p class="product-price">₩${data.price}</p>
        <p>재고 : ${data.stock}</p>
    `;
    console.log(response.data);
});