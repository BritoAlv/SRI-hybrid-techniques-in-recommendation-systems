console.log(location.href.split("?"))
l = location.href.split("?")
book_title = decodeURIComponent(l[1].split("&")[0].split("=")[1])
book_id = l[1].split("&")[1].split("=")[1]
document.getElementById("title").innerHTML = book_title
rating = 0

pages = 4
page = 1

shared = 0

document.getElementById("send").addEventListener("click", async () => {
    data = {
        "user_id": parseInt(localStorage.getItem("user_id")),
        "comment": document.getElementById("comment").value,
        "rating": rating,
        "read_ratio": page / pages * 100,
        "shared": shared,
        "book_id": parseInt(book_id)
      }
      console.log(data)
    try {
        a = await fetch(`http://127.0.0.1:5000/bookshelf/rating`, {
            'method': "POST",
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': JSON.stringify(data)
        })
        console.log(a)
        if (a.status == 200) {

        }
      } catch (error) {
        console.log(error)
      } 
})


document.getElementById("share").addEventListener("click", () => {
  shared += 1
})



next = document.getElementById("next")
before = document.getElementById("before")
next.addEventListener("click", () => {
  page += 1 
  console.log(page, pages)
  if (page == pages) {
    next.style.display = "none"
  }
  if (pages >= 2) {
    before.style.display = "block"
  }
})
before.addEventListener("click", () => {
  page -= 1
  console.log(page, pages)
  if (page == 1) {
    before.style.display = "none"
  }
  if (pages >= 2) {
    next.style.display = "block"
  }
})


stars = document.getElementsByClassName("star")
for (let index = 0; index < stars.length; index++) {
  const element = stars[index];
  element.addEventListener("click", (e) => {
    id = parseInt(e.target.id.split("-")[1])
    rating = id
    console.log(id)
    for (let i = 0; i < stars.length; i++) {
      const element = stars[i];
      if (id < i) {
      console.log(element)
        element.classList.remove("bi-star-fill")
        element.classList.add("bi-star")
      }
      else {
        element.classList.remove("bi-star")
        element.classList.add("bi-star-fill")
      }
    }
  })
}




 