function indexImages() {
    const loader = document.getElementById("loader");
    const button = document.getElementById("index-button");
    const progress = document.getElementById("progress");

    // Show loader with animation
    loader.style.display = "flex";
    loader.style.opacity = "0";
    loader.style.transform = "translateY(10px)";
    loader.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    
    setTimeout(() => {
        loader.style.opacity = "1";
        loader.style.transform = "translateY(0)";
    }, 10);

    // Disable button with animation
    button.disabled = true;
    button.style.transform = "scale(0.95)";
    button.style.opacity = "0.7";
    
    // Show progress text
    progress.style.opacity = "1";
    progress.textContent = "Starting indexing process...";

    // Start the indexing process by making an AJAX request to the server
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/index", true);
    
    xhr.onprogress = function(event) {
        // Update progress if we get progress events
        if (event.lengthComputable) {
            const percentComplete = Math.round((event.loaded / event.total) * 100);
            progress.textContent = `Indexing... ${percentComplete}% completed`;
        }
    };
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Final completion state
                progress.innerHTML = '<span style="color:#38b000">✓ Indexing completed!</span>';
                
                // Hide loader with animation
                loader.style.opacity = "0";
                loader.style.transform = "translateY(-10px)";
                
                setTimeout(() => {
                    loader.style.display = "none";
                    
                    // Re-enable button with animation
                    button.disabled = false;
                    button.style.transform = "scale(1)";
                    button.style.opacity = "1";
                }, 300);
            } else {
                // Error handling
                progress.innerHTML = '<span style="color:#dc3545">✗ Error during indexing</span>';
                loader.style.display = "none";
                
                // Re-enable button
                button.disabled = false;
                button.style.transform = "scale(1)";
                button.style.opacity = "1";
            }
        }
    };
    
    xhr.send();
}

// Add event listener for when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add click animation to the index button
    const indexButton = document.getElementById('index-button');
    if (indexButton) {
        indexButton.addEventListener('click', function(e) {
            // Ripple effect
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.width = '10px';
            ripple.style.height = '10px';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.top = y + 'px';
            ripple.style.left = x + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }
});

// Add the ripple animation to the style sheet if not already present
if (!document.getElementById('ripple-animation-style')) {
    const style = document.createElement('style');
    style.id = 'ripple-animation-style';
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(15);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}