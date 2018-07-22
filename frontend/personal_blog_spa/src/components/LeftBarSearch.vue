<template>
  <div class="single-blog-page">
    <!-- search option start -->
    <form action="#">
      <div class="search-option">
        <input type="text" placeholder="Search..." v-model="keyword">
        <button class="button" type="submit"
                v-on:click.stop.prevent="search()"
                v-on:submit.stop.prevent="search()">
          <i class="fa fa-search"></i>
        </button>
      </div>
    </form>
    <!-- search option end -->
  </div>
</template>

<script>
export default {
    name: 'LeftBarSearch',
    data() {
        return {
            keyword: ''
        }
    },
    methods: {
        search: function(keyword) {
            this.$router.push({ name: 'Search', params: { keyword: this.keyword }})
        }
    }
}
</script>

<style scoped>
</style>
