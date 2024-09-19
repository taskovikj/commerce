<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Your Watchlist</h1>

    <!-- If no items in the watchlist -->
    <div v-if="watchlist.length === 0" class="text-center">
      <p>No items in your watchlist.</p>
    </div>

    <!-- Display the watchlist -->
    <div v-else class="row">
      <div v-for="listing in watchlist" :key="listing.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <img
            v-if="listing.image_url"
            :src="listing.image_url"
            class="card-img-top"
            :alt="listing.title"
          />
          <img
            v-else
            src="https://via.placeholder.com/350x200.png?text=No+Image"
            class="card-img-top"
            alt="No image available"
          />
          <div class="card-body">
            <h5 class="card-title">{{ listing.title }}</h5>
            <p class="card-text">{{ listing.description }}</p>
            <p class="card-text">Current Price: ${{ listing.current_price }}</p>
          </div>
          <div class="card-footer text-center">
            <router-link :to="'/listing/' + listing.id" class="btn btn-primary">View Details</router-link>
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
      watchlist: []  // Store the watchlist data
    };
  },
  mounted() {
    console.log('Component Mounted');
    this.fetchWatchlist();  // Fetch the watchlist when the component is mounted
  },
  methods: {
    fetchWatchlist() {
      console.log('Fetching Watchlist...');
      axios.get('/api/watchlist/')
        .then(response => {
          console.log('API Response:', response.data);  // Check the API response
          this.watchlist = response.data.watchlist;  // Store the fetched watchlist data
          console.log('Watchlist Data:', this.watchlist);  // Ensure watchlist is being set
        })
        .catch(error => {
          console.error('Error fetching watchlist:', error);  // Log any error
        });
    }
  }
};
</script>

<style scoped>
.card {
  transition: box-shadow 0.3s ease-in-out;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  object-fit: cover;
  height: 200px;
}
</style>
