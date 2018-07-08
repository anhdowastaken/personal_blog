import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function fetchAllPosts(jwt) {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_all_posts`,
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function fetchPublicPosts() {
    return axios.create({ withCredentials: true })
                .get(`${API_URL}/get_public_posts`)
}

export function submitLogin(username, password) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/login`,
                      { username: username,
                        password: password
                      }
                    )
}

export function submitLogout() {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/logout`)
}

export function submitResetPassword(jwt, username) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/reset_password`,
                      { username: username },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}

export function submitChangePassword(jwt, old_password, new_password) {
    return axios.create({ withCredentials: true })
                .post(`${API_URL}/change_password`,
                      { old_password: old_password, new_password: new_password },
                      { headers: { Authorization: `Bearer: ${jwt}` } }
                    )
}
