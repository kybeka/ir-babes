<template>
  <v-container class="search-container" fluid>
    <v-row justify="center" align="center" style="height: 100vh">
      <v-col cols="12" sm="8" md="6">
        <v-card class="search-card" elevation="10">
          <v-card-title class="title">News d-AI-ly</v-card-title>
          <v-card-text>
            <v-text-field v-model="query" label="Enter your search query" outlined dense></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="search" color="primary">Search</v-btn>
          </v-card-actions>
        </v-card>

        <v-divider></v-divider>

        <v-card v-if="results.length" class="results-card" elevation="10">
          <v-card-title class="results-title">Search Results</v-card-title>
          <v-list>
            <v-list-item v-for="result in results" :key="result.id">
              <v-list-item-content>
                <v-list-item-title>
                  <v-btn text :href="result.url" class="result-link">{{ result.title }}</v-btn>
                </v-list-item-title>
                <v-list-item-subtitle>{{ result.description }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>

        <v-card v-else class="results-card" elevation="10">
          <v-card-title class="results-title">No results found</v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      results: [],
    };
  },
  methods: {
    search() {
      // Simulate search results (replace this with your actual data)
      this.results = [
        { id: 1, title: 'Result 1', description: 'Description for Result 1', url: 'https://example.com/result1' },
        { id: 2, title: 'Result 2', description: 'Description for Result 2', url: 'https://example.com/result2' },
        // Add more results as needed
      ];
    },
  },
};
</script>

<style scoped>
.search-container {
  background: linear-gradient(to bottom right, #673AB7, #2196F3);
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
