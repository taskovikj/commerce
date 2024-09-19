import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import ListingDetailPage from './components/ListingDetailPage.vue';
import CreateListingPage from './components/CreateListingPage.vue';
import EditListingPage from './components/EditListingPage.vue';
import MyListingsPage from './components/MyListingsPage.vue';
import WatchlistPage from './components/WatchlistPage.vue';
import ProfilePage from './components/ProfilePage.vue';
import MyBids from '@/components/MyBids.vue';
// import UpdatePasswordPage from './components/UpdatePasswordPage.vue';

// Define your routes
const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/listing/:id', name: 'ListingDetail', component: ListingDetailPage },
  { path: '/create-listing', name: 'CreateListing', component: CreateListingPage, meta: { requiresAuth: true } },
  { path: '/my-listings', name: 'MyListings', component: MyListingsPage, meta: { requiresAuth: true } },
  // { path: '/update-password', name: 'UpdatePasswordPage', component: UpdatePasswordPage, meta: { requiresAuth: true } },
  {
      path: '/my-bids', name: 'MyBids', component: MyBids },
  { path: '/edit-listing/:id', name: 'EditListing', component: EditListingPage, meta: { requiresAuth: true } },

    { path: '/watchlist', name: 'Watchlist', component: WatchlistPage, meta: { requiresAuth: true } },
  { path: '/my-profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } }

];

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  // If the route requires authentication and the user is not authenticated
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next(); // Allow access if authenticated or the route does not require authentication
  }
});

export default router;
