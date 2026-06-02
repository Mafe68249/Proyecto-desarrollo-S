const API = "https://proyecto-desarrollo-s.onrender.com";

const formulario = document.getElementById("formKDrama");

formulario.addEventListener("submit", async function (e) {
    e.preventDefault();

    const kdrama = {
        nombre: document.getElementById("nombre").value,
        genero: document.getElementById("genero").value,
        nivel_emocional: parseInt(document.getElementById("nivel_emocional").value)
    };

    try {
        const response = await fetch(API + "/kdramas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(kdrama)
        });

        if (!response.ok) throw new Error("Error al crear kdrama");

        alert("K-Drama creado correctamente");

        formulario.reset();
        cargarKDramas();

    } catch (error) {
        console.error(error);
        alert("Error al crear K-Drama");
    }
});

async function cargarKDramas() {

    try {
        const response = await fetch(API + "/kdramas");
        const kdramas = await response.json();

        const tabla = document.getElementById("tablaKDramas");
        tabla.innerHTML = "";

        kdramas.forEach(k => {
            tabla.innerHTML += `
                <tr>
                    <td>${k.id}</td>
                    <td>${k.nombre}</td>
                    <td>${k.genero}</td>
                    <td>${k.nivel_emocional}</td>
                </tr>
            `;
        });

    } catch (error) {
        console.error(error);
    }
}

cargarKDramas();