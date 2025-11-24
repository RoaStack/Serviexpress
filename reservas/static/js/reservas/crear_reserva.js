document.addEventListener("DOMContentLoaded", function() {
    const fechaInput = document.querySelector("#id_fecha");
    const horaSelect = document.querySelector("#id_hora");

    fechaInput.addEventListener("change", function() {
        const fecha = this.value;
        horaSelect.innerHTML = '<option value="">Cargando horas disponibles...</option>';
        horaSelect.disabled = true;

        fetch(`/reservas/horas_disponibles/?fecha=${fecha}`)
            .then(response => response.json())
            .then(data => {
                horaSelect.innerHTML = "";
                horaSelect.disabled = false;

                if (data.horas && data.horas.length > 0) {
                    data.horas.forEach(hora => {
                        const option = document.createElement("option");
                        option.value = hora;
                        option.textContent = `🕓 ${hora}`;
                        horaSelect.appendChild(option);
                    });
                } else {
                    horaSelect.innerHTML = '<option value="">No hay horas disponibles</option>';
                }
            })
            .catch(() => {
                horaSelect.innerHTML = '<option value="">Error al cargar horas</option>';
                horaSelect.disabled = false;
            });
    });
});
