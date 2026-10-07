document.querySelectorAll('label').forEach(label => {
    label.addEventListener('click',function() {
        document.querySelectorAll('.store-card').forEach(c => {
            c.classList.remove('select');
        });
        const card = this.querySelector('.store-card');
        if (card){
            card.classList.add('selected');
        }
    });
});
document.querySelectorAll('.store-radio:checked').forEach(radio => {
    const label = radio.closest('label');
    const card = label.querySelector('.store-card');
    if (card) {
        card.classList.add('selected');
    }
});