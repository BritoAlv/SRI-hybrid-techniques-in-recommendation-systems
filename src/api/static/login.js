document.getElementById("form").addEventListener("submit", (e) => {
    e.preventDefault()
    console.log(e.target.email.value)
    fetchDefault("bookshelf/login", JSON.stringify({email: e.target.email.value}), "POST", (d) => {
        console.log(d)
        localStorage.setItem("user_id", d.id)
        location.href = "/"
    }, (e) => {
        console.log(e)
    })
})