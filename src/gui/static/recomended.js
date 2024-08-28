getData = async () => {
    try {
        a = await fetch(`/bookshelf/recommend/${localStorage.getItem("user_id")}`, {
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
          html += `<p>${element}</p>`
        }
        document.getElementById("results").innerHTML = html
      } catch (error) {
        console.log(error)
      } 
}

getData()