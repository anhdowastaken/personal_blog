<template>
    <div>
        <header-component></header-component>
        <header-image-component></header-image-component>

        <div class="blog-page area-padding">
          <div class="container">
            <div class="row">
              <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                <div class="page-head-blog">
                  <div class="single-blog-page" v-if="isAuthenticated">
                    <div class="left-blog">
                      <router-link to="/new_post">new post</router-link>
                    </div>
                  </div>
                  <div class="single-blog-page">
                    <!-- search option start -->
                    <form action="#">
                      <div class="search-option">
                        <input type="text" placeholder="Search...">
                        <button class="button" type="submit">
                                                  <i class="fa fa-search"></i>
                                              </button>
                      </div>
                    </form>
                    <!-- search option end -->
                  </div>
                  <div class="single-blog-page">
                    <div class="left-tags blog-tags">
                      <div class="popular-tag left-side-tags left-blog">
                        <h4>tags</h4>
                        <ul>
                          <li>
                            <a href="#">life</a>
                          </li>
                          <li>
                            <a href="#">work</a>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
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
                              v-if="post.comments.length == 1">
                          <i class="fa fa-comment-o"></i> 1 comment
                        </span>
                        <span class="comments-type"
                              v-else-if="post.comments.length > 1">
                          <i class="fa fa-comment-o"></i> {{ post.comments.length }} comments
                        </span>
                      </div>
                      <div class="blog-text">
                        <router-link :to="{ name: 'Post', params: { post_id: post.post_id }}">
                            <h4>{{ post.header }}</h4>
                            <p style="color: gray;">{{ post.preview }}</p>
                        </router-link>
                      </div>
                      <!-- <span>
                        <a href="blog-details.html" class="ready-btn">Read more</a>
                      </span> -->
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
        <!-- End Blog Area -->

        <footer-component></footer-component>

        <a href="#" class="back-to-top"><i class="fa fa-chevron-up"></i></a>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import HeaderComponent from '@/components/HeaderComponent'
import HeaderImageComponent from '@/components/HeaderImageComponent'
import FooterComponent from '@/components/FooterComponent'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import NewPost from '@/components/NewPost'
import Post from '@/components/Post'

import { fetchAllPosts } from '@/api'
import { fetchPublicPosts } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Home',
    components: {
        HeaderComponent,
        HeaderImageComponent,
        FooterComponent,
        Login,
        Logout,
        NewPost,
        Post
    },
    data () {
        return {
            isHttpRequestCompleted: true
        }
    },
    beforeMount() {
        this.$nextTick(() => {
            this.fetchPosts(this.currentPage)
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
            'setPageInfo'
        ]),
        fetchPosts: function(page) {
            if (this.isAuthenticated) {
                fetchAllPosts(this.jwt, page)
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
            } else {
                fetchPublicPosts(page)
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
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
