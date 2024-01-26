<template>
    <v-container class="topic-container" fluid>
      <v-row justify="center" align="center" class="main">
        <v-col cols="12" sm="8" md="6">
          <!-- Back button to go back to the topics page -->
          <v-btn icon @click="goBack" color="primary" class="go-back">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
  
          <v-card class="results-card" elevation="10">
            <v-card-title class="results-title"><u>Articles for Topic: {{ topic }}</u></v-card-title>
  
            <!-- Loading indicator -->
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
              class="loading-bar"
            ></v-progress-circular>
            
            <!-- Show articles when not loading -->
            <v-row v-if="!loading">
              <v-col>
                <v-card>
                  <!-- Customize the content based on your article data structure -->
                  <template v-if="isGridView">
                    <v-row>
                    <v-col v-for="result in results" :key="result.rank" cols="12" md="4">
                        <v-card v-if="loading" class="results-card" elevation="10">
                            <v-card-title class="results-title">Loading...</v-card-title>
                        </v-card>
                        <v-card v-else-if="results" class="results-card" elevation="10">
                            <div class="result-image-container">
                                <v-img :src='result.img' alt="Article Image" class="result-image"></v-img>
                            </div>
                            <v-card-title>{{ result.title }}</v-card-title>
                            <v-card-subtitle>{{ truncateText(result.text, 250) }}</v-card-subtitle>
                            <v-card-text class="result-info">
                            <p class="result-author-date">{{ formatAuthorName(result.author)}} | {{ result.year }} | {{ getMonthText(result.month) }}</p>
                            </v-card-text>
                            <v-card-actions>
                            <v-btn text @click="openArticle(result.url)" class="result-link">Read more</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                    </v-row>
                </template>
                </v-card>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        loading: true,
        resuilts: [],
        topic: '',
        isGridView: true,
      };
    },
    methods: {
      async fetchDataFromBackend() {
        this.loading = true
        try {
          // Extract the topic parameter from the route
          this.topic = this.$route.params.topic;
          const response = await axios.get(`http://127.0.0.1:5000/topic/${this.topic}`);
            var jsonString = response.data;
            // console.log(jsonString)
            console.log(jsonString.length)
            var jsonStringArray = []
            
            if (jsonString.length !== undefined) {
            jsonStringArray = jsonString.trim().split('\n');
            } else {
            jsonStringArray.push(JSON.stringify(jsonString))
            }

            const dataArray = jsonStringArray.map(JSON.parse);
            this.results = dataArray;

        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.loading = false;
        }
      },
      goBack() {
        // Use router to navigate back to the topics page
        this.$router.push('/menus');
      },
      truncateText(text, maxLength) {
      if(text === undefined) {
        this.results.text = null
        return
      }
      if (text.length <= maxLength) {
        return text + '...';
      } else {
        return text.substring(0, maxLength) + '...';
      }
    },
    formatAuthorName(author) {
      if(author === null || author === undefined) {
        return this.results.author = "Author"
      }
      // Split the author name into words
      const words = author.toLowerCase().split(' ');
      // Capitalize the first letter of each word
      const capitalizedWords = words.map(word => word.charAt(0).toUpperCase() + word.slice(1));
      // Join the capitalized words back into a string
      return capitalizedWords.join(' ');
    },
    filterByDate() {
      this.search();
    },
    openArticle(url) {
      window.open(url, '_blank');
    },
  getMonthText(month) {
    if(month === null || month === undefined) {
        this.results.month = null
        return 
      }
      const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
      return months[month - 1] || ''; // Subtract 1 as array is zero-based
    }
    },
    created() {
      // Fetch data when the component is created (you can trigger this as needed)
      this.fetchDataFromBackend();
    },
  };
  </script>
  
  <style scoped>

  .result-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 3px solid rgba(169, 169, 169, 0.5); /* 3px semi-opaque grey box */
  border-radius: 5px; /* Optional: Add border-radius for rounded corners */
  overflow: hidden; /* Optional: Hide any overflowing content within the container */
}

.result-image {
  padding-inline: 10px;
  display: stretch;
  max-width: 100%; /* Ensure the image doesn't exceed the container width */
  max-height: 50%; /* Ensure the image doesn't exceed the container height */
  object-fit: cover; /* Maintain aspect ratio while covering the container */
}

  
  .go-back {
    align-self: baseline;
  }
  
  .loading-bar {
    margin: 20px;
  }
  
  .main {
    overflow-x: hidden;
    height: 100vh;
    background: radial-gradient(circle, #d5ced2, #d0bccd, #c5accd, #b29ecf, #9793d3, #8689d7, #7080dc, #5378e1, #566ae5, #605ae6, #6f45e4, #8125de);
  }

  .results-card {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin-top: 20px;
  }
  
  .results-title {
    font-size: 1.8em;
    font-weight: bold;
    color: #673AB7; /* Vuetify primary color */
  }

  .result-link {
  object-fit: cover;
  text-decoration: none;
  color: #2196F3;
  /* Vuetify primary color */
  font-size: 1.2em;
  font-weight: bold;
  cursor: pointer;
}

.result-link:hover {
  text-decoration: underline;
}
  
  /* You can include other styles as needed */
  </style>
  