(function () {
  const alfanumEspacios = /^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ ]+$/;

  function setError(input, msg) {
    const block = input.closest(".video-block");
    if (!block) return;
    const err = block.querySelector(".client-error");
    if (err) err.textContent = msg || "";
    input.style.borderColor = msg ? "rgba(255,91,110,.8)" : "rgba(255,255,255,.10)";
  }

  function validateInput(input) {
    const type = input.dataset.validate;
    const v = (input.value || "").trim();

    if (!v) {
      setError(input, "Error: Campo no puede estar vacío.");
      return false;
    }

    if (type === "alfanum") {
      if (!alfanumEspacios.test(v)) {
        setError(input, "Error: Campo debe ser alfanumérico (puede incluir espacios) sin símbolos.");
        return false;
      }
      setError(input, "");
      return true;
    }

    if (type === "tamano") {
      const n = Number(v);
      if (Number.isNaN(n)) {
        setError(input, "Error: Tamaño (MB) debe ser numérico.");
        return false;
      }
      if (n <= 0) {
        setError(input, "Error: Tamaño (MB) debe ser mayor que 0.");
        return false;
      }
      if (n > 3) {
        setError(input, "Error: Tamaño (MB) excede el máximo permitido (3MB).");
        return false;
      }
      setError(input, "");
      return true;
    }

    // si no tiene tipo, lo dejamos pasar
    setError(input, "");
    return true;
  }

  // Validar al salir del campo (blur)
  document.querySelectorAll("[data-validate]").forEach((inp) => {
    inp.addEventListener("blur", () => validateInput(inp));
  });

  // Confirmación emergente al guardar
  const form = document.getElementById("form-videos");
  const btn = document.getElementById("btn-guardar");
  if (form && btn) {
    form.addEventListener("submit", (e) => {
      let ok = true;
      document.querySelectorAll("[data-validate]").forEach((inp) => {
        if (!validateInput(inp)) ok = false;
      });

      if (!ok) {
        e.preventDefault();
        alert("Hay errores. Corrige los campos marcados antes de guardar.");
        return;
      }

      const confirmar = confirm("¿Deseas guardar estos videos en la Base de Datos?");
      if (!confirmar) {
        e.preventDefault();
      }
    });
  }
})();