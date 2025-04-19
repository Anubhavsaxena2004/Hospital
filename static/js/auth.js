/**
 * Authentication JavaScript
 * Handles form validation and other authentication-related functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password strength indicator
    const passwordInput = document.getElementById('id_password1');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strengthIndicator = document.getElementById('password-strength');
            
            if (strengthIndicator) {
                let strength = 0;
                let feedback = '';
                
                // Length check
                if (password.length >= 8) {
                    strength += 1;
                }
                
                // Contains number
                if (/\d/.test(password)) {
                    strength += 1;
                }
                
                // Contains lowercase
                if (/[a-z]/.test(password)) {
                    strength += 1;
                }
                
                // Contains uppercase
                if (/[A-Z]/.test(password)) {
                    strength += 1;
                }
                
                // Contains special character
                if (/[^A-Za-z0-9]/.test(password)) {
                    strength += 1;
                }
                
                // Update strength indicator
                switch(strength) {
                    case 0:
                    case 1:
                        strengthIndicator.className = 'progress-bar bg-danger';
                        strengthIndicator.style.width = '20%';
                        feedback = 'Very Weak';
                        break;
                    case 2:
                        strengthIndicator.className = 'progress-bar bg-warning';
                        strengthIndicator.style.width = '40%';
                        feedback = 'Weak';
                        break;
                    case 3:
                        strengthIndicator.className = 'progress-bar bg-info';
                        strengthIndicator.style.width = '60%';
                        feedback = 'Medium';
                        break;
                    case 4:
                        strengthIndicator.className = 'progress-bar bg-primary';
                        strengthIndicator.style.width = '80%';
                        feedback = 'Strong';
                        break;
                    case 5:
                        strengthIndicator.className = 'progress-bar bg-success';
                        strengthIndicator.style.width = '100%';
                        feedback = 'Very Strong';
                        break;
                }
                
                strengthIndicator.textContent = feedback;
            }
        });
    }
    
    // Password confirmation check
    const passwordConfirmInput = document.getElementById('id_password2');
    if (passwordConfirmInput && passwordInput) {
        passwordConfirmInput.addEventListener('input', function() {
            const password = passwordInput.value;
            const confirmPassword = this.value;
            const confirmFeedback = document.getElementById('password-confirm-feedback');
            
            if (confirmFeedback) {
                if (password === confirmPassword) {
                    confirmFeedback.className = 'text-success';
                    confirmFeedback.textContent = 'Passwords match';
                } else {
                    confirmFeedback.className = 'text-danger';
                    confirmFeedback.textContent = 'Passwords do not match';
                }
            }
        });
    }
    
    // Role-based field visibility
    const roleSelect = document.getElementById('id_role');
    const specializationField = document.getElementById('id_specialization').closest('.mb-3');
    
    if (roleSelect && specializationField) {
        // Initial check
        if (roleSelect.value !== 'DOCTOR') {
            specializationField.style.display = 'none';
        }
        
        // Change event
        roleSelect.addEventListener('change', function() {
            if (this.value === 'DOCTOR') {
                specializationField.style.display = 'block';
            } else {
                specializationField.style.display = 'none';
            }
        });
    }
    
    // Remember me functionality
    const rememberMeCheckbox = document.getElementById('id_remember_me');
    if (rememberMeCheckbox) {
        // Check if there's a saved username
        const savedUsername = localStorage.getItem('rememberedUsername');
        if (savedUsername) {
            document.getElementById('id_username').value = savedUsername;
            rememberMeCheckbox.checked = true;
        }
        
        // Save username on form submission
        const loginForm = rememberMeCheckbox.closest('form');
        if (loginForm) {
            loginForm.addEventListener('submit', function() {
                if (rememberMeCheckbox.checked) {
                    localStorage.setItem('rememberedUsername', document.getElementById('id_username').value);
                } else {
                    localStorage.removeItem('rememberedUsername');
                }
            });
        }
    }
}); 