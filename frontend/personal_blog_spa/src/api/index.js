import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function fetchAllPosts(jwt, page) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_all_posts?page=${page}`,
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function fetchPublicPosts(page) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_public_posts?page=${page}`)
}

export function submitLogin(username, password) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/login`,
                      { username: username,
                        password: password
                      })
}

export function submitLogout() {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/logout`)
}

export function submitResetPassword(jwt, username) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/reset_password`,
                      { username: username },
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function submitChangePassword(jwt, old_password, new_password) {
    return axios.create({ withCredentials: true })
                .put(`${API_URL}/change_password`,
                      { old_password: old_password, new_password: new_password },
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function createNewPost(jwt, header, body, tags, private_post) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/create_new_post`,
                      { header: header,
                        body: body,
                        tags: tags,
                        private_post: private_post
                      },
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function fetchPost(jwt, post_id) {
    if (jwt) {
        return axios.create({ withCredentials: true })
                    .get(`${API_URL}/get_post?post_id=${post_id}`,
                          { headers: { Authorization: `Bearer: ${jwt}` } })
    } else {
        return axios.create({ withCredentials: true })
                    .get(`${API_URL}/get_post?post_id=${post_id}`)
    }
}

export function submitComment(jwt, post_id, content, author_name, author_email, recaptcha_response) {
    if (jwt) {
        return axios.create({ withCredentials: true })
                    .post(`${API_URL}/post_comment`,
                          { post_id: post_id,
                            content: content,
                            author_name: author_name,
                            author_email: author_email },
                          { headers: { Authorization: `Bearer: ${jwt}` } })
    } else {
        return axios.create({ withCredentials: true })
                    .post(`${API_URL}/post_comment`,
                          { post_id: post_id,
                            content: content,
                            author_name: author_name,
                            author_email: author_email,
                            recaptcha_response: recaptcha_response })
    }
}

export function submitDeletePost(jwt, post_id) {
    return axios.create({ withCredentials: true })
                .delete(`${API_URL}/delete_post`,
                       { headers: { Authorization: `Bearer: ${jwt}` },
                         data: { post_id: post_id } })
}

export function submitUpdatePost(jwt, post_id, header, body, tags, private_post) {
    return axios.create({ withCredentials: true })
                .put(`${API_URL}/update_post`,
                     { post_id: post_id,
                       header: header,
                       body: body,
                       tags: tags,
                       private_post: private_post
                     },
                     { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function submitDeleteComment(jwt, comment_id) {
    return axios.create({ withCredentials: true })
                .delete(`${API_URL}/delete_comment`,
                       { headers: { Authorization: `Bearer: ${jwt}` },
                         data: { comment_id: comment_id} })
}

export function fetchTags() {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_tags`)
}

export function fetchAllPostsByTag(jwt, page, tag_id) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_all_posts_by_tag?page=${page}&tag_id=${tag_id}`,
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function fetchPublicPostsByTag(page, tag_id) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_public_posts_by_tag?page=${page}&tag_id=${tag_id}`)
}

export function searchAllPostsByKeyword(jwt, page, keyword) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/search_all_posts_by_keyword?page=${page}&keyword=${keyword}`,
                      { headers: { Authorization: `Bearer: ${jwt}` } })
}

export function searchPublicPostsByKeyword(page, keyword) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/search_public_posts_by_keyword?page=${page}&keyword=${keyword}`)
}
