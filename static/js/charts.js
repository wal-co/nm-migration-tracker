let allData = {}

fetch("/api/observations")
    .then(response => response.json())
    .then(data => {
      allData = data
      renderBarChart(data)
    })

document.getElementById("species-search").addEventListener("input", applyFilters)
document.getElementById("family-search").addEventListener("input", applyFilters)

function applyFilters() {
  const nameSearch = document.getElementById("species-search").value.toLowerCase()
  const familySearch = document.getElementById("family-search").value.toLowerCase()

  const filtered = Object.fromEntries(
    Object.entries(allData).filter(([species, bird]) => {
      const matchesName = bird.common_name.toLowerCase().includes(nameSearch)
      const matchesFamily = bird.family.toLowerCase().includes(familySearch)
      return matchesName && matchesFamily
    })
  )

  renderBarChart(filtered)
}

function renderBarChart(data) {
  const container = document.getElementById("bar-view")
  container.innerHTML = ""
  const months = [
    "January", 
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"]

  //Create header
  const header = document.createElement("div")
  header.className = "month-header"
  header.innerHTML = `<div class="species-name"></div>` + 
    months.map(m => `<div class="month-label">${m}</div>`).join("")
  
  container.appendChild(header)

  //Create species rows
  for (const [species, bird] of Object.entries(data)) {
    const row = document.createElement("div")
    row.className = "bar-row"
    row.innerHTML = row.innerHTML = `<a href="https://ebird.org/species/${bird.species_code}" target="_blank" class="species-name">${bird.common_name}</a>` +        // loop through 1-12, create a cell for each month
      Array.from({length: 12}, (_, i) => i + 1)
        .map(month => bird.months.includes(month) ? 
          `<div class="month-cell present"></div>` : 
          `<div class="month-cell"></div>`)
        .join("")
    container.appendChild(row)
}

}
