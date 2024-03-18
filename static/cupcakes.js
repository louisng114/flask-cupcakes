cupcakeList = document.querySelector("#cupcakeList");
flavorInput = document.querySelector("#flavor");
sizeInput = document.querySelector("#size");
ratingInput = document.querySelector("#rating");
imageInput = document.querySelector("#image");
submitBtn = document.querySelector("#submitBtn");

submitBtn.addEventListener("click", (evt) => {
    evt.preventDefault();
    addCupcake();
});

const addCupcake = async () => {
    flavor = flavorInput.value;
    size = sizeInput.value;
    rating = ratingInput.value;
    image = imageInput.value;

    await axios.post("/api/cupcakes", {
        flavor : flavor,
        size : size,
        rating : rating,
        image : image
        })
    
    new_li = document.createElement("li");
    new_li.innerHTML = `<img src="${image}}" height="200">
                        ${flavor}`

    cupcakeList.append(new_li);

    flavorInput.value = "";
    sizeInput.value = "";
    ratingInput.value = "";
    imageInput.value = "";
};
