document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault()
    console.log(localStorage.getItem("user_id"), {
        user_id: localStorage.getItem("user_id"),
        genres: e.target.genres.value,
        authors: e.target.authors.value,
        time_periods: e.target.periods.value
    })
    data = {
        "user_id": 507,
        "genres": "eq",
        "authors": "e",
        "time_periods": [1, 2]
      }
    
      try {
        a = await fetch(`/bookshelf/features`, {
            'method': "POST",
            'headers': {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        location.href = "/"
      } catch (error) {
        console.log(error)
      } 
     
     
})