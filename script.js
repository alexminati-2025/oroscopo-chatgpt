document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value;
  const data = document.getElementById("data").value;
  const ora = document.getElementById("ora").value;
  const luogo = document.getElementById("luogo").value;

  try {
    const response = await fetch("/oroscopo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, data, ora, luogo })
    });

    const result = await response.json();

    if (!response.ok) {
      // Se il server ha restituito un errore
      document.getElementById("risultato").innerHTML = `<p style="color:red;">Errore: ${result.error}</p>`;
      return;
    }

    document.getElementById("risultato").innerHTML = `
      <h2>${result.nome}</h2>
      <p><strong>Segno Solare:</strong> ${result.segno}</p>
      <p><strong>Ascendente:</strong> ${result.ascendente}</p>
      <p><strong>Luna:</strong> ${result.luna}</p>
      <p><strong>Tema Natale:</strong><br>${result.tema}</p>
      <p><strong>Oroscopo:</strong><br>${result.oroscopo}</p>
    `;
  } catch (err) {
    // Se c'è un errore nella fetch o parsing JSON
    document.getElementById("risultato").innerHTML = `<p style="color:red;">Errore nella richiesta: ${err.message}</p>`;
  }
});
