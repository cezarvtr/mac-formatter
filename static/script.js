function mostrarToast(){
    const toast = document.getElementById("toast");
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 1500);
}

function copiarTexto(texto){
    if (navigator.clipboard) {
        navigator.clipboard.writeText(texto)
        .then(() => mostrarToast())
        .catch(() => fallbackCopy(texto));
    } else {
        fallbackCopy(texto);
    }
}

function fallbackCopy(texto){
    const input = document.createElement("input");
    input.value = texto;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
    mostrarToast();
}
