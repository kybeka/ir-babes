<template>
    <v-container class="search-container" fluid>
      <v-row justify="center" align="center" class="main">
        <v-col cols="12" sm="8" md="6">
            <v-btn icon @click="goBack" color="primary" class="go-back">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          <v-card class="results-card" elevation="10">
            <!-- Back button to go back to the search page -->

            <v-card-title class="results-title"><u>Most Popular Topics:</u></v-card-title>
            <!-- Display time taken to retrieve data -->
                <v-card v-if="!loading" class="timing-card" elevation="5">
                    <v-card-text>
                    <p>Data retrieved in {{ fetchDataTime }} milliseconds</p>
                    </v-card-text>
                </v-card>
                
            <!-- Loading indicator -->
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
              class="loading-bar"
            ></v-progress-circular>
  
            <!-- Show topics when not loading -->
            <v-list v-if="!loading">
              <v-list-item v-for="(topic, index) in topics" :key="index">
                <v-list-item-content>
                  <v-list-item-title>
                    <!-- Display topic name and value -->
                    <v-card>
                        <v-btn
                        @click="redirectToTopicPage(Object.values(topic)[0])"
                        text
                        color="primary"
                    >
                        {{ ` ${Object.values(topic)[0]}` }}
                    </v-btn>
                    </v-card>


                  </v-list-item-title>
                </v-list-item-content>
                <v-divider :thickness="30" class="border-opacity-0"></v-divider>
              </v-list-item>
            </v-list>
  
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
        responseData: [],
        topics: [],
        fetchStartTime: 0,
        fetchEndTime: 0,
      }
    },
    computed: {
    fetchDataTime() {
        return this.fetchEndTime - this.fetchStartTime;
        },
    },
    methods: {
      async fetchDataFromBackend() {
        this.fetchStartTime = Date.now(); // Record start time before making the request
        try {

          const response = await axios.get(`http://127.0.0.1:5000/menus`);
          this.responseData = response.data;
          this.topics = this.responseData;
          console.log('Response from backend:', this.responseData);
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
            this.fetchEndTime = Date.now(); // Record end time after receiving the response
          this.loading = false;
        }
      },
      redirectToTopicPage(query) {
            // Redirect to a new page with the query being the string of the topic
            this.$router.push(`/topic/${encodeURIComponent(query)}`);
        },
      goBack() {
        this.$router.push('/search');
      },
    },
    created() {
      this.fetchDataFromBackend();
    },
  };
  </script>
  
  <style scoped>

.timing-card {
  margin-top: 5px;
  margin-bottom: 10px;
  text-align: center;
  background-color: #F0F0F0;
  padding: 5px;
}

.go-back {
    align-self:baseline;
}


  .loading-bar {
    margin: 20px;
  }

  .main {
    overflow-x: hidden;
    height: 100vh;
    /* width: 100vh; */
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
  
  .result-link:hover {
    text-decoration: underline;
  }
  
  /* You can include other styles as needed */
  </style>
  
  