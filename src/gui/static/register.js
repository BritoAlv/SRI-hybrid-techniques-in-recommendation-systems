document.getElementById("form").addEventListener("submit", (e) => {
    e.preventDefault()
    fetchDefault("bookshelf/register", JSON.stringify({name: e.target.name.value, email: e.target.email.value}), "POST", (d) => {
        console.log(d.id)
        localStorage.setItem("user_id", d.id)
        location.href = "/survey"
    }, (e) => {
        console.log(e)
    })
})