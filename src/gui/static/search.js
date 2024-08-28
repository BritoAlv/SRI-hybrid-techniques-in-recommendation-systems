getData = async () => {
    try {
        a = await fetch(`/bookshelf/search/${document.getElementById("query").value}`, {
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
          html += `<a href="/book?name=${element[0]}&id=${element[1]}">${element[0]}</a>`
        }
        document.getElementById("results").innerHTML = html
      } catch (error) {
        console.log(error)
      } 
}



document.getElementById("search").addEventListener("click", getData)