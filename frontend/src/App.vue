<template>
  <v-app>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script>
import { RouterView } from 'vue-router'

export default {
  name: 'App',

  components: {
    RouterView
},

  data: () => ({
    //
  }),
}
</script>
