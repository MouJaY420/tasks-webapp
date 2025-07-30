document.addEventListener("DOMContentLoaded", function () {
    const editables = document.querySelectorAll(".editable");

    editables.forEach(el => {
      const inputId = el.dataset.inputId;
      const hiddenInput = document.getElementById(inputId);

      // Initialize editable div with input value (if any)
      if (hiddenInput && hiddenInput.value) {
        el.textContent = hiddenInput.value;
      }

      // On blur, update hidden input with current value
      el.addEventListener("input", () => {
        if (hiddenInput) {
          hiddenInput.value = el.textContent;
        }
      });
    });
  });