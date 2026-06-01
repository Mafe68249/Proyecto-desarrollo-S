const API = "https://proyecto-desarrollo-s.onrender.com";

const formulario = document.getElementById("formUsuario");

formulario.addEventListener("submit", async function (e) {

    e.preventDefault();

    const usuario = {
        nombre: document.getElementById("nombre").value,
        edad: parseInt(document.getElementById("edad").value)
    };

    try {

        const response = await fetch(API + "/usuarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(usuario)
        });

        if (!response.ok) {
            throw new Error("Error al crear usuario");
        }

        alert("Usuario creado correctamente");

        formulario.reset();

        cargarUsuarios();

    } catch (error) {

        console.error(error);
        alert("Error al crear usuario");

    }

});


async function cargarUsuarios() {

    try {

        const response = await fetch(API + "/usuarios");

        const usuarios = await response.json();

        const tabla = document.getElementById("tablaUsuarios");

        tabla.innerHTML = "";

        usuarios.forEach(function (usuario) {

            tabla.innerHTML +=
                "<tr>" +
                "<td>" + usuario.id + "</td>" +
                "<td>" + usuario.nombre + "</td>" +
                "<td>" + usuario.edad + "</td>" +
                "</tr>";

        });

    } catch (error) {

        console.error(error);

    }

}

cargarUsuarios();