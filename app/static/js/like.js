function likeBook(bookId) {
    const likeButton = document.getElementById(`like-button-${bookId}`);
    const likeCount = document.getElementById(`like-count-${bookId}`);

    fetch(`/like/${bookId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.liked) {
            likeButton.textContent = "Unlike"; // Change button text to "Unlike"
        } else {
            likeButton.textContent = "Like"; // Change button text to "Like"
        }
        likeCount.textContent = data.likes_count; // Update like count
    })
    .catch(error => console.error('Error:', error));
}
