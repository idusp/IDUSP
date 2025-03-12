async function sendData() {
    const csrftoken = getCookie('csrftoken');  // Cookie se CSRF token le raha hai

    const response = await fetch('/api/my-endpoint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // CSRF token bhejna zaroori hai
        },
        body: JSON.stringify({ "name": "Test User" })
    });

    const data = await response.json();
    console.log(data);
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
