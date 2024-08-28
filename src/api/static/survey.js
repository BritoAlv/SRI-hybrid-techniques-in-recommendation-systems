document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault()
    console.log(localStorage.getItem("user_id"), {
        user_id: parseInt(localStorage.getItem("user_id")),
        genres: Array.from(document.querySelectorAll('#genres-container input:checked')).map(el => el.value),
        authors: Array.from(document.querySelectorAll('#authors-container input:checked')).map(el => el.value),
        time_periods: Array.from(document.querySelectorAll('#periods-container input:checked')).map(el => el.value),
    })
    data = {
      user_id: parseInt(localStorage.getItem("user_id")),
      genres: Array.from(document.querySelectorAll('#genres-container input:checked')).map(el => parseInt(el.value)),
      authors: Array.from(document.querySelectorAll('#authors-container input:checked')).map(el => parseInt(el.value)),
      time_periods: Array.from(document.querySelectorAll('#periods-container input:checked')).map(el => el.value),
      }
    
      try {
        a = await fetch(`/bookshelf/features`, {
            'method': "POST",
            'headers': {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        // location.href = "/"
      } catch (error) {
        console.log(error)
      } 
     
     
})








const form = document.getElementById('form');
const genresContainer = document.getElementById('genres-container');
const authorsContainer = document.getElementById('authors-container');

fetchGet('bookshelf/features', (data) => {
    renderCheckboxes(genresContainer, data.genres);
    renderCheckboxes(authorsContainer, data.authors);
}, (error) => {
    console.error('Error fetching features:', error);
});




renderCheckboxes = (container, options) => {
  options.forEach(option => {
      const checkbox = document.createElement('div');
      checkbox.innerHTML = `
          <input type="checkbox" id="feature-${option}" value="${option}">
          <label for="feature-${option}">${option}</label>
      `;
      container.appendChild(checkbox);
  });
}