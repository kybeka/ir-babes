<template>
  <v-container class="search-container" fluid>

    <v-card class="timing-card" v-if="searched && !loading" elevation="5">
      <v-card-text>
        <p>Results retrieved in {{ queryTime }} milliseconds</p>
      </v-card-text>
    </v-card>

    <v-row justify="center" align="center" class="main">
      <v-col cols="12" sm="8" md="6">
        <v-card class="search-card" elevation="10">
          <!-- Use v-img for the logo -->
          <v-img src="../assets/logo/logo.png" max-height="175"></v-img>
          <v-card-text>
            <v-text-field
                v-model="query"
                label="Enter your search query"
                outlined
                dense
                @keydown.enter="search"
              ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="search()" color="primary">Search</v-btn>
            <v-btn  prepend-icon="" @click="toggleView()" color="primary">Toggle View</v-btn>
            <v-divider class="border-opacity-0"></v-divider>
            <v-menu offset-y>
            <template v-slot:activator="{ on }">
                <v-btn v-on="on" icon>
                  <v-icon>mdi-calendar-month</v-icon>
                </v-btn>
              </template>

              <v-date-picker v-model="selectedDate" @input="filterByDate"></v-date-picker>
          </v-menu>

          </v-card-actions>
        </v-card>

        <v-divider></v-divider>

        <!-- Conditionally render the search results section -->
        <v-card v-if="searched && results" class="results-card" elevation="10">
          <v-card-title class="results-title"><u>Search Results</u></v-card-title>

          <template v-if="isGridView">
            <v-row>
              <v-col v-for="result in results" :key="result.rank" cols="12" md="4">

                  <v-card v-if="loading" class="results-card" elevation="10">
                    <v-card-title class="results-title">Loading...</v-card-title>
                  </v-card>

                  <v-card v-else-if="results" class="results-card" elevation="10">
                    <v-img :src="result.image" alt="Article Image" class="result-image" @load="handleImageLoad"></v-img>
                    <v-card-title>{{ result.title }}</v-card-title>
                    <v-card-subtitle>{{ truncateText(result.text, 250) }}</v-card-subtitle>
                    <v-card-text class="result-info">
                      <p class="result-author-date">{{ formatAuthorName(result.author)}} | {{ result.year }}, {{ result.month }}</p>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn text :href="result.url" class="result-link">Read more</v-btn>
                    </v-card-actions>
                  </v-card>
                  <v-divider v-if="index < results.length - 1"></v-divider>
              </v-col>
            </v-row>
          </template>

          <template v-else>
            <v-list>
              <v-list-item v-for="result in results" :key="result.docid">
                <v-list-item-content>
                  <v-img :src="result.image" alt="Article Image" class="result-image"></v-img>
                  <v-list-item-title>
                    <v-text text :href="result.url" class="result-link">{{ result.title }}</v-text>
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ truncateText(result.text, 250) }}</v-list-item-subtitle>
                  <v-list-item-content class="result-info">
                    <p class="result-author-date">{{ formatAuthorName(result.author) }} | {{ result.year }}, {{ result.month }}</p>
                  </v-list-item-content>
                </v-list-item-content>
                <v-divider :thickness="30" class="border-opacity-0"></v-divider>
              </v-list-item>
            </v-list>
          </template>
        </v-card>

        <v-card v-else class="results-card" elevation="10">
          <v-card-title class="results-title">No results found</v-card-title>
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
      query: '',
      results: [],
      isGridView: false,
      loading: false,
      searched: false, // Added searched variable
      queryTime: 0,
      selectedDate: null,
    };
  },
  methods: {
    async search() {
      try {
        const startTime = Date.now(); // Record start time before making the request
        this.loading = true;
        const response = await axios.get(`http://localhost:5000/search/${this.query}`);
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
        const endTime = Date.now(); // Record end time after receiving the response
        this.queryTime = endTime - startTime; // Calculate the time taken for the query
        this.searched = true;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    toggleView() {
      this.isGridView = !this.isGridView;
    },
    truncateText(text, maxLength) {
      if (text.length <= maxLength) {
        return text + '...';
      } else {
        return text.substring(0, maxLength) + '...';
      }
    },
    formatAuthorName(author) {
      if(author === null) {
        return "Author"
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
  },
};
</script>

<style scoped>
.timing-card {
  margin-top: 5px;
  margin-bottom: 10px;
  text-align: center;
  background-color: #F0F0F0;
  /* border-radius: 5px; */
  padding: -3px;

}

.main {
  overflow-x: hidden;
  height: 100vh
}

.result-image {
  max-width: 10%; /* Ensure images don't exceed the container width */
  max-height: 200px; /* Set a maximum height for the images */
  object-fit: cover; /* Maintain aspect ratio while covering the container */
}

.search-container {
  background: radial-gradient(circle, #d5ced2, #d0bccd, #c5accd, #b29ecf, #9793d3, #8689d7, #7080dc, #5378e1, #566ae5, #605ae6, #6f45e4, #8125de);
  padding: 0;
}

.search-card {
  background-color: #FFFFFF;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 20px;
  color: #2196F3;
  /* Vuetify primary color */
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
  color: #673AB7;
  /* Vuetify primary color */
}

.result-link {
  object-fit: cover;
  text-decoration: none;
  color: #2196F3;
  /* Vuetify primary color */
  font-size: 1.2em;
  font-weight: bold;
}

.result-link:hover {
  text-decoration: underline;
}</style>
