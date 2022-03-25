document.querySelectorAll('.div-principal img').forEach(el => {
    el.addEventListener("click", function(ev){
        ev.stopPropagation();
        this.parentNode.classList.add('active');    
}) 
});
document.querySelectorAll('.div-principal').forEach(el => {
    el.addEventListener("click", function(ev){
        this.classList.remove('active');
        console.log("click"); 
}) 
})




/*
    const ruta = elemento.getAttribute('src');
    console.log('ruta')
    elemento.addEventListener('click', () => {
        overlay.classList.add('activo');
        document.querySelector('#overlay .contenedor-overlay img').src = ruta;
    });
});
document.querySelector('#btn-cerrar-popup').addEventListener('click', () => {
    overlay.classList.remove('activo');

});*/