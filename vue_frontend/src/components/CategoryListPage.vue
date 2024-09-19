<template>
  <div>
    <h2>{{ category.name }}</h2>
    <div v-for="listing in listings" :key="listing.id">
      <h3>{{ listing.title }}</h3>
      <p>{{ listing.description }}</p>
      <router-link :to="'/listing/' + listing.id">View</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      category: {},
      listings: []
    };
  },
  mounted() {
    const categoryId = this.$route.params.id;
    axios.get(`/api/category_listings/${categoryId}/`)
      .then(response => {
        this.category = response.data.category;
        this.listings = response.data.listings;
      });
  }
};
</script>
