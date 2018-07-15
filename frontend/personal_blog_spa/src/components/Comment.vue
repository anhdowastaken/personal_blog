<template>
  <li v-if="comment">
    <div class="comments-details">
      <div class="comments-list-img">
        <img v-bind:src="comment.author_avatar" alt="post-author">
      </div>
      <div class="comments-content-wrap">
        <span>
          <b>{{ comment.author_name }}</b>
          <span class="post-time">{{ comment.created_at }}</span>
        </span>
        <p>{{ comment.content }}</p>
      </div>
    </div>
  </li>
</template>

<script>
export default {
    name: 'Comment',
    components: {
    },
    data () {
        return {
        }
    },
    props: {
        comment: {
            type: Object,
            default: undefined
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
