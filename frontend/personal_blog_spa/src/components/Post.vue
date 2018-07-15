<template>
    <div>
        <header-component></header-component>
        <header-image-component></header-image-component>

        <back></back>

        <div class="blog-page area-padding">
          <div class="container">
            <div class="row">
              <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                <div class="page-head-blog">
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
                    <div class="left-blog">
                      <h4>archive</h4>
                      <ul>
                        <li>
                          <a href="#">July 2016</a>
                        </li>
                        <li>
                          <a href="#">June 2016</a>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="single-blog-page">
                    <div class="left-tags blog-tags">
                      <div class="popular-tag left-side-tags left-blog">
                        <h4>popular tags</h4>
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
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <!-- single-blog start -->
                    <article class="blog-post-wrapper">
                      <div class="post-information"
                           v-if="post">
                        <h2>{{ post.header }}</h2>
                        <div class="entry-meta">
                          <span class="author-meta"><i class="fa fa-user"></i> <a href="#">admin</a></span>
                          <span><i class="fa fa-clock-o"></i> march 28, 2016</span>
                          <span>
                            <i class="fa fa-tags"></i>
                            <a href="#">life</a>
                          </span>
                          <span><i class="fa fa-comments-o"></i> <a href="#">6 comments</a></span>
                        </div>
                        <div class="entry-content" v-html="post.body"></div>
                      </div>
                    </article>
                    <div class="clear"></div>
                    <div class="single-post-comments">
                      <div class="comments-area">
                        <div class="comments-heading">
                          <h3>6 comments</h3>
                        </div>
                        <div class="comments-list">
                          <ul>
                            <li>
                              <div class="comments-details">
                                <div class="comments-list-img">
                                  <img src="static/img/blog/b02.jpg" alt="post-author">
                                </div>
                                <div class="comments-content-wrap">
                                  <span>
                                    <b><a href="#">admin</a></b>
                                    Post author
                                    <span class="post-time">October 6, 2014 at 6:18 pm </span>
                                  </span>
                                  <p>Quisque orci nibh, porta vitae sagittis sit amet, vehicula vel mauris. Aenean at justo dolor. Fusce ac sapien bibendum, scelerisque libero nec</p>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                      <div class="comment-respond">
                        <h3 class="comment-reply-title">Leave a Reply </h3>
                        <span class="email-notes">Your email address will not be published. Required fields are marked *</span>
                        <form action="#">
                          <div class="row">
                            <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                              <p>Name *</p>
                              <input type="text" />
                            </div>
                            <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                              <p>Email *</p>
                              <input type="email" />
                            </div>
                            <div class="col-lg-12 col-md-12 col-sm-12 comment-form-comment">
                              <p>Comment</p>
                              <textarea id="message-box" cols="30" rows="10"></textarea>
                              <input type="submit" value="Post Comment" />
                            </div>
                          </div>
                        </form>
                      </div>
                    </div>
                    <!-- single-blog end -->
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

import HeaderComponent from '@/components/HeaderComponent'
import HeaderImageComponent from '@/components/HeaderImageComponent'
import FooterComponent from '@/components/FooterComponent'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Back from '@/components/Back'

import { fetchPost } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Post',
    components: {
        HeaderComponent,
        HeaderImageComponent,
        FooterComponent,
        Login,
        Logout,
        Back
    },
    data () {
        return {
            post: undefined,
            isHttpRequestCompleted: true
        }
    },
    props: ['post_id'],
    beforeMount() {
        this.$nextTick(() => {
            fetchPost(this.jwt, this.post_id)
                .then(response => {
                    if (response.status === 200) {
                        this.post = response.data
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
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
