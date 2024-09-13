(function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');

    // Truy cập webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Lỗi khi truy cập webcam: ", err);
        });

    // Hàm để lấy CSRF token từ thẻ meta
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    // Chụp ảnh và gửi lên server
    captureButton.addEventListener('click', () => {
        const name = document.getElementById('name').value;
        if (!name) {
            alert("Vui lòng nhập tên!");
            return;
        }

        // Chụp ảnh từ video
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Lấy dữ liệu ảnh từ canvas
        const imageData = canvas.toDataURL('image/png');

        // Lấy CSRF token
        const csrfToken = getCSRFToken();

        // Gửi ảnh lên server qua AJAX
        fetch('/capture/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken  // Thêm CSRF token vào header
            },
            body: `name=${encodeURIComponent(name)}&image=${encodeURIComponent(imageData)}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Lỗi khi gửi ảnh:', error);
        });
    });
})();
(function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');

    // Truy cập webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Lỗi khi truy cập webcam: ", err);
        });

    // Hàm để lấy CSRF token từ thẻ meta
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    // Chụp ảnh và gửi lên server
    captureButton.addEventListener('click', () => {
        const name = document.getElementById('name').value;
        if (!name) {
            alert("Vui lòng nhập tên!");
            return;
        }

        // Chụp ảnh từ video
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Lấy dữ liệu ảnh từ canvas
        const imageData = canvas.toDataURL('image/png');

        // Lấy CSRF token
        const csrfToken = getCSRFToken();

        // Gửi ảnh lên server qua AJAX
        fetch('/capture/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken  // Thêm CSRF token vào header
            },
            body: `name=${encodeURIComponent(name)}&image=${encodeURIComponent(imageData)}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Lỗi khi gửi ảnh:', error);
        });
    });
})();

