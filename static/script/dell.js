function confirmarDeletar(url) {
    const resultado = confirm("Você tem certeza que deseja deletar isso?");
    if (resultado) {
        window.location.href = url; 
    }
    return false; 
}