<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">My Bids</h1>

    <!-- Loader while data is being fetched -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- If there are no bids -->
    <div v-if="!loading && bidListings.length === 0" class="text-center">
      <p>You have not placed any bids yet.</p>
    </div>

    <!-- Bid Listings -->
    <div v-if="!loading && bidListings.length > 0" class="row">
      <div v-for="listing in bidListings" :key="listing.id" class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100 shadow-sm">
          <!-- Listing Image -->
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

          <!-- Listing Title and Info -->
          <div class="card-body">
            <h5 class="card-title">{{ listing.title }}</h5>
            <p class="card-text">Current Price: ${{ listing.current_price }}</p>
          </div>

          <!-- Status Badge and Buttons -->
          <div class="card-footer d-flex justify-content-between align-items-center">
            <span class="badge"
                  :class="{
                    'bg-warning': listing.status === 'Winning',
                    'bg-danger': listing.status === 'Outbid',
                    'bg-secondary': listing.status === 'Lost',
                    'bg-success': listing.status === 'Won'
                  }">
              {{ listing.status }}
            </span>
            <router-link :to="'/listing/' + listing.id" class="btn btn-primary">
              View Listing
            </router-link>
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
      bidListings: [], // List of listings where the user has placed a bid
      loading: true,   // Loading state
    };
  },
  mounted() {
    this.fetchUserBids();
  },
  methods: {
    // Fetch listings where the user has placed a bid
    fetchUserBids() {
      axios.get('/api/user_bids/')
        .then(response => {
          this.bidListings = response.data.bid_listings;
        })
        .catch(error => {
          console.error('Error fetching user bids:', error);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>



<style scoped>
.container {
  max-width: 1200px;
}

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

.card-body {
  text-align: left;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
}

.badge {
  font-size: 1rem;
  padding: 0.5rem 1rem;
}

.btn {
  margin-left: 10px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>


