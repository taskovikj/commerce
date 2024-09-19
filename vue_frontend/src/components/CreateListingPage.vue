<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Create Listing</h1>

    <form @submit.prevent="createListing">
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input v-model="title" type="text" class="form-control" id="title" required />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea v-model="description" class="form-control" id="description" required></textarea>
      </div>

      <div class="mb-3">
        <label for="startingPrice" class="form-label">Starting Price</label>
        <input v-model="startingPrice" type="number" class="form-control" id="startingPrice" required />
      </div>

      <div class="mb-3">
        <label for="imageUrl" class="form-label">Image URL</label>
        <input v-model="imageUrl" type="url" class="form-control" id="imageUrl" />
      </div>

      <div class="mb-3">
        <label for="category" class="form-label">Category</label>
        <select v-model="category" class="form-control" id="category">
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>

      <button type="submit" class="btn btn-primary">Create Listing</button>
    </form>

    <!-- Display error message -->
    <div v-if="errorMessage" class="alert alert-danger mt-4">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      description: '',
      startingPrice: '',
      imageUrl: '',
      category: '',
      categories: [],
      errorMessage: ''
    };
  },
  mounted() {
    // Fetch categories for the select dropdown
    axios.get('/api/categories/')
        .then(response => {
          this.categories = response.data.categories;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
  },
 methods: {
  // Handle form submission to create a new listing
createListing() {
  const csrftoken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  const listingData = {
    title: this.title,
    description: this.description,
    starting_price: this.startingPrice,
    image_url: this.imageUrl,
    category: this.category
  };

  axios.post('/api/create_listing/', listingData, {
    headers: {
      'X-CSRFToken': csrftoken
    }
  })
    .then(() => {
      this.$router.push('/my-listings');
    })
    .catch(error => {
      this.errorMessage = error.response?.data?.message || 'Failed to create listing. Please try again.';
    });
}
}
};
</script>

<style scoped>
/* Basic styling */
form {
  max-width: 600px;
  margin: 0 auto;
}

button {
  display: block;
  width: 100%;
}
</style>
