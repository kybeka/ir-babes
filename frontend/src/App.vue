<template>
  <v-app>
    <v-main>
      <!-- <HelloWorld/> -->
      <SearchComponentVue/>
    </v-main>
  </v-app>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import SearchComponentVue from './components/SearchComponent.vue'

export default {
  name: 'App',

  components: {
    // HelloWorld,
    SearchComponentVue
  },

  data: () => ({
    //
  }),
}
</script>
