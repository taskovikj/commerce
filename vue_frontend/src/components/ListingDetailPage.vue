<template>
  <div class="container my-5">
    <div v-if="listing.title" class="card">
      <div class="row g-0">
        <div class="col-md-4">
          <img v-if="listing.image_url" :src="listing.image_url" class="img-fluid rounded-start" :alt="listing.title" />
          <div v-else class="d-flex justify-content-center align-items-center bg-light" style="height: 250px;">
            <p class="text-muted">No photo available</p>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card-body">
            <h2 class="card-title mb-3">{{ listing.title }}</h2>
            <p class="card-text">{{ listing.description }}</p>
            <p><strong>Category:</strong> {{ listing.category_name || 'N/A' }}</p>
            <p><strong>Created At:</strong> {{ new Date(listing.created_at).toLocaleDateString() }}</p>
            <p><strong>Starting Price:</strong> ${{ listing.starting_price }}</p>
            <p class="fw-bold">Current Price: ${{ listing.current_price }}</p>
            <p>Highest Bidder: {{ listing.highest_bidder || 'No bids yet' }}</p>

            <div v-if="listing.closed" class="alert alert-danger mt-3">
              This auction is closed. {{ listing.highest_bidder ? `Winner: ${listing.highest_bidder}` : 'No bids were placed.' }}
            </div>

            <div v-if="isOwner && !listing.closed" class="mt-3">
              <button @click="closeAuction" class="btn btn-danger">Close Auction</button>
            </div>

            <div v-if="!isOwner && !listing.closed && isAuthenticated" class="mt-4">
              <h4>Place a Bid</h4>
              <input v-model="bidAmount" type="number" step="0.01" class="form-control" placeholder="Enter your bid" />
              <button @click="placeBid" class="btn btn-success mt-2" :disabled="isSubmitting">
                {{ isSubmitting ? 'Placing Bid...' : 'Place Bid' }}
              </button>
              <div v-if="bidSuccessMessage" class="text-success mt-2">{{ bidSuccessMessage }}</div>
              <div v-if="bidErrorMessage" class="text-danger mt-2">{{ bidErrorMessage }}</div>
            </div>

            <div v-if="!isAuthenticated" class="alert alert-warning mt-4">
              Please <router-link to="/login">login</router-link> to place a bid.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="comments-section mt-5" v-if="listing.title">
      <h3>Comments</h3>
      <ul class="list-group">
        <li v-for="comment in comments" :key="comment.id" class="list-group-item">
          {{ comment.text }} - <strong>{{ comment.user__username || 'Anonymous' }}</strong>
        </li>
      </ul>

      <div v-if="isAuthenticated" class="mt-4">
        <h4>Add a Comment</h4>
        <textarea v-model="comment" class="form-control" rows="3" placeholder="Write your comment..."></textarea>
        <button @click="addComment" class="btn btn-primary mt-2" :disabled="isSubmitting">
          {{ isSubmitting ? 'Submitting...' : 'Add Comment' }}
        </button>
        <div v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</div>
      </div>
      <div v-else class="alert alert-warning mt-4">
        Please <router-link to="/login">login</router-link> to add a comment.
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      listing: {},
      comments: [],
      comment: '',
      errorMessage: '',
      bidAmount: '',
      bidErrorMessage: '',
      bidSuccessMessage: '',
      isAuthenticated: false,
      isOwner: false,
      listingId: this.$route.params.id,
      isSubmitting: false,
    };
  },
  mounted() {
    this.fetchListingDetails();
  },
  methods: {
    fetchListingDetails() {
      axios
        .get(`/api/listing_detail/${this.listingId}/`)
        .then((response) => {
          this.listing = response.data.listing || {};
          this.comments = response.data.comments || [];
          this.isAuthenticated = response.data.isAuthenticated || false;
          this.isOwner = response.data.isOwner || false;
        })
        .catch((error) => {
          console.error('Error fetching listing details:', error);
        });
    },
    addComment() {
      if (this.comment.trim() === '') {
        this.errorMessage = 'Comment cannot be empty';
        return;
      }

      this.isSubmitting = true;
      this.errorMessage = '';

      const csrftoken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];

      axios
        .post(`/api/listing_detail/${this.listingId}/`, { text: this.comment }, {
          headers: {
            'X-CSRFToken': csrftoken,
          },
        })
        .then((response) => {
          this.comments.push({
            text: this.comment,
            user__username: response.data.username,
            created_at: new Date().toISOString(),
          });
          this.comment = '';
        })
        .catch((error) => {
          console.error('Error adding comment:', error.response ? error.response.data : error);
          this.errorMessage = 'Failed to add comment. Please try again.';
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
    placeBid() {
      if (!this.bidAmount || parseFloat(this.bidAmount) <= parseFloat(this.listing.current_price)) {
        this.bidErrorMessage = 'Bid must be higher than the current price';
        return;
      }

      this.isSubmitting = true;
      this.bidErrorMessage = '';
      this.bidSuccessMessage = '';

      const csrftoken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];

      axios
        .post(`/api/listing_detail/${this.listingId}/`, { bid_amount: this.bidAmount }, {
          headers: {
            'X-CSRFToken': csrftoken,
          },
        })
        .then((response) => {
          if (response.data.status === 'success') {
            this.listing.current_price = response.data.current_price;
            this.bidSuccessMessage = 'Bid placed successfully!';
            this.bidAmount = '';
          } else {
            this.bidErrorMessage = response.data.message || 'Failed to place bid.';
          }
        })
        .catch((error) => {
          this.bidErrorMessage = error.response?.data?.message || 'Failed to place bid. Please try again.';
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
    closeAuction() {
      if (confirm('Are you sure you want to close this auction?')) {
        axios
          .post(`/api/close_auction/${this.listingId}/`)
          .then((response) => {
            if (response.data.status === 'success') {
              this.listing.closed = true;
              alert('Auction closed successfully!');
            } else {
              alert(response.data.message || 'Failed to close the auction.');
            }
          })
          .catch((error) => {
            console.error('Error closing the auction:', error);
            alert('Failed to close the auction. Please try again.');
          });
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
}

.img-fluid {
  object-fit: cover;
  height: 100%;
  width: 100%;
}

.comments-section {
  margin-top: 2rem;
}

.card {
  border: 1px solid #ddd;
  margin-top: 20px;
}

.no-photo {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  color: #6c757d;
}
</style>
