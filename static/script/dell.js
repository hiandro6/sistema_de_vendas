function confirmarDeletar(url) {
    const resultado = confirm("Você tem certeza que deseja deletar isso?");
    if (resultado) {
        window.location.href = url; // Redireciona para a URL de remoção
    }
    return false; // Impede o link de ser seguido imediatamente
}