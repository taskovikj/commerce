<template>
  <div>
    <h2>{{ listing.title }}</h2>
    <p>{{ listing.description }}</p>

    <h3>Comments</h3>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        {{ comment.text }} - {{ comment.user.username }}
      </li>
    </ul>

    <div v-if="isAuthenticated">
      <h4>Add a Comment</h4>
      <textarea v-model="comment" placeholder="Write your comment..."></textarea>
      <button @click="addComment">Add Comment</button>
      <div v-if="errorMessage">{{ errorMessage }}</div>
    </div>
    <div v-else>
      <p>Please login to add a comment.</p>
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
      isAuthenticated: false,
      listingId: this.$route.params.id
    };
  },
  mounted() {
    axios.get(`/api/listing_detail/${this.listingId}/`)
        .then(response => {
          this.listing = response.data.listing;
          this.comments = response.data.comments;
          this.isAuthenticated = response.data.isAuthenticated;
        })
        .catch(error => {
          console.error('Error fetching listing details:', error);
        });
  },
  methods: {
    addComment() {
      if (this.comment.trim() === '') {
        this.errorMessage = 'Comment cannot be empty';
        return;
      }

      const csrftoken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      axios.post(`/api/listing_detail/${this.listingId}/`, {
        text: this.comment
      }, {
        headers: {
          'X-CSRFToken': csrftoken
        }
      }).then(response => {
        this.comments.push({
          text: this.comment,
          user: { username: response.data.username },
          created_at: new Date().toISOString()
        });
        this.comment = '';
        this.errorMessage = '';
      }).catch(error => {
        console.error('Error adding comment:', error.response ? error.response.data : error);
        this.errorMessage = 'Failed to add comment. Please try again.';
      });
    }
  }
};
</script>
