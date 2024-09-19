<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-lg-4 text-center mb-4">
        <i class="bi-person-circle" style="font-size: 100px;"></i>
        <h2 class="mt-3">My Profile</h2>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>

        <div class="d-flex justify-content-center mt-4">
          <button
            class="btn me-2"
            :class="showEditForm ? 'btn-danger' : 'btn-secondary'"
            @click="toggleEditForm"
          >
            {{ showEditForm ? 'Cancel Edit Profile' : 'Edit Profile' }}
          </button>
          <button
            class="btn"
            :class="showPasswordForm ? 'btn-danger' : 'btn-secondary'"
            @click="togglePasswordForm"
          >
            {{ showPasswordForm ? 'Cancel Update Password' : 'Update Password' }}
          </button>
        </div>
      </div>

      <div class="col-lg-8">
        <div class="row mb-4">
          <div class="col-md-12">
            <div class="card h-100 shadow-sm p-4">
              <h4 class="card-title text-center">Auction Stats</h4>
              <div class="row">
                <div class="col-md-6 text-center">
                  <p><strong>Total Won Auctions:</strong></p>
                  <p class="display-4 text-primary">{{ totalWonAuctions }}</p>
                  <p><strong>Total Money Spent:</strong></p>
                  <p class="display-4 text-danger">${{ totalMoneySpent }}</p>
                </div>
                <div class="col-md-6 text-center">
                  <p><strong>Total Sold Items:</strong></p>
                  <p class="display-4 text-primary">{{ totalSoldItems }}</p>
                  <p><strong>Total Money Earned:</strong></p>
                  <p class="display-4 text-success">${{ totalMoneyEarned }}</p>
                </div>
              </div>

              <div class="row mt-4">
                <div class="col text-center">
                  <p><strong>Net Balance (Earned - Spent):</strong></p>
                  <p
                    :class="netBalanceClass"
                    class="display-4"
                  >
                    ${{ netBalance }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <!-- My Listings Section -->
          <div class="col-md-6">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h4 class="card-title">My Listings</h4>
                <ul class="list-group list-group-flush">
                  <li v-for="listing in myListings" :key="listing.id" class="list-group-item">
                    {{ listing.title }}
                  </li>
                </ul>
              </div>
              <div class="card-footer text-center">
                <router-link to="/my-listings" class="btn btn-primary">See more</router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h4 class="card-title">Watchlist</h4>
                <ul class="list-group list-group-flush">
                  <li v-for="item in watchlist" :key="item.id" class="list-group-item">
                    {{ item.title }}
                  </li>
                </ul>
              </div>
              <div class="card-footer text-center">
                <router-link to="/watchlist" class="btn btn-primary">See more</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showEditForm" class="mt-4">
      <h4>Edit Profile</h4>
      <form @submit.prevent="updateProfile">
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="username" class="form-label">Username</label>
            <input v-model="editUser.username" type="text" class="form-control" id="username" required />
          </div>
          <div class="col-md-6">
            <label for="email" class="form-label">Email</label>
            <input v-model="editUser.email" type="email" class="form-control" id="email" required />
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="first_name" class="form-label">First Name</label>
            <input v-model="editUser.first_name" type="text" class="form-control" id="first_name" />
          </div>
          <div class="col-md-6">
            <label for="last_name" class="form-label">Last Name</label>
            <input v-model="editUser.last_name" type="text" class="form-control" id="last_name" />
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>

    <div v-if="showPasswordForm" class="mt-4">
      <h4>Update Password</h4>
      <form @submit.prevent="updatePassword">
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="password" class="form-label">New Password</label>
            <input v-model="passwordData.new_password" type="password" class="form-control" id="password" required />
          </div>
          <div class="col-md-6">
            <label for="password_confirmation" class="form-label">Confirm New Password</label>
            <input v-model="passwordData.confirm_password" type="password" class="form-control" id="password_confirmation" required />
          </div>
        </div>
        <button type="submit" class="btn btn-primary">Update Password</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {},
      totalWonAuctions: 0,
      totalMoneySpent: 0,
      totalSoldItems: 0,
      totalMoneyEarned: 0,
      editUser: {},
      myListings: [],
      watchlist: [],
      showEditForm: false,
      showPasswordForm: false,
      passwordData: {
        new_password: '',
        confirm_password: ''
      }
    };
  },
  computed: {

    netBalance() {
      return this.totalMoneyEarned - this.totalMoneySpent;
    },

    netBalanceClass() {
      return this.netBalance >= 0 ? 'text-success' : 'text-danger';
    }
  },
  mounted() {
    this.fetchUserProfile();
    this.fetchUserListings();
    this.fetchUserWatchlist();
  },
  methods: {

    toggleEditForm() {
      this.showEditForm = !this.showEditForm;
      this.showPasswordForm = false;
    },

    togglePasswordForm() {
      this.showPasswordForm = !this.showPasswordForm;
      this.showEditForm = false;
    },

    fetchUserProfile() {
      axios.get('/api/my_profile/')
          .then(response => {
            const data = response.data;
            this.user = data.user;
            this.totalWonAuctions = data.total_won_auctions;
            this.totalMoneySpent = data.total_money_spent;
            this.totalSoldItems = data.total_sold_items;
            this.totalMoneyEarned = data.total_money_earned;
            this.editUser = {...this.user};
          });
    },

    fetchUserListings() {
      axios.get('/api/my_listings/')
          .then(response => {
            this.myListings = response.data.listings.slice(0, 3);
          });
    },

    fetchUserWatchlist() {
      axios.get('/api/watchlist/')
          .then(response => {
            this.watchlist = response.data.watchlist.slice(0, 3);
          });
    },

    updateProfile() {
      const payload = {
        username: this.editUser.username,
        email: this.editUser.email,
        first_name: this.editUser.first_name,
        last_name: this.editUser.last_name
      };

      axios.put('/api/my_profile/', payload)
          .then(() => {
            this.user = {...this.editUser};
            this.showEditForm = false;
            alert('Profile updated successfully!');
          })
          .catch(error => {
            console.error('Error updating profile:', error);
            alert('Failed to update profile. Please try again.');
          });
    },

    updatePassword() {
      if (this.passwordData.new_password !== this.passwordData.confirm_password) {
        alert('Passwords do not match');
        return;
      }

      const payload = {
        password: this.passwordData.new_password
      };

      axios.put('/api/update_password/', payload)
          .then(() => {
            this.passwordData.new_password = '';
            this.passwordData.confirm_password = '';
            this.showPasswordForm = false;
            alert('Password updated successfully!');
          })
          .catch(error => {
            console.error('Error updating password:', error);
            alert('Failed to update password. Please try again.');
          });
    }
  }
};
</script>

<style scoped>
.bi-person-circle {
  color: #6c757d;
}

.text-center {
  text-align: center;
}

.d-flex .btn {
  margin-right: 10px;
}

.card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card-footer {
  text-align: center;
}

.display-4 {
  font-size: 2.5rem;
  font-weight: bold;
}
</style>