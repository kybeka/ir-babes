<template>
    <div>
      <input v-model="query" placeholder="Enter your search query" />
      <button @click="search">Search</button>
  
      <div v-if="results.length">
        <h2>Search Results</h2>
        <ul>
          <li v-for="result in results" :key="result.id">
            <a :href="result.url" target="_blank">{{ result.title }}</a>
            <p>{{ result.description }}</p>
          </li>
        </ul>
      </div>
  
      <div v-else>
        <p>No results found for the given query.</p>
      </div>
    </div>
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
  /* Add your component styles here */
  
  div {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  
  button {
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 20px;
  }
  
  a {
    text-decoration: none;
    color: #1e88e5;
    font-weight: bold;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  </style>