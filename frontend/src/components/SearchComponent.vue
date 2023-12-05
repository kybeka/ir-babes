<template>
  <v-container class="search-container">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="title">News d-AI-ly</v-card-title>
          <v-card-text>
            <v-text-field v-model="query" label="Enter your search query" outlined></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="search" color="primary">Search</v-btn>
          </v-card-actions>
        </v-card>

        <v-divider></v-divider>

        <v-card v-if="results.length" class="results-card">
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

        <v-card v-else class="results-card">
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
