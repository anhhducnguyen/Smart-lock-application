// Access the camera
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const photo = document.getElementById('photo');
const imageDataInput = document.getElementById('image_data');
const nameInput = document.getElementById('name');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    });

// Capture the photo
document.getElementById('capture').addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');
    photo.src = imageData;
    imageDataInput.value = imageData;
});

// Handle form submission via AJAX
document.getElementById('photoForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    formData.append('name', nameInput.value);  // Add name to form data

    fetch('', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Image uploaded successfully! URL: ' + data.image_url);
        } else {
            alert('Error: ' + data.message);
        }
    });
});