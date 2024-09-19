
<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Listings</h1>

    <!-- Loading Spinner -->
    <div v-if="loading" class="d-flex justify-content-center align-items-center vh-100">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Filter Section -->
    <div v-if="!loading" class="row mb-4">
      <!-- Search by name -->
      <div class="col-md-4">
        <div class="input-group">
          <span class="input-group-text"><i class="bi-search"></i></span>
          <input
            type="text"
            class="form-control"
            placeholder="Search by name"
            v-model="filters.name"
            @input="applyFilters"
          />
        </div>
      </div>

      <!-- Select Category -->
      <div class="col-md-4">
        <div class="input-group">
          <span class="input-group-text"><i class="bi-list"></i></span>
          <select class="form-select" v-model="filters.category" @change="applyFilters">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Price Range -->
      <div class="col-md-4">
        <div class="d-flex align-items-center">
          <input
            type="number"
            class="form-control me-2"
            placeholder="Min Price"
            v-model.number="filters.minPrice"
            @input="applyFilters"
          />
          <input
            type="number"
            class="form-control"
            placeholder="Max Price"
            v-model.number="filters.maxPrice"
            @input="applyFilters"
          />
          <button class="btn btn-light ms-2" @click="toggleSliders">
            <i :class="showSliders ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
          </button>
        </div>

        <!-- Sliders (initially hidden) -->
        <transition name="slide">
          <div v-if="showSliders" class="mt-2">
            <input
              type="range"
              class="form-range"
              min="0"
              max="10000"
              step="100"
              v-model.number="filters.minPrice"
              @input="applyFilters"
            />
            <input
              type="range"
              class="form-range"
              min="0"
              max="10000"
              step="100"
              v-model.number="filters.maxPrice"
              @input="applyFilters"
            />
            <small class="text-muted">Price range: {{ filters.minPrice }} - {{ filters.maxPrice }}</small>
          </div>
        </transition>
      </div>
    </div>

    <!-- Sorting Options -->
    <div v-if="!loading" class="row mb-4">
      <div class="col-md-12 d-flex justify-content-start">
        <div class="form-check form-check-inline me-3">
          <input
            class="form-check-input"
            type="radio"
            id="sortLatest"
            value="latest"
            v-model="filters.sort"
            @change="applyFilters"
          />
          <label class="form-check-label" for="sortLatest">Latest</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            id="sortPopular"
            value="popular"
            v-model="filters.sort"
            @change="applyFilters"
          />
          <label class="form-check-label" for="sortPopular">Most Bids</label>
        </div>

        <!-- Reset Filters Button -->
        <button class="btn btn-outline-secondary ms-auto" @click="resetFilters">Reset Filters</button>
      </div>
    </div>

    <!-- Listings Grid -->
    <div v-if="!loading && filteredListings.length === 0" class="text-center">
      <p>No listings match your search criteria.</p>
    </div>

    <div v-if="!loading" class="row">
      <div v-for="listing in filteredListings" :key="listing.id" class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100 shadow-sm listing-card">
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
          <!-- Card Body -->
          <div class="card-body">
            <h5 class="card-title">{{ listing.title }}</h5>
            <p class="card-text">{{ listing.description }}</p>
          </div>

          <!-- Card Footer -->
          <div class="card-footer d-flex justify-content-between align-items-center">
            <router-link :to="'/listing/' + listing.id" class="btn btn-primary">View</router-link>
            <div class="d-flex align-items-center">
              <p class="mb-0 me-3 text-success fw-bold">${{ listing.current_price }}</p>
              <button
                class="btn btn-outline-warning"
                @click="toggleWatchlist(listing.id)"
                :disabled="isToggling[listing.id]"
              >
                <i :class="watchlist.includes(listing.id) ? 'bi-star-fill' : 'bi-star'" class="fs-4"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination Controls -->
    <nav v-if="totalPages > 1" aria-label="Page navigation">
      <ul class="pagination justify-content-center mt-4">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="fetchListings(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
        </li>
        <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
          <button class="page-link" @click="fetchListings(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="fetchListings(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      listings: [],
      watchlist: [],
      categories: [],
      isToggling: {},
      currentPage: 1,
      totalPages: 1,
      loading: true,
      showSliders: false,

      filters: {
        name: '',
        category: '',
        minPrice: 0,
        maxPrice: 10000,
        sort: 'latest'
      },
      filteredListings: []
    };
  },
  mounted() {
    this.fetchListings();
    this.fetchCategories();
    this.fetchWatchlist();
  },
  methods: {

    fetchListings(page = 1) {
      this.loading = true;
      axios.get(`/api/listings/?page=${page}`)
        .then(response => {
          this.listings = response.data.listings;
          this.totalPages = response.data.total_pages;
          this.currentPage = page;
          this.applyFilters();
        })
        .catch(error => {
          console.error('Error fetching listings:', error);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    fetchCategories() {
      axios.get('/api/categories/')
        .then(response => {
          this.categories = response.data.categories;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },

    fetchWatchlist() {
      axios.get('/api/watchlist/')
        .then(response => {
          this.watchlist = response.data.watchlist.map(item => item.id);
        })
        .catch(error => {
          console.error('Error fetching watchlist:', error);
        });
    },

    toggleWatchlist(listingId) {
      this.isToggling = { ...this.isToggling, [listingId]: true };

      if (this.watchlist.includes(listingId)) {

        axios.post(`/api/remove_from_watchlist/${listingId}/`)
          .then(() => {
            this.watchlist = this.watchlist.filter(id => id !== listingId);
          })
          .catch(error => {
            console.error('Error removing from watchlist:', error);
          })
          .finally(() => {
            this.isToggling = { ...this.isToggling, [listingId]: false };
          });
      } else {

        axios.post(`/api/add_to_watchlist/${listingId}/`)
          .then(() => {
            this.watchlist.push(listingId);
          })
          .catch(error => {
            console.error('Error adding to watchlist:', error);
          })
          .finally(() => {
            this.isToggling = { ...this.isToggling, [listingId]: false };
          });
      }
    },

    applyFilters() {
      this.filteredListings = this.listings
        .filter(listing => {
          const nameMatch = listing.title.toLowerCase().includes(this.filters.name.toLowerCase());
          const categoryMatch = this.filters.category
            ? listing.categories__id === parseInt(this.filters.category)
            : true;
          const priceMatch = (!this.filters.minPrice || listing.current_price >= this.filters.minPrice) &&
                             (!this.filters.maxPrice || listing.current_price <= this.filters.maxPrice);

          return nameMatch && categoryMatch && priceMatch;
        })
        .sort((a, b) => {
          if (this.filters.sort === 'latest') {
            return new Date(b.created_at) - new Date(a.created_at);
          } else if (this.filters.sort === 'popular') {
            return (b.bids_count || 0) - (a.bids_count || 0);
          }
          return 0;
        });
    },

    toggleSliders() {
      this.showSliders = !this.showSliders;
    },

    resetFilters() {
      this.filters = {
        name: '',
        category: '',
        minPrice: 0,
        maxPrice: 10000,
        sort: 'latest'
      };
      this.applyFilters();
    }
  }
};
</script>

<style scoped>
/* Card hover effect */
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

/* Pagination styles */
.page-link {
  cursor: pointer;
}

.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
  color: #fff;
}

.page-item.disabled .page-link {
  color: #6c757d;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.card-img-top {
  object-fit: contain;
  height: 200px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.listing-card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

button i.bi-star-fill {
  color: gold;
}

button i.bi-star {
  color: gray;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter, .slide-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
