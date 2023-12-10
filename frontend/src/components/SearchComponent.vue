<template>
  <v-container class="search-container" fluid>
    <v-row justify="center" align="center" style="height: 100vh">
      <v-col cols="12" sm="8" md="6">
        <v-card class="search-card" elevation="10">
           <!-- Use v-img for the logo -->
           <v-img
            src="../assets/logo/logo.png"
            max-height="200"
          ></v-img>
          <v-card-text>
            <v-text-field v-model="query" label="Enter your search query" outlined dense>
            </v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="search()" color="primary">Search</v-btn>
            <v-btn @click="toggleView()" color="primary">Toggle View</v-btn>
          </v-card-actions>
        </v-card>
        
        
        <v-divider></v-divider>
        
        
        <v-card v-if="results" class="results-card" elevation="10">
          <v-card-title class="results-title">Search Results</v-card-title>

          <template v-if="isGridView">
            <v-row>
              <v-col v-for="result in results" :key="result.rank" cols="12" md="4">   
                <v-card v-if="loading" class="results-card" elevation="10">
                  <v-card-title class="results-title">Loading...</v-card-title>
                </v-card>

                <v-card v-else-if="results" class="results-card" elevation="10">
                  <!-- ... (your existing template for results) ... -->
                  <v-card>
                    <v-card-title>{{ result.title }}</v-card-title>
                    <v-card-subtitle>{{ result.text }}</v-card-subtitle>
                    <v-card-actions>
                      <v-btn text :href="result.url" class="result-link">Read more</v-btn>
                    </v-card-actions>
                </v-card>
                </v-card>
                <v-card v-else class="results-card" elevation="10">
                  <v-card-title class="results-title">No results found</v-card-title>
                </v-card>
      
              </v-col>
            </v-row>
          </template>

          <template v-else>
            <v-list>
              <v-list-item v-for="result in results" :key="result.docid">
                <v-list-item-content>
                  <v-list-item-title>
                    <v-btn text :href="result.url" class="result-link">{{ result.title }}</v-btn>
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ result.text }}</v-list-item-subtitle>
                </v-list-item-content>
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
import axios from 'axios'


export default {
  data() {
    return {
      query: '',
      results: [{"title": "chris"}],
      isGridView: false, // Added boolean to track view mode
      loading: false, // Added loading state
    };
  },
  methods: {
    async search() {
    try {
      this.loading = true; // Set loading to true before making the request
      const response = await axios.get(`http://localhost:5000/search/${this.query}`);
      console.log(response);
      var jsonString = response.data
      const jsonStringArray = jsonString.trim().split('\n');

      // Parse each string in the array into a JavaScript object
      const dataArray = jsonStringArray.map(JSON.parse);

      console.log(dataArray);

      this.results = dataArray
      console.log("this.results:", this.results);
    } catch (error) {
      console.error(error);
    } finally {
      this.loading = false; // Set loading to false after the request (whether success or error)
    }
  },
    toggleView() {
      this.isGridView = !this.isGridView; // Toggle between list and grid view
    },
  },
};
</script>

<style scoped>
.search-container {
  background-image: radial-gradient(circle, #d5ced2, #d0bccd, #c5accd, #b29ecf, #9793d3, #8689d7, #7080dc, #5378e1, #566ae5, #605ae6, #6f45e4, #8125de);
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
  color: #2196F3; /* Vuetify primary color */
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
  text-decoration: none;
  color: #2196F3; /* Vuetify primary color */
  font-size: 1.2em;
  font-weight: bold;
}

.result-link:hover {
  text-decoration: underline;
}

</style>
