<template>
  <div class="single-blog-page">
    <div class="left-tags blog-tags">
      <div class="popular-tag left-side-tags left-blog">
        <h4>tags</h4>
        <ul>
          <li v-for="tag in tags" :key="tag.tag_id">
            <router-link :to="{ name: 'Tag', params: { tag_id: tag.tag_id }}">
              {{ tag.tag_name }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'LeftBarTags',
    data() {
        return {

        }
    },
    props: ['tags'],
    methods: {

    }
}
</script>

<style scoped>
</style>
