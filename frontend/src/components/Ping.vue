<template>
    <div>
      <p>{{ msg }}</p>
      <label for="parameterInput">Enter Parameter:</label>
      <input v-model="parameter" type="text" id="parameterInput" />
      <button @click="sendRequest">Send Request</button>

    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export default {
    name: 'PingVue',

    data() {
      return {
        msg: '',
        parameter: ''
      };
    },
    methods: {
        async getMessage() {
            const path = 'http://localhost:5000/ping';
            await axios.get(path)
                    .then((res) => {
                        this.msg = res.data;
                    })
                .catch((error) => {
                    console.error(error);
                });
    },
    sendRequest() {
      axios.get(`http://localhost:5000/ping/${this.parameter}`)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
  },

  created() {
    this.getMessage();
  },
  };
  </script>