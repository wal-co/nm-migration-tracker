fetch("/api/observations")
    .then(response => response.json())
    .then(data => {
        renderBarChart(data)
    })

function renderBarChart(data) {
  const container = document.getElementById("bar-view")
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
  for (const [species, presentMonths] of Object.entries(data)) {
    const row = document.createElement("div")
    row.className = "bar-row"
    row.innerHTML = `<div class="species-name">${species}</div>` +
        // loop through 1-12, create a cell for each month
      Array.from({length: 12}, (_, i) => i + 1)
        .map(month => presentMonths.includes(month) ? 
          `<div class="month-cell present"></div>` : 
          `<div class="month-cell"></div>`)
        .join("")
    container.appendChild(row)
}

}
