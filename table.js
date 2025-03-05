// Check the status of each data cell in a table

const table = document.getElementById('table1');
console.log(table.length);
console.log(11);
const cells = table.getElementsByTagName('td');
console.log(cells);
for (const cell of cells) {
  const status = cell.getAttribute("data-status");
  console.log(1)
    // Grab the data
}