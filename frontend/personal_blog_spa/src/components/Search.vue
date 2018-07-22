<template>
  <div class="blog-page area-padding">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
          <div class="page-head-blog">
            <div class="single-blog-page" v-if="isAuthenticated">
              <button type="button"
                      class="btn btn-primary btn-block btn-new-post"
                      v-on:click.stop.prevent="$router.push('/post_new')">Compose New Post</button>
            </div>
            <left-bar-profile></left-bar-profile>
            <left-bar-search></left-bar-search>
            <left-bar-tags v-bind:tags="tags"></left-bar-tags>
          </div>
        </div>
        <!-- End left sidebar -->
        <!-- Start single blog -->
        <div class="col-md-8 col-sm-8 col-xs-12">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12"
                 v-for="post in posts" :key="post.id">
              <div class="single-blog">
                <div class="blog-meta">
                  <span class="date-type">
                    <i class="fa fa-calendar"></i>{{ post.last_edit_at }}
                  </span>
                  <span class="comments-type"
                        v-if="post.comments == 1">
                    <i class="fa fa-comment-o"></i> 1 comment
                  </span>
                  <span class="comments-type"
                        v-else-if="post.comments > 1">
                    <i class="fa fa-comment-o"></i> {{ post.comments }} comments
                  </span>
                  <span v-if="isAuthenticated && post.private_post"
                        class="label label-default">Private</span>
                </div>
                <div class="blog-text">
                  <router-link :to="{ name: 'Post', params: { post_id: post.post_id }}">
                      <h4>{{ post.header }}</h4>
                      <p style="color: gray;">{{ post.preview }}</p>
                  </router-link>
                </div>
              </div>
            </div>
            <!-- End single blog -->
            <div class="blog-pagination">
              <ul class="pagination">
                <li><a v-if="has_prev"
                       v-on:click.stop.prevent="fetchPosts(prev_num)">&lt;</a></li>
                <li><a v-if="has_next"
                       v-on:click.stop.prevent="fetchPosts(next_num)">&gt;</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import LeftBarProfile from '@/components/LeftBarProfile'
import LeftBarSearch from '@/components/LeftBarSearch'
import LeftBarTags from '@/components/LeftBarTags'

import { searchAllPostsByKeyword} from '@/api'
import { searchPublicPostsByKeyword } from '@/api'
import { fetchTags } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Search',
    components: {
        LeftBarSearch,
        LeftBarTags,
        LeftBarProfile
    },
    data () {
        return {
            tags: []
        }
    },
    props: ['keyword'],
    beforeMount() {
        this.$nextTick(() => {
            this.searchPosts(this.currentPage)

            fetchTags()
                .then(response => {
                    if (response.status === 200) {
                        this.tags = response.data
                    }
                })
                .catch(error => {
                    if (error.response.data['message']) {
                        this.setNotificationContent({ header: 'Error',
                                                      body: error.response.data['message'] })
                        this.showNotification()
                    } else if (error) {
                        this.setNotificationContent({ header: 'Error',
                                                      body: 'Error Authenticating: ' + error })
                        this.showNotification()
                    } else {
                        this.setNotificationContent({ header: 'Error',
                                                      body: 'Error' })
                        this.showNotification()
                    }
                })
        })
    },
    computed: {
        ...mapState({
            jwt: function(state) {
                if (state.jwt) {
                    return state.jwt 
                } else {
                    return localStorage.getItem(key_jwt)
                }
            },
            posts: state => state.posts,
            currentPage: state => state.currentPage,
            has_next: state => state.has_next,
            has_prev: state => state.has_prev,
            next_num: state => state.next_num,
            prev_num: state => state.prev_num
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    },
    methods: {
        ...mapMutations([
            'setPosts',
            'setPageInfo',
            'setNotificationContent',
            'showNotification',
            'setNotificationRedirectAfterClose'
        ]),
        searchPosts: function(page) {
            this.$nextTick(() => {
                if (this.isAuthenticated) {
                    searchAllPostsByKeyword(this.jwt, page, this.keyword)
                        .then(response => {
                            if (response.status === 200) {
                                this.setPosts({ posts: response.data['posts'] })
                                this.setPageInfo({ currentPage: page,
                                                   has_next: response.data['has_next'],
                                                   has_prev: response.data['has_prev'],
                                                   next_num: response.data['next_num'],
                                                   prev_num: response.data['prev_num']
                                                 })
                            }
                        })
                        .catch(error => {
                            if (error.response.data['message']) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: error.response.data['message'] })
                                this.showNotification()

                                if (error.response.status == 401) {
                                    this.setNotificationRedirectAfterClose({ redirect: true,
                                                                             component_name: 'Login' })
                                    this.$store.dispatch('logout')
                                }
                            } else if (error) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error Authenticating: ' + error })
                                this.showNotification()
                            } else {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error' })
                                this.showNotification()
                            }
                        })
                } else {
                    searchPublicPostsByKeyword(page, this.keyword)
                        .then(response => {
                            if (response.status === 200) {
                                this.setPosts({ posts: response.data['posts'] })
                                this.setPageInfo({ currentPage: page,
                                                   has_next: response.data['has_next'],
                                                   has_prev: response.data['has_prev'],
                                                   next_num: response.data['next_num'],
                                                   prev_num: response.data['prev_num']
                                                 })
                            }
                        })
                        .catch(error => {
                            if (error.response.data['message']) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: error.response.data['message'] })
                                this.showNotification()
                            } else if (error) {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error Authenticating: ' + error })
                                this.showNotification()
                            } else {
                                this.setNotificationContent({ header: 'Error',
                                                              body: 'Error' })
                                this.showNotification()
                            }
                        })
                }
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.btn-new-post {
  margin-bottom: 30px;
}
</style>
