const thumbsContainer = document.getElementById('thumbsContainer');
const scrollUpBtn = document.getElementById('scrollUpBtn');
const scrollDownBtn = document.getElementById('scrollDownBtn');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function updateButtonsVisibility() {
// Jeśli da się przewinąć w górę (scrollTop > 0)
if (thumbsContainer.scrollTop > 0) {
    scrollUpBtn.style.display = 'block';
} else {
    scrollUpBtn.style.display = 'none';
}

// Jeśli da się przewinąć w dół (scrollTop + offsetHeight < scrollHeight)
if (thumbsContainer.scrollTop + thumbsContainer.offsetHeight < thumbsContainer.scrollHeight) {
    scrollDownBtn.style.display = 'block';
} else {
    scrollDownBtn.style.display = 'none';
}
}

// Aktualizuj widoczność przy starcie
updateButtonsVisibility();

// Aktualizuj przy scrollowaniu myszką
thumbsContainer.addEventListener('scroll', updateButtonsVisibility);

scrollUpBtn.addEventListener('click', () => {
thumbsContainer.scrollBy({ top: -100, behavior: 'smooth' });
});

scrollDownBtn.addEventListener('click', () => {
thumbsContainer.scrollBy({ top: 100, behavior: 'smooth' });
});

const thumbnails = document.querySelectorAll('.thumb-preview');
const mainImage = document.getElementById('mainImage');

thumbnails.forEach(thumb => {
    thumb.addEventListener('click', () => {
        mainImage.src = thumb.src;
    });
});

const likeBtn = document.getElementById('like-btn');
const heartIcon = document.getElementById('heart-icon');

// Na starcie ustaw ikonę w zależności od stanu
if (likeBtn.classList.contains('liked')) {
    heartIcon.classList.add('bi-heart-fill');
    heartIcon.style.color = 'red';
} else {
    heartIcon.classList.add('bi-heart');
    heartIcon.style.color = '';
}

likeBtn.addEventListener('click', function() {
const productId = this.dataset.productId;
const url = this.dataset.likeUrl;

fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    credentials: 'same-origin',
})
.then(response => {
    if (response.redirected) {
        // Django przekierowało na login
        window.location.href = response.url;
        return;
    }

    if (response.status === 401) {
        window.location.href = `store/accounts/login/?next=${window.location.pathname}`;
        return;
    }

    if (!response.ok) {
        throw new Error('Server error');
    }

    return response.json();
})

.then(data => {
    if (!data) return; // jeśli przekierowano, przerwij

    if(data.liked){
        likeBtn.classList.add('liked');
        heartIcon.classList.remove('bi-heart');
        heartIcon.classList.add('bi-heart-fill');
        heartIcon.style.color = 'red';
    } else {
        likeBtn.classList.remove('liked');
        heartIcon.classList.remove('bi-heart-fill');
        heartIcon.classList.add('bi-heart');
        heartIcon.style.color = '';
    }
})
.catch(error => {
    console.error('Błąd:', error);
    alert('Something went wrong with liking.');
});
});



// Inicjalizuj wszystkie toasty
document.addEventListener('DOMContentLoaded', function () {
var toastElList = [].slice.call(document.querySelectorAll('.toast'))
toastElList.map(function (toastEl) {
    var toast = new bootstrap.Toast(toastEl)
    toast.show()
})
});
