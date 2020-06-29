<template>
  <div class="hello">
    <div v-for="entry in data" v-bind:key="entry.url">
      <h2>
        <a
          v-bind:href="entry.url"
          v-on:click="access(entry.key, entry.url)"
          v-html="entry.title"
          target="_blank"
        ></a>&nbsp;
        <span
          style="color: red; text-decoration: underline; cursor: pointer;"
          v-on:click="access(entry.key, entry.url)"
          >(X)</span
        >
      </h2>
      <p v-html="entry.snippet"></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
  data: function() {
    return {
      data: [],
    };
  },
  methods: {
    access: function(key, url) {
      this.$http
        .get(this.$backend + "/access", {
          params: {
            key,
            url,
          },
        })
        .then(() => {
          this.data = this.data.filter((entry) => entry.url != url);
        });
    },
  },
  created: function() {
    this.$http.get(this.$backend).then((response) => {
      this.data = response.data.data;
      for (let i = 0; i < this.data.length; i++) {
        console.log(
          (this.data[i].snippet = this.data[i].snippet
            .replace(/\s+/g, " ")
            .replace(new RegExp(this.data[i].key, "ig"), "<b>$&</b>"))
        );
      }
      console.log(this.data);
    });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
