// Enhanced input focus effects
document.querySelectorAll("input").forEach(input => {
    input.addEventListener("focus", () => {
        input.style.border = "2px solid #667eea";
        input.style.transform = "scale(1.02)";
    });
    
    input.addEventListener("blur", () => {
        input.style.border = "1px solid #ccc";
        input.style.transform = "scale(1)";
    });
    
    // Add typing animation
    input.addEventListener("input", () => {
        input.style.boxShadow = "0 0 0 3px rgba(102, 126, 234, 0.1)";
        setTimeout(() => {
            input.style.boxShadow = "";
        }, 300);
    });
});

// Form submission animation
document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", (e) => {
        const button = form.querySelector("button");
        if (button) {
            button.style.transform = "scale(0.95)";
            button.textContent = "Processing...";
        }
    });
});

// Welcome page animations
document.addEventListener("DOMContentLoaded", () => {
    // Add floating animation to welcome elements
    const welcomeCard = document.querySelector(".welcome-card");
    if (welcomeCard) {
        // Create floating particles
        for (let i = 0; i < 20; i++) {
            createParticle();
        }
    }
    
    // Add click ripple effect to logout button
    const logoutBtn = document.querySelector(".logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function(e) {
            const ripple = document.createElement("span");
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + "px";
            ripple.style.left = x + "px";
            ripple.style.top = y + "px";
            ripple.classList.add("ripple");
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }
});

// Create floating particles
function createParticle() {
    const particle = document.createElement("div");
    particle.style.position = "absolute";
    particle.style.width = Math.random() * 5 + 2 + "px";
    particle.style.height = particle.style.width;
    particle.style.background = "rgba(255, 255, 255, 0.6)";
    particle.style.borderRadius = "50%";
    particle.style.left = Math.random() * 100 + "%";
    particle.style.top = Math.random() * 100 + "%";
    particle.style.pointerEvents = "none";
    particle.style.animation = `float ${Math.random() * 3 + 2}s ease-in-out infinite`;
    particle.style.animationDelay = Math.random() * 2 + "s";
    
    document.body.appendChild(particle);
    
    setTimeout(() => {
        particle.remove();
    }, 5000);
}

// Add floating animation
const style = document.createElement("style");
style.textContent = `
    @keyframes float {
        0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) translateX(20px);
            opacity: 0;
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Error message display
if (document.querySelector(".error")) {
    const errorMsg = document.querySelector(".error");
    setTimeout(() => {
        errorMsg.style.animation = "fadeOut 0.5s ease-out forwards";
    }, 5000);
}

// Add fadeOut animation
const fadeOutStyle = document.createElement("style");
fadeOutStyle.textContent = `
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(fadeOutStyle);