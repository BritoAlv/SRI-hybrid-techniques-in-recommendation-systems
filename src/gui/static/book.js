l = location.href.split("?")
book_title = decodeURIComponent(l[1].split("&")[0].split("=")[1])
book_id = l[1].split("&")[1].split("=")[1]
document.getElementById("title").innerHTML = book_title
rating = 0 
pages = 4
pagesArray = [] // para saber dado la pagina que botones pintar
for (let index = 0; index < pages; index++) {
  if (index == 0 && pages > 1) {
    pagesArray.push([false, true])
  }
  else {
    if (index == pages - 1  && pages > 1) {
      pagesArray.push([true, false])
    }
    else {
      pagesArray.push([true, true])
    }
  }
}
page = 1

shared = 0

const sendWithoutComment = async () => {
  data = {
    "user_id": parseInt(localStorage.getItem("user_id")),
    "comment": null,
    "rating": rating + 1,
    "read_ratio": page / pages * 100,
    "shared": shared,
    "book_id": parseInt(book_id)
  }
  try {
    a = await fetch(`http://127.0.0.1:5000/bookshelf/rating`, {
      'method': "POST",
      'headers': {
        'Content-Type': 'application/json',
      },
      'body': JSON.stringify(data)
    })
    if (a.status == 200) {

    }
  } catch (error) {
    console.log(error)
  } 
}

const sendWithComment = async () => {
  data = {
    "user_id": parseInt(localStorage.getItem("user_id")),
    "comment": document.getElementById("comment").value,
    "rating": rating + 1,
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
}

const loadStar = () => {  
  for (let i = 0; i < stars.length; i++) {
    const element = stars[i];
    if (rating < i) { 
      element.classList.remove("bi-star-fill")
      element.classList.add("bi-star")
    }
    else {
      element.classList.remove("bi-star")
      element.classList.add("bi-star-fill")
    }
  }
}

const setPage = () => {
  if (page > pages) {
    page = pages
  }
  if (pagesArray[page - 1][0] == false) {
    before.style.display = "none"
  }
  else {
    before.style.display = "block"
  }
  if (pagesArray[page - 1][1] == false) {
    next.style.display = "none"
  }
  else {
    next.style.display = "block"
  }
  if (page > pages) {
    page = pages
  }
  document.getElementById("page").innerHTML = page
  sendWithoutComment()
}

document.getElementById("send").addEventListener("click", async () => {
  if (document.getElementById("comment").value != "") {
    console.log(document.getElementById("comment").value  == "")
    sendWithComment()
    document.getElementById("last-comment").innerHTML = document.getElementById("comment").value 
    document.getElementById("comment").value = ""
  }
})

document.getElementById("share").addEventListener("click", () => {
  shared += 1
  sendWithoutComment()
})


next = document.getElementById("next")
before = document.getElementById("before")
next.addEventListener("click", () => {
  page += 1 
  setPage()
})
before.addEventListener("click", () => {
  page -= 1
  setPage()
})


stars = document.getElementsByClassName("star")
for (let index = 0; index < stars.length; index++) {
  const element = stars[index];
  element.addEventListener("click", (e) => {
    id = parseInt(e.target.id.split("-")[1])
    rating = id
    console.log(rating)
    loadStar()
    sendWithoutComment()
  })
}




fetchGet(`bookshelf/rating?user_id=${parseInt(localStorage.getItem("user_id"))}&book_id=${parseInt(book_id)}`, (d) => {
  rating = d.rating - 1
  page = d.read_ratio * pages / 100 
  document.getElementById("last-comment").innerHTML = d.comment
  loadStar()
  setPage()
}, e => {
  console.log(e)
})