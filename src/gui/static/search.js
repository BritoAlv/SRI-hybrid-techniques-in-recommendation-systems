getData = async () => {
    try {
        a = await fetch(`http://127.0.0.1:5000/bookshelf/search/${document.getElementById("query").value}`, {
            'method': "GET",
            'headers': {
                'Content-Type': 'application/json',
            },
        })
        a = await a.json()
        console.log(a)
        html = ""
        for (let index = 0; index < a.length; index++) {
          const element = a[index];
          console.log(element[0], element[1])
          html += `<div class="text-center product-father p-1 mt-2 col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2">
                <div class="  p-1  product ">
                    
                    <div class="card-body product-item">
                        <img loading="lazy" src="../static/book32.png" class="img-fluid w-100 rounded rounded-3 image" alt="">
                         
                    </div>
                    <div class="">  
                      <a href="/book?name=${element[0]}&id=${element[1]}" class="nav-link">${element[0]}</a>
                    </div>
                </div>
            </div>  `
        }
        document.getElementById("results").innerHTML = html
      } catch (error) {
        console.log(error)
      } 
}



document.getElementById("search").addEventListener("click", getData)