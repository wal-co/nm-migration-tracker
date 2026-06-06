let allData = {}
let selectedFamilies = new Set()
let selectedMonth = 0

fetch("/api/observations")
    .then(response => response.json())
    .then(data => {
      allData = data
      renderBarChart(data)
      populateFamilyPills(allData)
      populateMonthPills()
    })

document.getElementById("species-search").addEventListener("input", applyFilters)
// document.getElementById("family-search").addEventListener("input", applyFilters)
// document.getElementById("month-filter").addEventListener("change", applyFilters)
const month_pills = document.getElementById("month-pills")
document.getElementById("month-toggle").addEventListener("click", () => {
  if (month_pills.style.display === "none") {
    month_pills.style.display = "block" // show
  } else {
    month_pills.style.display = "none" // hide
  }
})

const family_pills = document.getElementById("family-pills")
document.getElementById("family-toggle").addEventListener("click", () => {
    if (family_pills.style.display === "none") {
    family_pills.style.display = "block" // show
  } else {
    family_pills.style.display = "none" // hide
  }
}) 

function applyFilters() {
  const nameSearch = document.getElementById("species-search").value.toLowerCase()
  // const familySearch = document.getElementById("selectedFamily").value.toLowerCase()
  // const monthSearch = parseInt(document.getElementById("month-filter").value)

  const filtered = Object.fromEntries(
    Object.entries(allData).filter(([species, bird]) => {
      const matchesName = bird.comName.toLowerCase().includes(nameSearch)
      // const matchesFamily = bird.family.toLowerCase().includes(familySearch)
      const matchesFamily = selectedFamilies.size === 0 || selectedFamilies.has(bird.family)
      let matchesMonth = false
      if (selectedMonth === 0) { matchesMonth = true}
      else { matchesMonth = bird.months.includes(selectedMonth) }
      return matchesName && matchesFamily && matchesMonth
    })
  )
  if (Object.keys(filtered).length === 0) {
    document.getElementById("bar-view").innerHTML = "<p>No species matched your search.</p>"
    return
  }

  renderBarChart(filtered)
}

function populateFamilyPills(data) {
  const families = [... new Set(Object.values(data).map(bird => bird.family))].sort()
  const container = document.getElementById("family-pills")
  container.innerHTML = families.map(family => 
    `<button class="family-pill" data-family="${family}">${family}</button>`
  ).join("")

  container.querySelectorAll(".family-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      if (selectedFamilies.has(pill.dataset.family)) {
        selectedFamilies.delete(pill.dataset.family)
      } else {
        selectedFamilies.add(pill.dataset.family)
      }
      pill.classList.toggle("active")
      applyFilters()
    })
  })
}

function populateMonthPills() {
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
  const container = document.getElementById("month-pills")
  container.innerHTML = months.map( (month, i) => 
    `<button class="month-pill" data-month="${i+1}">${month}</button>`
  ).join("")

  container.querySelectorAll(".month-pill").forEach(pill => {
      pill.addEventListener("click", () => {selectedMonth = parseInt(pill.dataset.month) === selectedMonth ? 0 : parseInt(pill.dataset.month)
      document.querySelectorAll(".month-pill").forEach(p => p.classList.remove("active"))
      if (selectedMonth) pill.classList.add("active")
      applyFilters()
    })
  })
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
    row.innerHTML = row.innerHTML = `<a href="https://ebird.org/species/${bird.speciesCode}" target="_blank" class="species-name">${bird.comName}</a>` +        // loop through 1-12, create a cell for each month
      Array.from({length: 12}, (_, i) => i + 1)
        .map(month => bird.months.includes(month) ? 
          `<div class="month-cell present"></div>` : 
          `<div class="month-cell"></div>`)
        .join("")
    container.appendChild(row)
}

}
