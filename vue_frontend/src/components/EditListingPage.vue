<template>
  <div class="container my-5">
    <h2 class="text-center mb-4">Edit Listing</h2>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex justify-content-center align-items-center vh-100">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Form for editing the listing -->
    <form @submit.prevent="updateListing" v-if="!loading">
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input
          type="text"
          id="title"
          v-model="title"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          id="description"
          v-model="description"
          class="form-control"
          rows="4"
          required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="startingPrice" class="form-label">Starting Price</label>
        <input
          type="number"
          id="startingPrice"
          v-model="startingPrice"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="imageUrl" class="form-label">Image URL</label>
        <input
          type="text"
          id="imageUrl"
          v-model="imageUrl"
          class="form-control"
        />
      </div>

      <div class="mb-3">
        <label for="category" class="form-label">Category</label>
        <select v-model="category" id="category" class="form-select" required>
          <option value="">Select Category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="d-grid">
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-else>Update Listing</span>
        </button>
      </div>
    </form>

    <!-- Success Modal -->
    <div v-if="successMessage" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Success</h5>
            <button type="button" class="btn-close" @click="closeSuccessModal"></button>
          </div>
          <div class="modal-body">
            <p>{{ successMessage }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeSuccessModal">OK</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Modal -->
    <div v-if="errorMessage" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger">Error</h5>
            <button type="button" class="btn-close" @click="closeErrorModal"></button>
          </div>
          <div class="modal-body">
            <p>{{ errorMessage }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="closeErrorModal">OK</button>
          </div>
        </div>
      </div>
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
      startingPrice: 0,
      imageUrl: '',
      category: null,
      categories: [],
      listingId: this.$route.params.id,
      loading: true,            // Loading state
      isSubmitting: false,      // Submitting state
      successMessage: '',       // Success message state
      errorMessage: ''          // Error message state
    };
  },
  mounted() {
    // Fetch the listing details and categories on mount
    this.fetchListingDetails();
    this.fetchCategories();
  },
  methods: {
    fetchListingDetails() {
      axios.get(`/api/listing_detail/${this.listingId}/`)
        .then(response => {
          const listing = response.data.listing;
          this.title = listing.title;
          this.description = listing.description;
          this.startingPrice = listing.current_price;
          this.imageUrl = listing.image_url;
          this.category = listing.category_id;
        })
          .finally(() => {
            this.loading = false;
          });
    },
    fetchCategories() {
      axios.get('/api/create_category/')
          .then(response => {
            this.categories = response.data.categories;
          });
    },
    updateListing() {
      this.isSubmitting = true;
      const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];

      axios.put(`/api/edit_listing/${this.listingId}/`, {
        title: this.title,
        description: this.description,
        starting_price: this.startingPrice,
        image_url: this.imageUrl,
        category: this.category
      }, {
        headers: {'X-CSRFToken': csrftoken}
      })
          .then(() => {
            this.successMessage = 'Listing updated successfully!';
          })
          .catch(() => {
            this.errorMessage = 'Failed to update the listing. Please try again.';
          })
          .finally(() => {
            this.isSubmitting = false;
          });
    },
    closeSuccessModal() {
      this.successMessage = '';
      this.$router.push('/my-listings'); // Redirect to My Listings after success
    },
    closeErrorModal() {
      this.errorMessage = '';
    }
  }
};
</script>

<style scoped>
/* Form and spinner styles */
.spinner-border {
  width: 1.5rem;
  height: 1.5rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Modal styling */
.modal-backdrop {
  opacity: 0.5;
}

.modal-dialog {
  max-width: 500px;
  margin: 1.75rem auto;
}
</style>
