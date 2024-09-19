<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">My Listings</h1>

    <div class="row">
      <!-- Loop through the listings and display them -->
      <div v-for="listing in listings" :key="listing.id" class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100 shadow-sm">
          <!-- Display the image if available, otherwise show a placeholder -->
          <img
            :src="getImageUrl(listing.image_url)"
            class="card-img-top"
            :alt="listing.title"
          />
          <div class="card-body">
            <h5 class="card-title">{{ listing.title }}</h5>
            <p class="card-text">{{ listing.description }}</p>

            <!-- Show Active or Closed badge based on auction status -->
            <span :class="listing.closed ? 'badge bg-danger' : 'badge bg-success'">
              {{ listing.closed ? 'Closed' : 'Active' }}
            </span>
          </div>

          <!-- Card Footer with Edit, Delete, and View buttons -->
          <div class="card-footer d-flex justify-content-between">
            <!-- Edit Button -->
            <router-link :to="'/edit-listing/' + listing.id" class="btn btn-outline-secondary">
              Edit
            </router-link>

            <!-- View Button -->
            <router-link :to="'/listing/' + listing.id" class="btn btn-primary">
              View
            </router-link>

            <!-- Delete Button -->
            <button @click="deleteListing(listing.id)" class="btn btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Message when no listings are available -->
    <div v-if="!listings.length" class="text-center">
      <p>You don't have any listings yet.</p>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      listings: []  // Stores all the user's listings
    };
  },
  mounted() {
    // Fetch user's listings when the component is mounted
    this.fetchListings();
  },
  methods: {
    // Fetch listings from the API
    fetchListings() {
      axios.get('/api/my_listings/')
        .then(response => {
          this.listings = response.data.listings; // Store all listings
        })
        .catch(error => {
          console.error('Error fetching listings:', error);
        });
    },

    // Get full image URL or a placeholder
    getImageUrl(imageUrl) {
      if (!imageUrl) {
        return 'https://via.placeholder.com/350x200.png?text=No+Image';
      }
      if (!imageUrl.startsWith('http')) {
        return `${process.env.VUE_APP_BASE_URL}${imageUrl}`;
      }
      return imageUrl;
    },

    // Delete a listing by ID
    deleteListing(listingId) {
      if (confirm('Are you sure you want to delete this listing?')) {
        axios.delete(`/api/delete_listing/${listingId}/`)
          .then(() => {
            this.listings = this.listings.filter(listing => listing.id !== listingId);
          })
          .catch(error => {
            console.error('Error deleting listing:', error);
          });
      }
    }
  }
};
</script>



<style scoped>
/* Card hover effect and responsive styling */
.card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  object-fit: cover;
  height: 200px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 767px) {
  .card {
    margin-bottom: 20px;
  }
}
</style>
