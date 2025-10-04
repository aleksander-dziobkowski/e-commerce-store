const minSlider = document.getElementById('priceRangeMin');
const maxSlider = document.getElementById('priceRangeMax');
const minPriceVal = document.getElementById('minPriceVal');
const maxPriceVal = document.getElementById('maxPriceVal');
const toggleBtn = document.getElementById('priceFilterToggle');
const filterBox = document.getElementById('priceFilterBox');

if (minSlider && maxSlider) {
minSlider.addEventListener('input', () => {
    minPriceVal.textContent = minSlider.value;
});

maxSlider.addEventListener('input', () => {
    maxPriceVal.textContent = maxSlider.value;
});
}

if (toggleBtn && filterBox) {
toggleBtn.addEventListener('click', () => {
    filterBox.style.display = (filterBox.style.display === 'none' || filterBox.style.display === '') ? 'block' : 'none';
});

document.addEventListener('click', (e) => {
    if (!toggleBtn.contains(e.target) && !filterBox.contains(e.target)) {
    filterBox.style.display = 'none';
    }
});
}

document.getElementById('sortToggle').addEventListener('click', function() {
const box = document.getElementById('sortBox');
box.style.display = box.style.display === 'block' ? 'none' : 'block';
document.getElementById('priceFilterBox').style.display = 'none';
});
