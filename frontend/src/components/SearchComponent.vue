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
                variant="outlined"
                @keydown.enter="search"
              ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="search()" color="primary"><v-icon>mdi-search-web</v-icon>Search</v-btn>
            <v-btn @click="toggleView()" color="primary"><v-icon>mdi-view-grid</v-icon> Toggle View</v-btn>
            <v-divider class="border-opacity-0"></v-divider>
            <v-btn icon @click="redirectToMenusPage" color="primary">
                <v-icon>mdi-menu</v-icon>
            </v-btn>
            <!-- <v-menu offset-y>
            <template v-slot:activator="{ on }">
                <v-btn v-on="on" icon>
                  <v-icon>mdi-calendar-month</v-icon>
                </v-btn>
              </template>

              <v-date-picker v-model="selectedDate" @input="filterByDate"></v-date-picker>
          </v-menu> -->

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
                    <div v-if="result.img !== undefined" class="result-image-container">
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

          <template v-else>
            <v-list>
              <v-list-item v-for="result in results" :key="result.docid">
                <v-list-item-content>
                  <div class="result-image-container">
                      <v-img :src='result.img' alt="Article Image" class="result-image"></v-img>
                    </div>
                  <v-list-item-title>
                    <v-text text @click="openArticle(result.url)" class="result-link">{{ result.title }}</v-text>
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ truncateText(result.text, 250) }}</v-list-item-subtitle>
                  <v-list-item-content class="result-info">
                    <!-- <template v-if="this.results.author !== undefined && this.results.month !== undefined && this.results.text !== undefined"> -->
                      <p class="result-author-date">{{ formatAuthorName(result.author) }} | {{ result.year }} | {{ getMonthText(result.month) }}</p>
                  <!-- </template> -->
                  </v-list-item-content>
                </v-list-item-content>
                <v-divider :thickness="30" class="border-opacity-0"></v-divider>
              </v-list-item>
            </v-list>
          </template>
        </v-card>

        <v-card v-else-if="results == []" class="results-card" elevation="10">
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
    redirectToMenusPage() {
        this.$router.push('/menus');
    },
    async search() {
      try {
        const startTime = Date.now(); // Record start time before making the request
        this.loading = true;
        const response = await axios.get(`http://localhost:5000/search/${this.query}`);
        var jsonString = response.data;
        // console.log(jsonString)
        // console.log(jsonString.length)
        var jsonStringArray = []
        
        if (jsonString.length !== undefined) {
          jsonStringArray = jsonString.trim().split('\n');
        } else {
          jsonStringArray.push(JSON.stringify(jsonString))
        }

        const dataArray = jsonStringArray.map(JSON.parse);
        console.log(dataArray[0])
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
};
</script>

<style scoped>
.timing-card {
  margin-top: 5px;
  margin-bottom: 10px;
  text-align: center;
  background-color: #F0F0F0;
  padding: -3px;

}

.main {
  overflow-x: hidden;
  height: 100vh
}

.result-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 3px solid rgba(169, 169, 169, 0.5); 
  border-radius: 5px; 
  overflow: hidden; 
}

.result-image {
  padding-inline: 10px;
  max-width: 50%; 
  max-height: 75%; 
  object-fit: cover; 
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
 
}

.result-link {
  object-fit: cover;
  text-decoration: none;
  color: #2196F3;
  font-size: 1.2em;
  font-weight: bold;
  cursor: pointer;
}

.result-link:hover {
  text-decoration: underline;
}</style>
