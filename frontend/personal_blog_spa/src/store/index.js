import Vue from 'vue'
import Vuex from 'vuex'

import router from '@/router'

import { key_jwt, key_user_data } from '@/common'

// imports of AJAX functions go here
import { submitLogout } from '@/api'
import { isValidJwt } from '@/utils'

Vue.use(Vuex)

const state = {
    // The state object will serve as the single source of truth where all
    // the important application-level data is contained within the store.
    // This state object will contain data that can be accessed and watched for
    // changes by any components interested in them such as the Home component.
    posts: [],
    currentPage: 1,
    has_next: false,
    has_prev: false,
    next_num: 1,
    prev_num: 1,
    userData: {},
    jwt: '',
    // States of notification modal
    notificationHeader: '',
    notificationBody: '',
    notificationDisplay: false,
    notificationDisplayStyle: 'none',
    notificationRedirectAfterClose: false,
    notificationRedirectComponentName: ''
}

const actions = {
    // The actions object is where I will define what are known as action methods.
    // Action methods are referred to as being "dispatched" and they're used to
    // handle asynchronous operations such as AJAX calls to an external service or API.
    logout(context) {
        return submitLogout()
            .then(() => {
                context.commit('setPosts', { posts: [] })
                context.commit('removeJwtToken')
                context.commit('removeUserData')
            })
            .catch(error => {
                if (error) {
                    context.commit('setNotificationContent', { header: 'Error',
                                                               body: error })
                    context.commit('showNotification')
                } else {
                    context.commit('setNotificationContent', { header: 'Error',
                                                               body: 'Error' })
                    context.commit('showNotification')
                }
            })
    }
}

const mutations = {
    // The mutations object provides methods which are referred to being "committed"
    // and serve as the one and only way to change the state of the data in the state object.
    // When a mutation is committed any components that are referencing
    // the now reactive data in the state object are updated with the new values, causing the UI to update and re-render its elements.
    setPosts(state, payload) {
        for (let i = 0; i < payload.posts.length; i++) {
            let post = payload.posts[i]

            let d = new Date(post['last_edit_at'] * 1000)
            post['last_edit_at'] = d.toLocaleString()
        }
        state.posts = payload.posts
    },
    setPageInfo(state, payload) {
        state.currentPage = payload.currentPage
        state.has_next = payload.has_next
        state.has_prev = payload.has_prev
        state.next_num = payload.next_num
        state.prev_num = payload.prev_num
    },
    setUserData(state, payload) {
        // console.log('setUserData payload = ', payload)
        if (payload.userData['last_login_at']) {
            // Backend returns timestamp in second (UTC)
            let d = new Date()
            d = new Date(payload.userData['last_login_at'] * 1000)
            payload.userData['last_login_at'] = d.toLocaleString()
        }
        localStorage.setItem(key_user_data, JSON.stringify(payload.userData))
        state.userData = payload.userData
    },
    setJwtToken(state, payload) {
        // console.log('setJwtToken payload = ', payload)
        localStorage.setItem(key_jwt, payload.jwt)
        state.jwt = payload.jwt
    },
    removeUserData(state) {
        localStorage.removeItem(key_user_data)
        state.userData = {}
    },
    removeJwtToken(state, payload) {
        localStorage.removeItem(key_jwt)
        state.jwt = ''
    },
    setNotificationContent(state, payload) {
        state.notificationHeader = payload['header']
        state.notificationBody = payload['body']
    },
    setNotificationRedirectAfterClose(state, payload) {
        state.notificationRedirectAfterClose = payload['redirect']
        state.notificationRedirectComponentName = payload['component_name']
    },
    showNotification(state) {
        state.notificationDisplayStyle = 'block'
        state.notificationDisplay = true
    },
    hideNotification(state) {
        state.notificationDisplayStyle = 'none'
        state.notificationDisplay = false
        state.notificationHeader = ''
        state.notificationBody = ''
        if (state.notificationRedirectAfterClose == true) {
            state.notificationRedirectAfterClose = false
            let componentName = state.notificationRedirectComponentName
            state.notificationRedirectComponentName = ''
            router.push({ name: componentName })
        }
    }
}

const getters = {
    // The getters object contains methods also, but in this case they serve to
    // access the state data utilizing some logic to return information.
    // Getters are useful for reducing code duplication and promote reusability across many components.
    isAuthenticated(state) {
        if (state.jwt) {
            return isValidJwt(state.jwt)
        } else {
            return isValidJwt(localStorage.getItem(key_jwt))
        }
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store
