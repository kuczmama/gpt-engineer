window.addEventListener('DOMContentLoaded', (event) => {
  const table = document.getElementById('rosterTable');
  
  if (table) {
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) { // Skip the header row
      const row = rows[i];
      
      if (row) {
        row.addEventListener('click', () => {
          const cells = row.getElementsByTagName('td');
          const name = cells[0]?.textContent || '';
          const contactInfo = cells[1]?.textContent || '';
          alert(`Name: ${name}\nContact Info: ${contactInfo}`);
        });
      }
    }
  }
});