<template>
  <div class="container mt-5">
    <h2 class="text-center">Login</h2>
    <form @submit.prevent="loginUser" class="mx-auto mt-4" style="max-width: 400px;">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          v-model="username"
          id="username"
          class="form-control"
          placeholder="Enter your username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
            type="password"
            v-model="password"
            id="password"
            class="form-control"
            placeholder="Enter your password"
            required
        />
      </div>
      <!-- Display error message -->
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-if="!isLoading">Login</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      isLoading: false, // Loading state to disable the button
      errorMessage: '' // Store error messages
    };
  },
  methods: {
    loginUser() {
      // Extract CSRF token from cookies
      const csrftoken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1];

      if (!csrftoken) {
        console.error('CSRF token not found');
        this.errorMessage = 'An error occurred. Please try again.';
        return;
      }

      // Validate the form before sending the request
      if (this.username && this.password) {
        this.isLoading = true; // Start loading

        axios.post('/api/login/', {
          username: this.username,
          password: this.password
        }, {
          headers: {'X-CSRFToken': csrftoken}
        })
            .then(response => {
              // Store the user info and authentication state
              localStorage.setItem('user', JSON.stringify(response.data.user));
              localStorage.setItem('isAuthenticated', 'true');

              // Redirect to the homepage
              this.$router.push('/');
            })
            .catch(error => {
              // Display error message from the backend
              if (error.response && error.response.data) {
                this.errorMessage = error.response.data.message || 'Login failed. Please check your credentials.';
              } else {
                this.errorMessage = 'Login failed. Please try again.';
              }
              console.error('Login error:', error.response);
            })
            .finally(() => {
              this.isLoading = false; // Stop loading
            });
      } else {
        this.errorMessage = 'Please enter both username and password.';
      }
    }
  }
};
</script>

<style scoped>
/* Optional: Adjust form width and layout for responsiveness */
.container {
  max-width: 600px;
}

.spinner-border-sm {
  margin-right: 5px;
}
</style>
