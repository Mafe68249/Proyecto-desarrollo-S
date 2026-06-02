const API = window.location.origin;

const form = document.getElementById("formPersonalidad");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        id_usuario: parseInt(document.getElementById("id_usuario").value),
        romantico: document.getElementById("romantico").checked,
        aventurero: document.getElementById("aventurero").checked,
        sensible: document.getElementById("sensible").checked,
        extrovertido: document.getElementById("extrovertido").checked,
        oscuro: document.getElementById("oscuro").checked,
        intenso: document.getElementById("intenso").checked,
    };

    try {
        const res = await fetch(API + "/personalidad", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error();

        alert("Personalidad guardada");
        form.reset();
        cargarPersonalidades();

    } catch (err) {
        console.error(err);
        alert("Error al guardar");
    }
});

async function cargarPersonalidades() {

    try {
        const res = await fetch(API + "/personalidad");
        const data = await res.json();

        const tabla = document.getElementById("tablaPersonalidad");
        tabla.innerHTML = "";

        data.forEach(p => {
            tabla.innerHTML += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.id_usuario}</td>
                    <td>${p.romantico ? "✔" : ""}</td>
                    <td>${p.aventurero ? "✔" : ""}</td>
                    <td>${p.sensible ? "✔" : ""}</td>
                    <td>${p.extrovertido ? "✔" : ""}</td>
                    <td>${p.oscuro ? "✔" : ""}</td>
                    <td>${p.intenso ? "✔" : ""}</td>
                </tr>
            `;
        });

    } catch (err) {
        console.error(err);
    }
}

cargarPersonalidades();