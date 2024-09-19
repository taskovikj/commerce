<template>
  <div class="container mt-5">
    <h2 class="text-center">Register</h2>
    <form @submit.prevent="registerUser" class="mx-auto mt-4" style="max-width: 400px;">
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
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          v-model="email"
          id="email"
          class="form-control"
          placeholder="Enter your email"
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
      <div class="mb-3">
        <label for="confirmation" class="form-label">Confirm Password</label>
        <input
            type="password"
            v-model="confirmation"
            id="confirmation"
            class="form-control"
            placeholder="Confirm your password"
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
          <span v-if="!isLoading">Register</span>
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
      email: '',
      password: '',
      confirmation: '',
      isLoading: false, // Loading state to disable the button
      errorMessage: '' // Store error messages
    };
  },
  methods: {
    registerUser() {
      // Check if passwords match
      if (this.password !== this.confirmation) {
        this.errorMessage = "Passwords don't match!";
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';

      axios.post('/api/register/', {
        username: this.username,
        email: this.email,
        password: this.password,
        confirmation: this.confirmation
      })
          .then(() => {
            // On successful registration, redirect to homepage
            this.$router.push('/');
          })
          .catch(error => {
            // Handle registration errors and display the message
            if (error.response && error.response.data) {
              this.errorMessage = error.response.data.message || 'Registration failed. Please try again.';
            } else {
              this.errorMessage = 'Registration failed. Please try again.';
            }
          })
          .finally(() => {
            this.isLoading = false; // Stop loading
          });
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.spinner-border-sm {
  margin-right: 5px;
}
</style>
